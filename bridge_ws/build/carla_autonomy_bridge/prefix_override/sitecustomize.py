import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/a01004/Desktop/Calra-autoware_interface/bridge_ws/install/carla_autonomy_bridge'
