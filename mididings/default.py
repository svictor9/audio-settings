from mididings import *
from mididings.extra import *

# depend on additional python packages
from mididings.extra.osc import OSCInterface
from mididings.extra.inotify import AutoRestart

config(
    client_name = 'mididings',
    in_ports = [
        ('A30', 'system:midi_capture_1'),
        ('BCR', 'system:midi_capture_2'),
        ('arpIn', 'qmidiarp:out.*')
    ],
    out_ports = [
        # ('printdings', 'printdings:.*'),
        ('toYoshi', 'yoshimi:.*'),
        ('toArp', 'qmidiarp:in.*'),
        ('toHydrogen', 'hydrogen-midi:RX'),
        ('commonOut')
    ],    
    backend = 'jack',
)
hook(
    # some functions (like scene switching) can be controlled via OSC.
    # this is needed for the livedings GUI, for example.
    # by default, UDP port 56418 is used to control mididings, and mididings
    # will send notification to port 56419.
    # OSCInterface(),
    
    #restart automatically when script changes
    AutoRestart(),
)

# Remove continuous messages and bank changes sent by A-30
cleanA30 = PortFilter('A30') % -Filter(SYSRT_SENSING|SYSRT_CLOCK|PROGRAM) >> -CtrlFilter(0,32,91,93)

toYoshi = Port('toYoshi')
toArp =  Port('toArp')
toHydrogen = Port('toHydrogen')

commonRouting = [
    PortFilter('BCR') >> (toYoshi // toArp),
    PortFilter('arpIn') >> toYoshi,
    Filter(SYSRT_START,SYSRT_STOP) >> toHydrogen,
    Port('commonOut')
    ]

# return subscene for the A30 on specified channel.
# option to finger lower part of keyboard or send it just to arp
def ArpA30(channel, playLow):
    high = Output('toYoshi', channel)
    
    if playLow == True:
        low = [
            Filter(NOTE) >> Output('toArp'),
            Output('toYoshi', 1)
        ]
    else:
        low = Filter(NOTE) >> Output('toArp')
        
    return PortFilter('A30') >> ChannelSplit({
        1: high,
        16: low
    })

# return a list of 16 scenes, each routing to a different channel on the
# specified port
def yoshiSceneGroups():
    SceneGroups = dict()
    for c in range(1, 17):
        SceneGroups[c] = SceneGroup("Channel %d" % c, [
            Scene("Low Arp Only", [ArpA30(c, False), commonRouting]),
            Scene("Low Arp and Yoshi", [ArpA30(c, True), commonRouting]),
        ])
    return SceneGroups

# Make scenes for first 16 patches)
scenes = yoshiSceneGroups()

# Additional scenes
scenes[32] = Scene("A30 to Hydrogen", [
    PortFilter('A30') >> Port('toHydrogen')
])

# use the pre and post patches to print all incoming and outgoing events.
# pre also filters out program changes on the A30 (handled by the
# control patch 
pre = cleanA30 >> [Pass(), ~PortFilter('arpIn') >> Print('input', portnames='in')]

# post = PortSplit({
#     'A30': [Port('toYoshi'), Port('toArp')],
#     'BCR': [Port('toYoshi'), Port('toArp')]
# }) >> Print('output', portnames='out')

post = Print('output', portnames='out')
# post = Print('output', portnames='out')

# Use Program Change on the A30 to switch scenes
control = PortFilter('A30') >> [
    Filter(PROGRAM) >> ChannelFilter(1) >> SceneSwitch(),
    CtrlFilter(93) >> CtrlValueSplit(1, SubSceneSwitch(number=1), SubSceneSwitch(number=2)),
]

# split keyboard somewhere betmeen c2 and c3
# floatSplit = FloatingKeySplit('c2', 'c3', Channel(1), Channel(2))

# ...and start the whole thing...
run(
    control=control,
    pre=pre,
    post=post,
    scenes=scenes,
)
