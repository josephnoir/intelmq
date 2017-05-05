# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import io
import datetime
import dateutil.parser

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

    def init(self):
        self.logger.debug("Opening %r file." % self.parameters.file)
        self.file = io.open(self.parameters.file, mode='at', encoding="utf-8")
        self.logger.info("File %r is open." % self.parameters.file)
        try:

            self.file.write("#separator \\x09\n")
            self.file.write("#set_separator\t,\n")
            self.file.write("#empty_field\t(empty)\n")
            self.file.write("#unset_field\t-\n")
            self.file.write("#path\tblacklist\n")
            self.file.write("#open\t{}\n".format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
            fields = "#fields"
            types = "#types"
            for f, t in sorted(self.entries.items()):
                fields += "\t" + f
                types += "\t" + t
            self.file.write(fields)
            self.file.write("\n")
            self.file.write(types)
            self.file.write("\n")
            self.file.flush()

        except FileNotFoundError:
            self.logger.info("Failed to open %r." % self.parameters.file)

    def process(self):
        event = self.receive_message()
        event_dict = event.to_dict(hierarchical=False)
        line = ""
        for f,t in sorted(self.entries.items()):
            if line != "":
                line += '\t'
            if f in event_dict:
                if t == "time":
                    ts = event_dict[f]
                    dt = dateutil.parser.parse(ts)
                    line += dt.strftime('%s.0')
                else:
                    line += str(event_dict[f])
            else:
                line += '-'
        try:
            self.file.write(line)
            self.file.write("\n")
            self.file.flush()
        except FileNotFoundError:
            self.init()
        else:
            self.acknowledge_message()

    def shutdown(self):
        self.file.write("#close\t{}\n".format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
        io.close(self.file)
        self.logger.info("File %r is closed." % self.parameters.file)
        self.logger.info("Shutting down Bro bot.")


BOT = BroBot
