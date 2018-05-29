# Get the mididings and OSC stuffs
from mididings import *
from mididings.extra.osc import SendOSC
from mididings.extra import *

# Set up the OSC port 
#(you define it in non-mixer thanks to  "--osc-port=7587" option - no quotes)
port = 9769
#The actual conversion stuff
run(
   Filter(CTRL) >> CtrlSplit({
       # Non-mixer maping
       #It's always : /strip/[strip_name]/[effect_name]/[control_name]
       #Non-mixer uses values from 0.0 to 1.0. Therfore you have to divide by 127
       # Caution : 127.0 ( .0 !!). Check 'python's promotion' if you want to know why.

       # In Gain
       1: SendOSC(port, '/strip/In1/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       2: SendOSC(port, '/strip/In2/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       3: SendOSC(port, '/strip/In3/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       4: SendOSC(port, '/strip/In4/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       5: SendOSC(port, '/strip/In5/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       6: SendOSC(port, '/strip/In6/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       7: SendOSC(port, '/strip/In7/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       8: SendOSC(port, '/strip/In8/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       # In Mute
       65: SendOSC(port, '/strip/In1/Gain/Mute', lambda ev: ev.value / 127.0),
       66: SendOSC(port, '/strip/In2/Gain/Mute', lambda ev: ev.value / 127.0),
       67: SendOSC(port, '/strip/In3/Gain/Mute', lambda ev: ev.value / 127.0),
       68: SendOSC(port, '/strip/In4/Gain/Mute', lambda ev: ev.value / 127.0),
       69: SendOSC(port, '/strip/In5/Gain/Mute', lambda ev: ev.value / 127.0),
       70: SendOSC(port, '/strip/In6/Gain/Mute', lambda ev: ev.value / 127.0),
       71: SendOSC(port, '/strip/In7/Gain/Mute', lambda ev: ev.value / 127.0),
       72: SendOSC(port, '/strip/In8/Gain/Mute', lambda ev: ev.value / 127.0),
       # In Aux 1 send
       81: SendOSC(port, '/strip/In1/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),
       82: SendOSC(port, '/strip/In2/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),
       83: SendOSC(port, '/strip/In3/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),
       84: SendOSC(port, '/strip/In4/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),
       85: SendOSC(port, '/strip/In5/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),
       86: SendOSC(port, '/strip/In6/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),
       87: SendOSC(port, '/strip/In7/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),
       88: SendOSC(port, '/strip/In8/Aux%20(A)/Gain%20(dB)', lambda ev: ev.value / 127.0),

       # Bus Gain
       9: SendOSC(port, '/strip/Bus1/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       10: SendOSC(port, '/strip/Bus2/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       11: SendOSC(port, '/strip/Bus3/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       12: SendOSC(port, '/strip/Bus4/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       13: SendOSC(port, '/strip/Bus5/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       14: SendOSC(port, '/strip/Bus6/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       15: SendOSC(port, '/strip/Bus7/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
       16: SendOSC(port, '/strip/Bus8/Gain/Gain%20(dB)', lambda ev: ev.value / 127.0),
      
   })
)
