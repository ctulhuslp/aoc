import re
from collections import namedtuple
from datetime import datetime

Record = namedtuple('Record', ['timestamp', 'id', 'event'])


def parse_to_record(logline):
    timestamp, rest = logline[1:].split(']')
    return {'timestamp': datetime.strptime(timestamp, "%Y-%m-%d %H:%M"), 'id': 0, 'event': rest}


if __name__ == '__main__':
    with open('aoc4_inp.txt') as inp_file:
        inp = inp_file.read()
    records = [parse_to_record(i) for i in inp.strip().split("\n")]
    print(records[0])
    records.sort(key=lambda x: x['timestamp'])
    print(records[0])
    current_id = 0
    for record in records:
        if "#" in record['event']:
            current_id = int(re.findall(r'#+\d+', records[0]['event'])[0][1:])
        record['id'] = current_id
    print(records[0])

    # construct a dict with guard ids as rows and their sleep times as columns(?)
    # each minute from 00 to 59 is its own entry in a su
    # each date is a dict element in dict of a guard; the stuff inside is a dict of minutes, or maybe a set
    sleep_schedules = {}
    for record in records:
        start_sleep = 0
        if record['id'] in sleep_schedules:
            sleep_schedules[record['id']][record['timestamp'].strftime("%m-%d")] = set()
            if "wakes up" in record['event']:
                pass
            elif "falls asleep" in record['event']:
                start_sleep = record['timestamp'].minute

    # overlaps = set()
    # overlapping = set()
    # for i, claim1 in enumerate(inp_claims):
    #     for claim2 in inp_claims[i + 1:]:
    #         els = overlap_elements(claim1, claim2)
    #         if els:
    #             overlaps.update(els)
    #             overlapping.update([claim1.id, claim2.id])
    #
    # for i in inp_claims:
    #     if i.id not in overlapping:
    #         print(i)
