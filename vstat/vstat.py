from collections import namedtuple
import os


StatusTuple = namedtuple('StatusTyple',
                         'token, hostname, provider, state, path')


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
