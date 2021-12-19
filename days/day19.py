import collections
import re
import itertools

def parse(inp):
    scanners = dict()

    for i, block in enumerate(inp.split('\n\n')):
        lines = block.splitlines()
        beacons = set()
        for line in lines[1:]:
            beacon = tuple(int(v) for v in line.split(','))
            beacons.add(beacon)
        scanners[i] = beacons
    return scanners


def rotations(v):
    for roll_index in range(6):
        yield v
        for turn_index in range(3):
            if roll_index % 2:
                # Rotate CW
                v = (-v[1],v[0],v[2])
            else:
                # Rotate CCW
                v = (v[1],-v[0],v[2])
            yield v
        # Roll forward
        v = (v[0], -v[2], v[1])

def vec_sub(v0, v1):
    return tuple(a-b for a, b in zip(v0, v1))

def vec_add(v0, v1):
    return tuple(a+b for a, b in zip(v0, v1))

def vec_dist(v0, v1):
    return sum(abs(a-b) for a, b in zip(v0, v1))

def match_beacons(dst, src):
    match_count = collections.Counter()
    for dst_beacon, src_beacon in itertools.product(dst, src):
        offset = vec_sub(dst_beacon, src_beacon)
        match_count[offset] += 1

    offset, n = match_count.most_common(1)[0]
    if n >= 12:
        beacons = set(vec_add(offset, b) for b in src)
        return offset, beacons

    return None

def match_rotations(dst, src_rots):
    for src_rot in src_rots:
        match = match_beacons(dst, src_rot)
        if match:
            return match
    return None

def rotate_beacons(src):
    src_rots = [list() for _ in range(24)]
    for src_beacon in src:
        for idx, beacon in enumerate(rotations(src_beacon)):
            src_rots[idx].append(beacon)
    return src_rots

def search_scanners(scanners):
    found = {0: scanners[0]}
    offsets = {0: (0,0,0)}

    lost = dict()
    for scanner, beacons in scanners.items():
        if scanner in found:
            continue
        lost[scanner] = rotate_beacons(beacons)

    while lost:
        for dst in list(found.keys()):
            for scanner, rotations in lost.items():
                match = match_rotations(found[dst], rotations)
                if match:
                    break
            else:
                continue

            offset, beacons = match
            found[scanner] = beacons
            offsets[scanner] = offset
            del lost[scanner]

    return found, offsets


def part1(scanners):
    found, _ = search_scanners(scanners)

    beacons = set()
    for found_beacons in found.values():
        beacons |= found_beacons
    return len(beacons)

def part2(scanners):
    _, offsets = search_scanners(scanners)

    dists = []
    offsets = list(offsets.values())
    for v0, v1 in itertools.product(offsets, repeat=2):
        dist = vec_dist(v0, v1)
        dists.append(dist)
    return max(dists)
