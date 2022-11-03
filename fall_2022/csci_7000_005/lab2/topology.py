"""
Topology to simulate BGP hijack
"""

from seedemu.layers import Base, Routing, Ebgp, Ibgp, Ospf, PeerRelationship
from seedemu.services import WebService
from seedemu.compiler import Docker
from seedemu.core import Emulator
from seedemu.raps import OpenVpnRemoteAccessProvider
from seedemu.utilities import Makers

###############################################################################

emu     = Emulator()
base    = Base()
routing = Routing()
ebgp    = Ebgp()
ibgp    = Ibgp()
ospf    = Ospf()
web     = WebService()
ovpn    = OpenVpnRemoteAccessProvider()

###############################################################################

ix100 = base.createInternetExchange(100)
ix101 = base.createInternetExchange(101)
ix102 = base.createInternetExchange(102)
ix103 = base.createInternetExchange(103)

# Customize names (for visualization purpose)
ix100.getPeeringLan().setDisplayName('India-100')
ix101.getPeeringLan().setDisplayName('USA-101')
ix102.getPeeringLan().setDisplayName('UK-102')
ix102.getPeeringLan().setDisplayName('Australia-103')

###############################################################################
# Create Transit Autonomous Systems 

## Tier 1 ASes
Makers.makeTransitAs(base, 2, [100, 101, 102], 
       [(100, 101), (100, 102)] 
)

Makers.makeTransitAs(base, 3, [103, 101, 102], 
       [(103, 101), (103, 102)]
)

###############################################################################
# Create single-homed stub ASes 

Makers.makeStubAs(emu, base, 150, 100, [web, None])
Makers.makeStubAs(emu, base, 151, 100, [None, None])

Makers.makeStubAs(emu, base, 152, 101, [web, None])
Makers.makeStubAs(emu, base, 153, 101, [None, None])

Makers.makeStubAs(emu, base, 154, 102, [web, None])
Makers.makeStubAs(emu, base, 155, 102, [None, None])

Makers.makeStubAs(emu, base, 156, 103, [web, None])
Makers.makeStubAs(emu, base, 157, 103, [None, None])

###############################################################################
# Peering 

ebgp.addRsPeers(100, [2])
ebgp.addRsPeers(101, [2, 3])
ebgp.addRsPeers(102, [2, 3])
ebgp.addRsPeers(103, [3])

ebgp.addPrivatePeerings(100, [2],  [150, 151], PeerRelationship.Provider)
ebgp.addPrivatePeerings(101, [2, 3],  [152, 153], PeerRelationship.Provider)
ebgp.addPrivatePeerings(102, [2, 3],  [154, 155], PeerRelationship.Provider)
ebgp.addPrivatePeerings(103, [3],  [156, 157], PeerRelationship.Provider)

###############################################################################

# Create a new AS as the BGP attacker 
as199 = base.createAutonomousSystem(199)
as199.createNetwork('net0')
as199.createHost('host-0').joinNetwork('net0')

# Attach it to ix-105 and peer with AS-2
as199.createRouter('router0').joinNetwork('net0').joinNetwork('ix100')
ebgp.addPrivatePeerings(100, [2],  [199], PeerRelationship.Provider)

###############################################################################

# Add layers to the emulator
emu.addLayer(base)
emu.addLayer(routing)
emu.addLayer(ebgp)
emu.addLayer(ibgp)
emu.addLayer(ospf)
emu.addLayer(web)

emu.dump('base-component.bin')

emu.render()
emu.compile(Docker(), './output')
