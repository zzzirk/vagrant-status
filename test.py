"""
An few example blocks of the results of running a 'vagrant global-status'
command:

id       name   provider      state   directory
--------------------------------------------------------------------------
f3f2c96  search vmware_fusion running /Users/lzirkel/src/projects/cmdb
96d4335  db     vmware_fusion running /Users/lzirkel/src/projects/userweb
86a1585  web    vmware_fusion running /Users/lzirkel/src/projects/userweb
e9dd0b5  util   vmware_fusion running /Users/lzirkel/src/projects/audit
3a3935f  db     vmware_fusion running /Users/lzirkel/src/projects/cmdb
58b9b5c  web    vmware_fusion running /Users/lzirkel/src/projects/cmdb

"""

import unittest
import StringIO
from vstat.vstat import VagrantStatusFormat, VagrantStatus, VagrantStatusEntry


class VagrantStatusFormatTests(unittest.TestCase):
    def setUp(self):
        self.sample = """id       name   provider      state   directory"""

    def test_successful_instantiation(self):
        vfs = VagrantStatusFormat(self.sample)
        self.assertIsInstance(vfs, VagrantStatusFormat)

    def test_offset_values(self):
        vfs = VagrantStatusFormat(self.sample)
        self.assertIsNotNone(vfs.offset['id'])

    def test_valid_id_offset_values(self):
        vfs = VagrantStatusFormat(self.sample)
        self.assertIsNone(vfs.offset['id']['start'])
        self.assertIsInstance(vfs.offset['id']['end'], int)

    def test_valid_name_offset_values(self):
        vfs = VagrantStatusFormat(self.sample)
        self.assertIsInstance(vfs.offset['name']['start'], int)
        self.assertIsInstance(vfs.offset['name']['end'], int)

    def test_valid_provider_offset_values(self):
        vfs = VagrantStatusFormat(self.sample)
        self.assertIsInstance(vfs.offset['provider']['start'], int)
        self.assertIsInstance(vfs.offset['provider']['end'], int)

    def test_valid_state_offset_values(self):
        vfs = VagrantStatusFormat(self.sample)
        self.assertIsInstance(vfs.offset['state']['start'], int)
        self.assertIsInstance(vfs.offset['state']['end'], int)

    def test_valid_directory_offset_values(self):
        vfs = VagrantStatusFormat(self.sample)
        self.assertIsInstance(vfs.offset['directory']['start'], int)
        self.assertIsNone(vfs.offset['directory']['end'])


class VagrantStatusTests(unittest.TestCase):
    def setUp(self):
        self.sample = StringIO.StringIO("""id       name   provider      state   directory
--------------------------------------------------------------------------
f3f2c96  search vmware_fusion running /Users/lzirkel/src/projects/cmdb
96d4335  db     vmware_fusion running /Users/lzirkel/src/projects/userweb
86a1585  web    vmware_fusion running /Users/lzirkel/src/projects/userweb
e9dd0b5  util   vmware_fusion running /Users/lzirkel/src/projects/audit
3a3935f  db     vmware_fusion running /Users/lzirkel/src/projects/cmdb
58b9b5c  web    vmware_fusion running /Users/lzirkel/src/projects/cmdb
""")

    def test_successful_vagrant_status_instantiation(self):
        vfs = VagrantStatus(self.sample)
        self.assertIsInstance(vfs, VagrantStatus)

    def test_vagrant_status_generator(self):
        vfs = VagrantStatus(self.sample)
        self.assertIsInstance(vfs.next(), VagrantStatusEntry)


if __name__ == '__main__':
    unittest.main()
