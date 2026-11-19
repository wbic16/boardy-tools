# Play-test transcript — boardy_mcp.py

Real run of `test_client.py` against `boardy_mcp.py` over stdio, loading `boardy.phext` (46 scrolls, 8594 bytes). Nothing trimmed; every message below was exchanged verbatim.

```
>>> {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "playtest",
      "version": "0"
    }
  }
}

<<< {
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "boardy-phext",
      "version": "0.1.0"
    }
  }
}

CHECK initialize: PASS (server boardy-phext)

>>> {
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}

>>> {
  "jsonrpc": "2.0",
  "id": 2,
  "method": "ping"
}

<<< {
  "jsonrpc": "2.0",
  "id": 2,
  "result": {}
}

CHECK ping: PASS 

>>> {
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/list"
}

<<< {
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "tools": [
      {
        "name": "load",
        "description": "Load and parse a phext file from a local path.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": {
              "type": "string"
            }
          },
          "required": [
            "path"
          ]
        }
      },
      {
        "name": "toc",
        "description": "List every scroll coordinate with the first line of its scroll.",
        "inputSchema": {
          "type": "object",
          "properties": {}
        }
      },
      {
        "name": "fetch",
        "description": "Return the full text of the scroll at a coordinate (e.g. 1.1.1/1.2.1/1.1.11).",
        "inputSchema": {
          "type": "object",
          "properties": {
            "coordinate": {
              "type": "string"
            }
          },
          "required": [
            "coordinate"
          ]
        }
      },
      {
        "name": "search",
        "description": "Return coordinates of scrolls containing the text (case-insensitive substring).",
        "inputSchema": {
          "type": "object",
          "properties": {
            "text": {
              "type": "string"
            }
          },
          "required": [
            "text"
          ]
        }
      }
    ]
  }
}

CHECK tools/list: PASS ['load', 'toc', 'fetch', 'search']

>>> {
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "load",
    "arguments": {
      "path": "/home/hatch/workspace/boardy-receipts/boardy.phext"
    }
  }
}

<<< {
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "loaded /home/hatch/workspace/boardy-receipts/boardy.phext: 46 scrolls, 8594 bytes"
      }
    ]
  }
}

CHECK load: PASS (loaded /home/hatch/workspace/boardy-receipts/boardy.phext: 46 scrolls, 8594 bytes)

>>> {
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "toc",
    "arguments": {}
  }
}

<<< {
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "1.1.1/1.1.1/1.1.1  boardy.phext \u2014 Boardy's reference instance (N1-N20) as phext\n1.1.1/1.2.1/1.1.11  node: N11\n1.1.1/1.2.1/1.1.12  node: N12\n1.1.1/1.2.1/1.1.13  node: N13\n1.1.1/1.2.1/1.1.19  node: N19\n1.1.1/1.3.1/1.1.1  node: N1\n1.1.1/1.3.1/1.1.2  node: N2\n1.1.1/1.3.1/1.1.3  node: N3\n1.1.1/1.3.1/1.1.4  node: N4\n1.1.1/1.3.1/1.1.5  node: N5\n1.1.1/1.3.1/1.1.6  node: N6\n1.1.1/1.3.1/1.1.7  node: N7\n1.1.1/1.3.1/1.1.8  node: N8\n1.1.1/1.3.1/1.1.9  node: N9\n1.1.1/1.3.1/1.1.10  node: N10\n1.1.1/1.3.1/1.1.14  node: N14\n1.1.1/1.3.1/1.1.15  node: N15\n1.1.1/1.3.1/1.1.16  node: N16\n1.1.1/1.3.1/1.1.17  node: N17\n1.1.1/1.3.1/1.1.18  node: N18\n1.1.1/1.3.1/1.1.20  node: N20\n1.1.1/1.4.1/1.1.1  edge: E1\n1.1.1/1.4.1/1.1.2  edge: E2\n1.1.1/1.4.1/1.1.3  edge: E3\n1.1.1/1.4.1/1.1.4  edge: E4\n1.1.1/1.4.1/1.1.5  edge: E5\n1.1.1/1.4.1/1.1.6  edge: E6\n1.1.1/1.4.1/1.1.7  edge: E7\n1.1.1/1.4.1/1.1.8  edge: E8\n1.1.1/1.4.1/1.1.9  edge: E9\n1.1.1/1.4.1/1.1.10  edge: E10\n1.1.1/1.4.1/1.1.11  edge: E11\n1.1.1/1.4.1/1.1.12  edge: E12\n1.1.1/1.4.1/1.1.13  edge: E13\n1.1.1/1.4.1/1.1.14  edge: E14\n1.1.1/1.4.1/1.1.15  edge: E15\n1.1.1/1.4.1/1.1.16  edge: E16\n1.1.1/1.4.1/1.1.17  edge: E17\n1.1.1/1.4.1/1.1.18  edge: E18\n1.1.1/1.4.1/1.1.19  edge: E19\n1.1.1/1.4.1/1.1.20  edge: E20\n1.1.1/1.4.1/1.1.21  edge: E21\n1.1.1/1.4.1/1.1.22  edge: E22\n1.1.1/1.4.1/1.1.23  edge: E23\n1.1.1/1.4.1/1.1.24  edge: E24\n1.1.1/1.4.1/1.1.25  edge: E25"
      }
    ]
  }
}

CHECK toc: PASS (46 lines)

>>> {
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "fetch",
    "arguments": {
      "coordinate": "1.1.1/1.3.1/1.1.1"
    }
  }
}

<<< {
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "node: N1\nkind: person\nattributes: role, function, stage, current_focus\nattribute values: not supplied by the spec\n"
      }
    ]
  }
}

CHECK fetch node: PASS (1.1.1/1.3.1/1.1.1)

>>> {
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "fetch",
    "arguments": {
      "coordinate": "1.1.1/1.4.1/1.1.11"
    }
  }
}

<<< {
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "edge: E11\nN11 -blocked_by(3)-> N12\nsource: N11 @ 1.1.1/1.2.1/1.1.11\ntarget: N12 @ 1.1.1/1.2.1/1.1.12\ntype: blocked_by\nweight: 3\nfamily: dense (ask->blocked_by)\n"
      }
    ]
  }
}

CHECK fetch edge: PASS (1.1.1/1.4.1/1.1.11)

>>> {
  "jsonrpc": "2.0",
  "id": 8,
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "text": "blocked_by"
    }
  }
}

<<< {
  "jsonrpc": "2.0",
  "id": 8,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "3 scroll(s) contain 'blocked_by':\n1.1.1/1.1.1/1.1.1\n1.1.1/1.4.1/1.1.11\n1.1.1/1.4.1/1.1.12"
      }
    ]
  }
}

CHECK search: PASS (3 hits)

>>> {
  "jsonrpc": "2.0",
  "id": 9,
  "method": "tools/call",
  "params": {
    "name": "fetch",
    "arguments": {
      "coordinate": "1.1.1/1.9.1/1.1.1"
    }
  }
}

<<< {
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "error: no scroll at 1.1.1/1.9.1/1.1.1"
      }
    ],
    "isError": true
  }
}

CHECK fetch absent errors: PASS (error: no scroll at 1.1.1/1.9.1/1.1.1)

PLAYTEST: ALL GREEN
```
