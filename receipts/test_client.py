#!/usr/bin/env python3
"""Play-test client for boardy_mcp.py.

Spawns the server over stdio, runs the MCP handshake, lists tools, loads
boardy.phext, fetches the TOC, fetches a node scroll and an edge scroll,
and runs a search. Prints the full transcript and writes PLAYTEST.md.
Exits non-zero if any step fails.
"""

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
PHEXT = HERE / "boardy.phext"
NODE = "1.1.1/1.3.1/1.1.1"    # N1, the person (solution space)
EDGE = "1.1.1/1.4.1/1.1.11"   # E11: N11 -blocked_by(3)-> N12 (join space)
NEEDLE = "blocked_by"

transcript = []
failures = []


def log(direction, obj):
    transcript.append("%s %s" % (direction, json.dumps(obj, indent=2)))


def check(label, ok, detail=""):
    transcript.append("CHECK %s: %s %s" % (label, "PASS" if ok else "FAIL", detail))
    if not ok:
        failures.append(label)


def main():
    proc = subprocess.Popen(
        [sys.executable, str(HERE / "boardy_mcp.py")],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    next_id = [0]

    def call(method, params=None):
        next_id[0] += 1
        req = {"jsonrpc": "2.0", "id": next_id[0], "method": method}
        if params is not None:
            req["params"] = params
        log(">>>", req)
        proc.stdin.write(json.dumps(req) + "\n")
        proc.stdin.flush()
        resp = json.loads(proc.stdout.readline())
        log("<<<", resp)
        return resp

    def notify(method):
        req = {"jsonrpc": "2.0", "method": method}
        log(">>>", req)
        proc.stdin.write(json.dumps(req) + "\n")
        proc.stdin.flush()

    def tool(name, args):
        resp = call("tools/call", {"name": name, "arguments": args})
        return resp.get("result", {})

    try:
        r = call("initialize", {"protocolVersion": "2024-11-05",
                                "capabilities": {},
                                "clientInfo": {"name": "playtest", "version": "0"}})
        check("initialize", r["result"]["serverInfo"]["name"] == "boardy-phext",
              "(server %s)" % r["result"]["serverInfo"]["name"])
        notify("notifications/initialized")

        r = call("ping")
        check("ping", r.get("result") == {})

        r = call("tools/list")
        names = [t["name"] for t in r["result"]["tools"]]
        check("tools/list", names == ["load", "toc", "fetch", "search"], str(names))

        res = tool("load", {"path": str(PHEXT)})
        text = res["content"][0]["text"]
        check("load", "46 scrolls" in text and "8594 bytes" in text, "(%s)" % text)

        res = tool("toc", {})
        toc_lines = res["content"][0]["text"].split("\n")
        check("toc", len(toc_lines) == 46, "(%d lines)" % len(toc_lines))

        res = tool("fetch", {"coordinate": NODE})
        node_text = res["content"][0]["text"]
        check("fetch node", "node: N1" in node_text and "kind: person" in node_text,
              "(%s)" % NODE)

        res = tool("fetch", {"coordinate": EDGE})
        edge_text = res["content"][0]["text"]
        check("fetch edge", "N11 -blocked_by(3)-> N12" in edge_text, "(%s)" % EDGE)

        res = tool("search", {"text": NEEDLE})
        hits = res["content"][0]["text"]
        check("search", EDGE in hits, "(%d hits)" % (hits.count("\n") - 1 + 1))

        res = tool("fetch", {"coordinate": "1.1.1/1.9.1/1.1.1"})
        check("fetch absent errors", res.get("isError") is True,
              "(%s)" % res["content"][0]["text"])
    finally:
        proc.stdin.close()
        proc.wait(timeout=10)

    verdict = "PLAYTEST: ALL GREEN" if not failures else \
        "PLAYTEST: FAILED (%s)" % ", ".join(failures)
    transcript.append(verdict)

    body = "\n\n".join(transcript)
    (HERE / "PLAYTEST.md").write_text(
        "# Play-test transcript — boardy_mcp.py\n\n"
        "Real run of `test_client.py` against `boardy_mcp.py` over stdio, "
        "loading `boardy.phext` (46 scrolls, 8594 bytes). Nothing trimmed; "
        "every message below was exchanged verbatim.\n\n```\n%s\n```\n" % body)
    print(body)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
