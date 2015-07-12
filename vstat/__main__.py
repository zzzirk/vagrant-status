import subprocess
import re
from .vstat import StatusEntry


def main():

    RE_statline = re.compile("^(?P<token>.*?)\s+(?P<hostname>.*?)\s+"
                             "(?P<provider>.*?)\s+(?P<state>.*?)\s+"
                             "(?P<path>.*?)$")

    vp = subprocess.Popen(["vagrant", "global-status"], stdout=subprocess.PIPE)
    result = vp.stdout.read().split('\n')
    # print result
    stats = {}
    for r in result[2:]:
        if r == ' ':
            break
        m = RE_statline.match(r)
        if m:
            e = StatusEntry(*m.groups())
        if e.project not in stats:
            stats[e.project] = []
        stats[e.project].append(e)

    for key, value in stats.iteritems():
        nextkey = key
        for v in value:
            print("{:16}{:10}{}".format(nextkey, v, v.state))
            if nextkey == key:
                nextkey = ""


if __name__ == '__main__':
    main()
