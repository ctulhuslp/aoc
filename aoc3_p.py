from collections import namedtuple
from typing import List, Tuple


Claim = namedtuple('Claim', ['id', 'x', 'y', 'width', 'height'])

def parse_to_claim(line: str) -> Claim:
    id, rest = line.split(" @ ")
    xy, size = rest.split(": ")
    x, y = xy.split(',')
    width, height = size.split('x')
    return Claim(int(id[1:]), int(x), int(y), int(width), int(height))


def overlap_size(claim1: Claim, claim2: Claim) -> int:
    dx = min(claim1.x + claim1.width, claim2.x + claim2.width) - max(claim1.x, claim2.x)
    dy = min(claim1.y + claim1.height, claim2.y + claim2.height) - max(claim1.y, claim2.y)
    if dx >= 0 and dy >= 0:
        return dx * dy
    else:
        return 0


def overlap_elements(claim1: Claim, claim2: Claim) -> List[Tuple[int, int]]:
    leftmost_right = min(claim1.x + claim1.width, claim2.x + claim2.width)
    rightmost_left = max(claim1.x, claim2.x)
    topmost_bottom = min(claim1.y + claim1.height, claim2.y + claim2.height)
    bottommost_top = max(claim1.y, claim2.y)
    dx = min(claim1.x + claim1.width, claim2.x + claim2.width) - max(claim1.x, claim2.x)
    dy = min(claim1.y + claim1.height, claim2.y + claim2.height) - max(claim1.y, claim2.y)
    if dx >= 0 and dy >= 0:
        # should return list of (x, y) coords which are overlapping
        return [(x, y) for x in range(rightmost_left, leftmost_right) for y in range(bottommost_top, topmost_bottom)]
    else:
        return []


def test_overlap():
    claim1 = Claim(1, 1, 1, 4, 4)
    claim2 = Claim(2, 4, 4, 3, 3)
    print(overlap_size(claim1, claim2))
    assert overlap_size(claim1, claim2) == 1


def test_2():
    test_inp = """#1 @ 1,3: 4x4
                    #2 @ 3,1: 4x4
                    #3 @ 5,5: 2x2"""
    test_claims = [parse_to_claim(i.strip()) for i in test_inp.strip().split("\n")]
    agg2 = sum(overlap_size(claim1, claim2) for i, claim1 in enumerate(test_claims) for claim2 in test_claims[i + 1:])
    print(agg2)
    assert agg2 == 4


if __name__ == '__main__':
    with open('aoc3.txt') as inp_file:
        inp = inp_file.read()
    inp_claims = [parse_to_claim(i) for i in inp.strip().split("\n")]

    overlaps = set()
    overlapping = set()
    for i, claim1 in enumerate(inp_claims):
        for claim2 in inp_claims[i + 1:]:
            els = overlap_elements(claim1, claim2)
            if els:
                overlaps.update(els)
                overlapping.update([claim1.id, claim2.id])

    for i in inp_claims:
        if i.id not in overlapping:
            print(i)
