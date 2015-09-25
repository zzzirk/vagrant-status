import subprocess
from collections import defaultdict
from .vstat import VagrantStatus


def main():
    vp = subprocess.Popen(["vagrant", "global-status"], stdout=subprocess.PIPE)

    stats = defaultdict(list)
    for status in VagrantStatus(vp.stdout):
        stats[status.project].append(status)

    for key in sorted(stats.keys()):
        value = stats[key]
        nextkey = key
        for v in value:
            print("{:20}{:10}{}".format(nextkey, v, v.state))
            if nextkey == key:
                nextkey = ""


if __name__ == '__main__':
    main()
