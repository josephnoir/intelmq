# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.bro.output import BroBot

class TestBroBot(test.BotTestCase, unittest.TestCase):

    header = """#separator \x09
                #set_separator	,
                #empty_field	(empty)
                #unset_field	-
                #path	blacklist
                #open	2014-05-23-18-02-04
             """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BroBot
        cls.os_fp, cls.filename = tempfile.mkstemp()
        cls.sysconfig = {"hierarchical_output": True,
                         "file": cls.filename}

    def test_event(self):
        self.run_bot()
        filepointer = os.fdopen(self.os_fp, 'rt')
        filepointer.seek(0)
        self.assertEqual(header, filepointer.read())
        filepointer.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)

if __name__ == '__main__': # pragma: no cover
    unittest.main()


