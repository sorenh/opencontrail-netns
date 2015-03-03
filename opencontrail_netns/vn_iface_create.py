"""
This script creates and configures an interface connected
to a virtualized network.
"""

import argparse
import socket
import sys

from instance_provisioner import Provisioner
from host_manager import HostManager
from vrouter_control import interface_register


def build_network_name(project_name, network_name):
    if network_name.find(':') >= 0:
        return network_name
    return "%s:%s" % (project_name, network_name)


def iface_create():
    """
    Creates a virtual-machine and vmi object in the API server.
    Creates a veth interface pair.
    Associates the veth interface in the master instance with the vrouter.
    """
    parser = argparse.ArgumentParser()
    defaults = {
        'api-server': '127.0.0.1',
        'api-port': 8082,
        'project': 'default-domain:default-project',
    }
    parser.set_defaults(**defaults)
    parser.add_argument("-s", "--api-server", help="API server address")
    parser.add_argument("-p", "--api-port", type=int, help="API server port")
    parser.add_argument("--project", help="OpenStack project name")
    parser.add_argument("network", help="network to connect to")
    parser.add_argument("ifname", help="name of interface (will be created)")

    arguments = parser.parse_args(sys.argv[1:])

    ifname = arguments.ifname

    manager = HostManager()
    provisioner = Provisioner(api_server=arguments.api_server,
                              api_port=arguments.api_port)
    instance_name = '%s-%s' % (socket.gethostname(), ifname)
    vm = provisioner.virtual_machine_locate(instance_name)

    network = build_network_name(arguments.project, arguments.network)
    vmi = provisioner.vmi_locate(vm, network, ifname)

    ifname_master = manager.interface_update(ifname, vmi)
    interface_register(vm, vmi, ifname_master)

    ip_prefix = provisioner.get_interface_ip_prefix(vmi)
    manager.interface_config(ifname, ip_prefix)

# end iface_create


if __name__ == '__main__':
    iface_create()
