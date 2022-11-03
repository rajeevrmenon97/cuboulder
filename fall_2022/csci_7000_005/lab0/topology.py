"""
Cloud lab profile created by Rajeev Menon as part of Lab 0 
at CU Boulder's Advanced Network Systems class in Fall 2022
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Node node-0
node_0 = request.RawPC('node-0')
node_0.hardware_type = 'd710'
node_0.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
iface0 = node_0.addInterface('interface-0')

# Node node-1
node_1 = request.RawPC('node-1')
node_1.hardware_type = 'd710'
node_1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
iface1 = node_1.addInterface('interface-1')

# Node node-2
node_2 = request.RawPC('node-2')
node_2.hardware_type = 'd710'
node_2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD'
iface2 = node_2.addInterface('interface-2')

# Link link-0
link_0 = request.LAN('link-0')
iface0.bandwidth = 100000
link_0.addInterface(iface0)
iface1.bandwidth = 100000
link_0.addInterface(iface1)
iface2.bandwidth = 100000
link_0.addInterface(iface2)


# Print the generated rspec
pc.printRequestRSpec(request)
