import unittest
import math

class TestBits(unittest.TestCase):
    def test_iter_bits(self):
        it = iterate_bits('0')
        self.assertEqual(list(it), [False, False, False, False])

        it = iterate_bits('F')
        self.assertEqual(list(it), [True, True, True, True])

        it = iterate_bits('7A')
        self.assertEqual(list(it), [False, True, True, True, True, False,
            True, False])

    def test_take_bits(self):
        it = iterate_bits('F128')
        self.assertEqual(take_bits(it, 3), 7)
        self.assertEqual(take_bits(it, 5), 17)
        self.assertEqual(take_bits(it, 2), 0)
        self.assertEqual(take_bits(it, 2), 2)
        self.assertEqual(take_bits(it, 1), 1)

    def test_parse_literal(self):
        packet, length = parse('D2FE28')
        target = { 'version': 6, 'type_id': 4, 'value': 2021 }
        self.assertEqual(packet, target)
        self.assertEqual(length, 21)

    def test_parse_operator(self):
        packet, length = parse('38006F45291200')
        target = {
            'version': 1,
            'type_id': 6,
            'value': [
                {'version': 6, 'type_id': 4, 'value': 10 },
                {'version': 2, 'type_id': 4, 'value': 20 }
            ]
        }
        self.assertEqual(packet, target)
        self.assertEqual(length, 49)

        packet, length = parse('EE00D40C823060')
        target = {
            'version': 7,
            'type_id': 3,
            'value': [
                {'version': 2, 'type_id': 4, 'value': 1},
                {'version': 4, 'type_id': 4, 'value': 2},
                {'version': 1, 'type_id': 4, 'value': 3}
            ]
        }
        self.assertEqual(packet, target)
        self.assertEqual(length, 51)

    def test_count_version(self):
        packet, _ = parse('8A004A801A8002F478')
        self.assertEqual(count_version(packet), 16)

        packet, _ = parse('620080001611562C8802118E34')
        self.assertEqual(count_version(packet), 12)

        packet, _ = parse('C0015000016115A2E0802F182340')
        self.assertEqual(count_version(packet), 23)

        packet, _ = parse('A0016C880162017C3686B18A3D4780')
        self.assertEqual(count_version(packet), 31)

    def test_eval_packet(self):
        packet, _ = parse('C200B40A82')
        self.assertEqual(eval_packet(packet), 3)

        packet, _ = parse('04005AC33890')
        self.assertEqual(eval_packet(packet), 54)

        packet, _ = parse('880086C3E88112')
        self.assertEqual(eval_packet(packet), 7)

        packet, _ = parse('CE00C43D881120')
        self.assertEqual(eval_packet(packet), 9)

        packet, _ = parse('D8005AC2A8F0')
        self.assertEqual(eval_packet(packet), 1)

        packet, _ = parse('F600BC2D8F')
        self.assertEqual(eval_packet(packet), 0)

        packet, _ = parse('9C005AC2F8F0')
        self.assertEqual(eval_packet(packet), 0)

        packet, _ = parse('9C0141080250320F1802104A08')
        self.assertEqual(eval_packet(packet), 1)



def iterate_bits(s):
    for c in s:
        h = int(c, 16)
        for i in reversed(range(4)):
            yield bool(h & (1<<i))

def take_bits(bits, n):
    v = 0
    for _ in range(n):
        v <<= 1
        v |= next(bits)
    return v

def parse(inp):
    bits = iterate_bits(inp.strip())
    return parse_packet(bits)

def parse_packet(bits):
    version = take_bits(bits, 3)
    type_id = take_bits(bits, 3)

    if type_id == 4:
        value, length = parse_val_literal(bits)
    else:
        value, length = parse_val_operator(bits)

    packet = {
        'version': version,
        'type_id': type_id,
        'value': value
    }
    length += 6

    return packet, length

def parse_val_literal(bits):
    value = 0
    length = 0
    while True:
        is_last = not next(bits)
        value <<= 4
        value |= take_bits(bits, 4)
        length += 5
        if is_last:
            break
    return value, length

def parse_val_operator(bits):
    length = 1
    length_type = next(bits)
    value = []

    if length_type:
        length += 11
        n_sub = take_bits(bits, 11)
        for _ in range(n_sub):
            packet, sub_len = parse_packet(bits)
            value.append(packet)
            length += sub_len
    else:
        length += 15
        total_sub_len = take_bits(bits, 15)
        length += total_sub_len
        while total_sub_len:
            packet, sub_len = parse_packet(bits)
            value.append(packet)
            total_sub_len -= sub_len

    return value, length

def count_version(packet):
    count = packet['version']

    type_id = packet['type_id']
    value = packet['value']
    if type_id != 4:
        for sub_packet in value:
            count += count_version(sub_packet)
    return count

def eval_packet(packet):
    type_id = packet['type_id']
    value = packet['value']

    if type_id != 4:
        values = [eval_packet(p) for p in value]
        if type_id == 0:
            return sum(values)
        elif type_id == 1:
            return math.prod(values)
        elif type_id == 2:
            return min(values)
        elif type_id == 3:
            return max(values)
        elif type_id == 5:
            a, b = values
            return int(a > b)
        elif type_id == 6:
            a, b = values
            return int(a < b)
        elif type_id == 7:
            a, b = values
            return int(a == b)
    else:
        return value


def part1(inp):
    packet, _ = inp
    return count_version(packet)

def part2(inp):
    packet, _ = inp
    return eval_packet(packet)
