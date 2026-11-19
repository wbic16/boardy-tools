"""Minimal phext serializer/parser (stdlib only).

Nine components: Library.Shelf.Series / Collection.Volume.Book / Chapter.Section.Scroll
Delimiter bytes by level (most -> least significant):
  Library 0x01, Shelf 0x1F, Series 0x1E, Collection 0x1D, Volume 0x1C,
  Book 0x1A, Chapter 0x19, Section 0x18, Scroll 0x17.  Line feed 0x0A is content.
Dead-reckoning: emitting the delimiter for level L increments component L and
resets every less-significant component to 1.
"""

LEVEL_BYTES = [0x01, 0x1F, 0x1E, 0x1D, 0x1C, 0x1A, 0x19, 0x18, 0x17]
_BYTE_TO_LEVEL = {b: i for i, b in enumerate(LEVEL_BYTES)}


def fmt(coord):
    return "%d.%d.%d/%d.%d.%d/%d.%d.%d" % tuple(coord)


def serialize(scrolls):
    """scrolls: dict {coord9 tuple: str} -> bytes, coordinates ascending."""
    out = bytearray()
    state = [1] * 9
    for coord in sorted(scrolls):
        target = list(coord)
        assert all(v >= 1 for v in target), coord
        for lvl in range(9):
            while state[lvl] < target[lvl]:
                out.append(LEVEL_BYTES[lvl])
                state[lvl] += 1
                for j in range(lvl + 1, 9):
                    state[j] = 1
        assert state == target, (state, target)
        text = scrolls[coord]
        assert not any(b in text.encode() for b in LEVEL_BYTES if b != 0x0A)
        out += text.encode()
    return bytes(out)


def parse(data):
    """bytes -> dict {coord9 tuple: str} (every scroll, including empty ones)."""
    scrolls = {}
    state = [1] * 9
    buf = bytearray()
    for byte in data:
        lvl = _BYTE_TO_LEVEL.get(byte)
        if lvl is None:
            buf.append(byte)
        else:
            scrolls[tuple(state)] = buf.decode()
            buf = bytearray()
            state[lvl] += 1
            for j in range(lvl + 1, 9):
                state[j] = 1
    scrolls[tuple(state)] = buf.decode()
    return scrolls


def common_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n
