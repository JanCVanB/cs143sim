"""This file contains all constant definitions

.. moduleauthor:: Lan Hongjian <lanhongjianlr@gmail.com>
.. moduleauthor:: Yamei Ou <oym111@gmail.com>
.. moduleauthor:: Samuel Richerd <dondiego152@gmail.com>
.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
.. moduleauthor:: Junlin Zhang <neicullyn@gmail.com>
"""

DEBUG = False
#DEBUG = False
"""Whether to run the simulation in debug mode, with extra print statements"""

PACKET_SIZE = 8192
"""Size of every :class:`.Packet` in the simulation, in bits"""

ACK_PACKET_SIZE = 512
"""Size of every :class:`.Packet` in the simulation, in bits"""

ROUTER_PACKET_SIZE = 512
"""Size of every :class:`.RouterPacket` in the simulation, in bits"""

GENERATE_ROUTERPACKET_TIME_INTEVAL = 1000
"""Time for every :class:`.Router` to wait before generating a new
:class:`.RouterPacket`, in milliseconds"""

DYNAMICH_ROUTE_DISTANCE_METRIC = True
"""Whether to take dynamic link delay as the metric for route distance, 
otherwise use hops(topology) to be the metric"""

INPUT_FILE_RATE_SCALE_FACTOR = 1000000/1000.0
""" Conversion factor for Mbps to bits per millisecond (for rate)"""

INPUT_FILE_DATA_SCALE_FACTOR = 8000000
"""Conversion factor for MBytes to bits (for flow total data size)"""

INPUT_FILE_TIME_SCALE_FACTOR = 1000
"""Conversion factor for seconds to milliseconds (for flow start time)"""

INPUT_FILE_BUFFER_SCALE_FACTOR = 8000
"""Conversion factor for KB to bits (for buffer size)"""

OUTPUT_BUFFER_OCCUPANCY_SCALE_FACTOR = 1.0 / PACKET_SIZE
"""Conversion factor for bits to packets"""
OUTPUT_FLOW_RATE_SCALE_FACTOR = 1000.0/1000000
""" Conversion factor for bits per millisecond (for rate) to Mbps"""
