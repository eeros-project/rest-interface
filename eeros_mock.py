#!/usr/bin/env python

class Signals:
	eeros = None
	signals = {"SignalA": "Nm",
                   "SignalB": "A",
                   "SignalC": "V",
                   "SignalD": "m",
                   "SignalE": "kg",
                   "Test": "unit"
                   }
	
	values = {      "SignalA": [ (403501000010, 1), (403502000020, 2), (403503000033, 3), (403504000001, 4), (403505000005, 5) ],
			"SignalB": [ (403501000000, 5.5), (403502000025, 0.0), (403503000002, 0.0), (403504000009, 1.2), (403505000001, 0.0) ]
                 }

	def __init__(self, eeros):
		self.eeros = eeros

	def list(self):
		print("getting list of signals")
		return self.signals

	def subscribe(self, *keys):
		if keys:
			print("subscribing to signals: " + str(keys))
			return keys

		else:
			print("unsubscribing all signals")
			return []

	def get(self):
		print("getting signals")
		return self.values

class Events:
	eeros = None
	events = {	"e1": "event 1 description", 
			"e2": "event 2 description",
			"e3": "event 3 description" }

	def __init__(self, eeros):
		self.eeros = eeros

	def list(self):
		print("getting list of events")
		return self.events

	def trigger(self, name):
		if name in self.events:
			print("triggering event: " + name)
			return True
		else:
			print("unknown event: " + name)
			return False

class Levels:
	eeros = None
	levels = [	["l1", "level 1 description" ], 
			["l2", "level 2 description" ],
			["l3", "level 3 description" ] ]
	index = 0

	def __init__(self, eeros):
		self.eeros = eeros

	def list(self):
		print("getting safety levels")
		return self.levels[:]

	def current(self):
		print("getting current safety level")
		return self.levels[self.index]

class Sequences:
	eeros = None
	sequences = {
		"move": {
			"description": "moves the robot to position (x,y,z)",
			"param": [	["int", "x"],
					["double", "y"],
					["double", "z"] ],
			"return": "bool"
		},
		"detect": {
			"description": "detects if a block is on the current position",
			"return": "double"
		},
		"grab": {
			"description": "grabs the block (activates the magnet)"
		},
		"release": {
			"description": "releases the block (deactivates the magnet)"
		},
#		"test": { "description": "grabs the block (activates the magnet)" }
	}

	def __init__(self, eeros):
		self.eeros = eeros

	def list(self):
		print("getting list of sequences")
		return self.sequences

	def call(self, s, *args, **kwargs):
		print("calling sequence: " + str(s))
		print("    with args: " + str(args))
	#	return None
                return "calling sequence: " + str(s)
#		raise Exception("sequence failed")

	def __getitem__(self, key):
		if key in self.sequences:
			return lambda *args: self.call(self.sequences[key], *args)
		else:
			return None

	def __getattr__(self, name):
		method = self.__getitem__(name)
		if method != None: return method
		else: raise AttributeError

class Log:
	eeros = None

	def __init__(self, eeros):
		self.eeros = eeros

	def get(self):
		print("reading log messages")
		return [ ["2014-11-29", "C", 5, "message 1"],
			 ["2014-11-29", "C", 1, "message 2"],
                         ["2014-11-30", "A", 3, "message 3"],
			 ["2014-11-30", "B", 7, "message 4"],
                         ["2014-11-31", "D", 8, "message 3"],
			 ["2014-11-31", "E", 9, "message 4"],                         
			 ["2014-11-31", "D", 0, "message 5"] ]
	

class EEROS:
	device = None
	signals = None
	events = None
	levels = None
	sequences = None
	log = None

	def __init__(self, device):
		self.device = device
		self.signals = Signals(self)
		self.events = Events(self)
		self.levels = Levels(self)
		self.sequences = Sequences(self)
		self.log = Log(self)

	def open(self):
		print("opening device: " + self.device)
		return True

	def close(self):
		print("closing device")

	def __enter__(self): self.open()
	def __exit__(self, exc_type, exc_value, traceback): self.close()


