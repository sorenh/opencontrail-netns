"""
Unconfigure the interface created by vn_iface_create
"""

import argparse
import socket
import sys

from instance_provisioner import Provisioner
from host_manager import HostManager
from vrouter_control import interface_unregister


def vn_iface_destroy():
    parser = argparse.ArgumentParser()
    defaults = {
        'api-server': '127.0.0.1',
        'api-port': 8082,
    }
    parser.set_defaults(**defaults)
    parser.add_argument("-s", "--api-server", help="API server address")
    parser.add_argument("-p", "--api-port", type=int, help="API server port")
    parser.add_argument("ifname", help="Interface name")
    arguments = parser.parse_args(sys.argv[1:])

    ifname = arguments.ifname

    manager = HostManager()
    provisioner = Provisioner(api_server=arguments.api_server,
                              api_port=arguments.api_port)
    instance_name = '%s-%s' % (socket.gethostname(), ifname)
    vm = provisioner.virtual_machine_lookup(instance_name)

    vmi_list = vm.get_virtual_machine_interfaces()
    for ref in vmi_list:
        uuid = ref['uuid']
        interface_unregister(uuid)

    manager.clear_interfaces(ifname)

    for ref in vmi_list:
        provisioner.vmi_delete(ref['uuid'])

    provisioner.virtual_machine_delete(vm)

# end vn_iface_destroy


if __name__ == '__main__':
    vn_iface_create()

