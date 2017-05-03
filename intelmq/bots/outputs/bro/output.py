# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys

# imports for additional libraries and intelmq
from intelmq.lib.bot import Bot

"""
Writing Bro translation

intelmq name            | VAST type
------------------------+---------------------
raw                     | -
classification.type     | string
time.observation        | time
source.asn              | count
event_description.text  | string
source.network          | subnet
feed.name               | string
protocol.application    | string
feed.accuracy           | count
feed.url                | string
source.ip               | addr
"""

class BroBot(Bot):
    entries = {"classification.type"    : "string",
               "time.observation"       : "time",
               "source.asn"             : "count",
               "event_description.text" : "string",
               "source.network"         : "subnet",
               "feed.name"              : "string",
               "protocol.application"   : "string",
               "feed.accuracy"          : "count",
               "feed.url"               : "string",
               "source.ip"              : "addr"}

    header = """#separator \x09
                #set_separator	,
                #empty_field	(empty)
                #unset_field	-
                #path	blacklist
                #open	2014-05-23-18-02-04
             """

    def init(self):
        self.logger.debug("Opening %r file." % self.parameters.file)
        self.file = io.open(self.parameters.file, mode='at', encoding="utf-8")
        self.logger.info("File %r is open." % self.parameters.file)
        try:
            self.file.write(header)
            fields = "#fields"
            types = "#types"
            for f, t in entries:
                fields += "\t" + f
                types += "\t" + t
            self.file.write(fields)
            self.file.write("\n")
            self.file.write(types)
            self.file.write("\n")
            self.flush()

        except FileNotFoundError;
            self.logger.info("Failed to open %r." % self.parameters.file)

    def process(self):
        event = self.receive_message()
        event_dict = event.to_dict(hierarchical=False)
        line = ""
        for e,_ in entries:
            if e in event_dict:
                line += "\t"
            else
                line += "\t-"
        try:
            self.file.write(line)
            self.file.write("\n")
            self.file.flush()
        except FileNotFoundError:
            self.init()
        else:
            self.acknowledge_message()


BOT = BroBot
