from collections import namedtuple, defaultdict
import os


StatusTuple = namedtuple('StatusTyple',
                         'token, hostname, provider, state, path')


class VagrantStatusEntry(object):
    def __init__(self, id, name, provider, state, directory):
        self.id = id
        self.name = name
        self.provider = provider
        self.state = state
        self.directory = directory

    def __str__(self):
        return self.id

    @property
    def project(self):
        return os.path.split(self.directory)[1]


class VagrantStatusFormat(object):
    KEYS = ['id', 'name', 'provider', 'state', 'directory']

    def __init__(self, format):
        self.offset = defaultdict(None)

        last_key = None
        for key in self.KEYS:
            self.offset[key] = {
                "start": None,
                "end": None
            }
            if last_key is not None:
                offset = format.find(key)
                self.offset[key]['start'] = offset
                self.offset[last_key]['end'] = offset - 1
            last_key = key


class VagrantStatus(object):
    def __init__(self, vfs):
        self.vfs = vfs
        self.format = VagrantStatusFormat(self.vfs.readline())
        self.vfs.readline()     # munch the divider line

    def __iter__(self):
        return self

    def next(self):
        while True:
            line = self.vfs.readline().strip()
            if len(line) == 0:
                raise StopIteration()
            args = []
            for key in VagrantStatusFormat.KEYS:
                start = self.format.offset[key]['start']
                end = self.format.offset[key]['end']
                args.append(line[start:end].strip())
            return VagrantStatusEntry(*args)


class StatusEntry(object):
    """
    A basic representation of a status line from running:

        $ vagrant global-status

    """
    def __init__(self, token, hostname, provider, state, path):
        self.token = token.strip()
        self.hostname = hostname.strip()
        self.provider = provider.strip()
        self.state = state.strip()
        self.path = path.strip()

    @property
    def project(self):
        return os.path.split(self.path)[1]

    def __repr__(self):
        return "<NewStatsEntry: {}>".format(self.token)

    def __str__(self):
        return "{}".format(self.token)

    @staticmethod
    def from_text(line):
        # RE_statline = re.compile("^(?P<token>.*?)\s+(?P<hostname>.*?)\s+"
        #                          "(?P<provider>.*?)\s+(?P<state>.*?)\s+"
        #                          "(?P<path>.*?)$")
        # m = RE_statline.match(r)
        # if m:
        #     e = StatusEntry.from_text(*m.groups())
        #     return e
        token = line[0:8].strip()
        hostname = line[8:15].strip()
        provider = line[15:29].strip()
        state = line[29:40].strip()
        path = line[40:].strip()
        return StatusEntry(token, hostname, provider, state, path)
