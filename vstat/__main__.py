import sys
import subprocess
from collections import defaultdict
from pprint import pprint
from .vstat import StatusEntry
from .vstat import VagrantStatus


def old_main():

    vp = subprocess.Popen(["vagrant", "global-status"], stdout=subprocess.PIPE)
    result = vp.stdout.read().split('\n')
    # print result
    stats = {}
    for r in result[2:]:
        if r == ' ':
            break
        e = StatusEntry.from_text(r)
        # m = RE_statline.match(r)
        # if m:
        #     e = StatusEntry.from_text(*m.groups())
        if e.project not in stats:
            stats[e.project] = []
        stats[e.project].append(e)

    for key, value in stats.iteritems():
        nextkey = key
        for v in value:
            print("{:16}{:10}{}".format(nextkey, v, v.state))
            if nextkey == key:
                nextkey = ""


def main():
    vp = subprocess.Popen(["vagrant", "global-status"], stdout=subprocess.PIPE)

    stats = defaultdict(list)
    for status in VagrantStatus(vp.stdout):
        stats[status.project].append(status)

    # pprint(stats)
    # sys.exit(0)

    for key in sorted(stats.keys()):
        value = stats[key]
        nextkey = key
        for v in value:
            print("{:16}{:10}{}".format(nextkey, v, v.state))
            if nextkey == key:
                nextkey = ""


if __name__ == '__main__':
    main()
