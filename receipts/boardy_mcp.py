#!/usr/bin/env python3
"""boardy_mcp.py — a very simple MCP server for loading a phext file.

Standard library only. Speaks MCP over stdio (newline-delimited JSON-RPC 2.0):
initialize, notifications/initialized, ping, tools/list, tools/call.

Tools:
  load   {path}       parse a phext file; report scroll count and byte size
  toc    {}           every coordinate with the first line of its scroll
  fetch  {coordinate} the full text of one scroll
  search {text}       coordinates whose scrolls contain the text

Run it directly (an MCP client spawns it the same way):
  python3 boardy_mcp.py
"""

import json
import sys

# Phext break bytes, outermost dimension first. A break increments its own
# dimension and resets every dimension inside it to 1. Line (0x0A) is content.
BREAK_LEVEL = {
    "\x01": 0,  # Library
    "\x1f": 1,  # Shelf
    "\x1e": 2,  # Series
    "\x1d": 3,  # Collection
    "\x1c": 4,  # Volume
    "\x1a": 5,  # Book
    "\x19": 6,  # Chapter
    "\x18": 7,  # Section
    "\x17": 8,  # Scroll
}

DOC = {"scrolls": {}, "size": 0, "path": None}  # the loaded document


def fmt(coord):
    return "%d.%d.%d/%d.%d.%d/%d.%d.%d" % tuple(coord)


def parse_phext(text):
    """Explode phext text into {coordinate_tuple: scroll_text}."""
    scrolls = {}
    state = [1] * 9
    buf = []
    for ch in text:
        lvl = BREAK_LEVEL.get(ch)
        if lvl is None:
            buf.append(ch)
            continue
        content = "".join(buf)
        if content:  # a scroll exists when it holds at least a byte
            scrolls[tuple(state)] = content
        buf = []
        state[lvl] += 1
        for j in range(lvl + 1, 9):
            state[j] = 1
    content = "".join(buf)
    if content:
        scrolls[tuple(state)] = content
    return scrolls


def parse_coordinate(text):
    parts = text.replace("/", ".").split(".")
    if len(parts) != 9:
        raise ValueError("coordinate needs 9 components, e.g. 1.1.1/1.2.1/1.1.11")
    coord = tuple(int(p) for p in parts)
    if any(n < 1 for n in coord):
        raise ValueError("coordinate components must be >= 1")
    return coord


def tool_load(args):
    path = args["path"]
    with open(path, "rb") as f:
        raw = f.read()
    DOC["scrolls"] = parse_phext(raw.decode("utf-8", errors="surrogateescape"))
    DOC["size"] = len(raw)
    DOC["path"] = path
    return "loaded %s: %d scrolls, %d bytes" % (path, len(DOC["scrolls"]), DOC["size"])


def require_doc():
    if DOC["path"] is None:
        raise ValueError("no document loaded; call load first")


def tool_toc(_args):
    require_doc()
    lines = []
    for coord in sorted(DOC["scrolls"]):
        first = DOC["scrolls"][coord].split("\n", 1)[0]
        lines.append("%s  %s" % (fmt(coord), first))
    return "\n".join(lines)


def tool_fetch(args):
    require_doc()
    coord = parse_coordinate(args["coordinate"])
    if coord not in DOC["scrolls"]:
        raise ValueError("no scroll at %s" % fmt(coord))
    return DOC["scrolls"][coord]


def tool_search(args):
    require_doc()
    needle = args["text"].lower()
    hits = [fmt(c) for c in sorted(DOC["scrolls"])
            if needle in DOC["scrolls"][c].lower()]
    if not hits:
        return "no scrolls contain %r" % args["text"]
    return "%d scroll(s) contain %r:\n%s" % (len(hits), args["text"], "\n".join(hits))


TOOLS = [
    {"name": "load", "fn": tool_load,
     "description": "Load and parse a phext file from a local path.",
     "schema": {"type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]}},
    {"name": "toc", "fn": tool_toc,
     "description": "List every scroll coordinate with the first line of its scroll.",
     "schema": {"type": "object", "properties": {}}},
    {"name": "fetch", "fn": tool_fetch,
     "description": "Return the full text of the scroll at a coordinate "
                    "(e.g. 1.1.1/1.2.1/1.1.11).",
     "schema": {"type": "object",
                "properties": {"coordinate": {"type": "string"}},
                "required": ["coordinate"]}},
    {"name": "search", "fn": tool_search,
     "description": "Return coordinates of scrolls containing the text "
                    "(case-insensitive substring).",
     "schema": {"type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"]}},
]


def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def result(rid, value):
    send({"jsonrpc": "2.0", "id": rid, "result": value})


def error(rid, code, message):
    send({"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}})


def handle(req):
    method = req.get("method", "")
    rid = req.get("id")
    params = req.get("params") or {}
    if method == "initialize":
        result(rid, {
            "protocolVersion": params.get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "boardy-phext", "version": "0.1.0"},
        })
    elif method == "notifications/initialized":
        pass  # notification: no response
    elif method == "ping":
        result(rid, {})
    elif method == "tools/list":
        result(rid, {"tools": [
            {"name": t["name"], "description": t["description"],
             "inputSchema": t["schema"]} for t in TOOLS]})
    elif method == "tools/call":
        name = params.get("name")
        tool = next((t for t in TOOLS if t["name"] == name), None)
        if tool is None:
            error(rid, -32602, "unknown tool: %s" % name)
            return
        try:
            text = tool["fn"](params.get("arguments") or {})
            result(rid, {"content": [{"type": "text", "text": text}]})
        except Exception as exc:  # tool errors ride back as content, per MCP
            result(rid, {"content": [{"type": "text", "text": "error: %s" % exc}],
                         "isError": True})
    elif rid is not None:
        error(rid, -32601, "method not found: %s" % method)


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            handle(json.loads(line))
        except Exception as exc:
            print("boardy_mcp: %s" % exc, file=sys.stderr)


if __name__ == "__main__":
    main()
