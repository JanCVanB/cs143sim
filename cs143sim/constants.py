"""
This file contains all constant definitions

.. moduleauthor:: Lan Hongjian <lanhongjianlr@gmail.com>
.. moduleauthor:: Yamei Ou <oym111@gmail.com>
.. moduleauthor:: Samuel Richerd <dondiego152@gmail.com>
.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
.. moduleauthor:: Junlin Zhang <neicullyn@gmail.com>
"""

DEBUG = False
PACKET_SIZE = 8192
GENERATE_ROUTERPACKET_TIME_INTEVAL = 20  #milliseconds


### INPUT FILE UNIT CONVERSIONS:
# Rate needs to go from Mbps to bits per millisecond (internally)
INPUT_FILE_RATE_SCALE_FACTOR = 1000000/1000.0
# Data (flow total data size) needs to go from MBytes to bits
INPUT_FILE_DATA_SCALE_FACTOR = 8000000
# Start time needs to go from seconds to milliseconds
INPUT_FILE_TIME_SCALE_FACTOR = 1000
# Buffer size goes from KB to Bytes
INPUT_FILE_BUFFER_SCALE_FACTOR = 1000
