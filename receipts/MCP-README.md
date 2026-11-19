# boardy-phext — a tiny MCP server for phext files

One Python file, standard library only. Needs nothing but Python 3.
It loads a phext file and serves its scrolls over MCP (stdio).

Run it the way any MCP client does — point the client at:

    python3 boardy_mcp.py

Or in an MCP client config:

    {
      "mcpServers": {
        "boardy-phext": {
          "command": "python3",
          "args": ["/path/to/boardy_mcp.py"]
        }
      }
    }

Tools (call `load` first):

- `load {path}` — parse a phext file; returns scroll count and byte size.
- `toc {}` — every scroll coordinate with the first line of its scroll.
- `fetch {coordinate}` — full text of one scroll, e.g. `1.1.1/1.2.1/1.1.11`.
- `search {text}` — coordinates of scrolls containing the text.

`boardy.phext` (next to the server) holds Boardy's reference instance
N1–N20: 46 scrolls — a header with the coordinate map, 20 node scrolls,
25 edge scrolls. `test_client.py` play-tests the whole interface;
`PLAYTEST.md` is the transcript of a real run.
