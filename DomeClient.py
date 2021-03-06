#!/usr/bin/env python
import sys, traceback, Ice, os
Ice.loadSlice("HinOTORI.ice")
import HinOTORI
from optparse import OptionParser
import config

status = 0

class DomeClient(Ice.Application):
	def run(self,args):
		self.args=args
		self.shutdownOnInterrupt()
		return self.DomeProcessor()

	def DomeProcessor(self):
		"""
		A class method to communicate with the dome.
		"""
		try:
			obj = self.communicator().stringToProxy("dome:default -h %s -p %d"
				 % ( \
						config.nodesetting["dome"]['ip'], \
						config.nodesetting["dome"]['port'] \
					))

			dome=HinOTORI.DomePrx.checkedCast(obj)

			if self.args[1] == "open":
				print "open"
				dome.slitOpen()

			elif self.args[1] == "close":
				print "close"
				dome.slitClose()

			else:
				print "no such command %s" % self.args[1]

			return 0
		except:
			raise


if __name__ == "__main__":
	app = DomeClient()
	status = app.main(sys.argv)
	sys.exit(status)

