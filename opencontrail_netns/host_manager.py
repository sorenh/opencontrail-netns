import re
import subprocess
import sys

def shell_command(str):
    cmd = subprocess.check_output(str, shell=True)
    return cmd


class HostManager(object):
    def create_interface(self, ifname, vmi=None):
        ifname_master = self._get_master_ifname(ifname)
        shell_command('ip link add %s type veth peer name %s' %
                      (ifname, ifname_master))
        if vmi:
            mac = vmi.virtual_machine_interface_mac_addresses.mac_address[0]
            shell_command('ifconfig %s hw ether %s' % (ifname, mac))

        shell_command('ip link set %s up' % ifname_master)
        return ifname_master

    def _interface_list_contains(self, output, iface):
        for line in output.split('\n'):
            m = re.match(r'[\d]+: ' + iface + ':', line)
            if m:
                return True
        return False

    def _get_master_ifname(self, ifname):
        return '%sm' % ifname

    def interface_update(self, ifname, vmi):
        """
        1. Make sure that the interface exists in the name space.
        2. Update the mac address.
        """
        output = shell_command('ip link list')
        if not self._interface_list_contains(output, ifname):
            ifname_master = self.create_interface(ifname, vmi)
        else:
            ifname_master = self._get_master_ifname(ifname)

        mac = vmi.virtual_machine_interface_mac_addresses.mac_address[0]
        shell_command('ifconfig %s hw ether %s' %
                      (ifname, mac))
        return ifname_master

    def interface_config(self, ifname, ip_prefix):
        """
        Once the interface is operational, configure the IP addresses.
        """
        shell_command('ip addr add %s/%d dev %s' %
                      (ip_prefix[0], ip_prefix[1], ifname))
        shell_command('ip link set %s up' % (ifname))

    def clear_interfaces(self, ifname):
        shell_command('ip link delete %s' % ifname)
