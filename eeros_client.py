#!/usr/bin/env python

from eeros_mock import EEROS

# fuer jeden User muss so ein Object erstellt werden, welches ueber alle Request hinweg am Leben bleibt
e = EEROS("/dev/eeduro") # pfad wird spaeter bestimmt


e.open() # einmal, wenn sich der User einloggt

seqName = "move"
params = []
print(e.sequences[seqName](params))
##print(e.signals.list())
##print(e.signals.subscribe("A", "B"))
##print(e.signals.get())
##print(e.signals.subscribe("A"))
##print(e.signals.get())
##print(e.signals.subscribe())
##
##
##print(e.events.list())
##print(e.events.trigger("e1"))
##print(e.events.trigger("x1"))
##
##
##print(e.log.get())
##
##
##print(e.levels.list())
##print(e.levels.current())
##
##
##print(e.sequences.list())
##print(e.sequences["move"](1.0, 2.0, 3.0))
##print(e.sequences.move(1.1, 2.2, 3.3))
##print(e.sequences["detect"]())
##
##seq = e.sequences["test"]
##if seq == None:
##	print("test() does not exist")
##else:
##	print("calling test()")
##	print(seq())


e.close() # wenn sich der User ausloggt

