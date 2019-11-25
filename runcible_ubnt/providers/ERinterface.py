from runcible.modules.ethernet_interface import EthernetInterface, EthernetInterfaceResources
from runcible.providers.sub_provider import SubProviderBase
from runcible.core.need import NeedOperation as Op
from ipaddress import ip_interface, IPv4Interface, IPv6Interface

SPEED_MAP = {
    # Maps VYOS speeds to Runcible speeds
    'auto',
    '100',
    '1000',
    '100000'
}


class UBNTERInterfaceProvider(SubProviderBase):
    supported_attributes = [
        EthernetInterfaceResources.MTU,
        EthernetInterfaceResources.IPV4_ADDRESSES,
        # EthernetInterfaceResources.DUPLEX
    ]
    provides_for = EthernetInterface

    @staticmethod
    def get_cstate(name: str, configuration: dict):
        config_dict = {}
        config_dict.update({'name': name})
        # IPV4 and IPV6 Addresses
        if 'address' in configuration:
            address_field = configuration.get('address')
            if type(address_field) is str:
                if address_field == 'dhcp':
                    config_dict.update({'ipv4_addresses': ['dhcp']})
                elif address_field == 'dhcpv6':
                    config_dict.update({'ipv6_addresses': ['dhcpv6']})
                elif type(ip_interface(address_field)) is IPv4Interface:
                    config_dict.update({'ipv4_addresses': [address_field]})
                elif type(ip_interface(address_field)) is IPv6Interface:
                    config_dict.update({'ipv6_addresses': [address_field]})
            elif type(address_field) is dict:
                v4_addresses = []
                v6_addresses = []
                for address in address_field.keys():
                    if address == 'dhcp':
                        v4_addresses.append('dhcp')
                    elif address == 'dhcpv6':
                        v6_addresses.append('dhcp')
                    elif type(ip_interface(address)) is IPv4Interface:
                        v4_addresses.append(address)
                    elif type(ip_interface(address)) is IPv6Interface:
                        v6_addresses.append(address)
                if v4_addresses:
                    config_dict.update({'ipv4_addresses': v4_addresses})
                if v6_addresses:
                    config_dict.update({'ipv6_addresses': v6_addresses})
        # Duplex and speed
        if 'duplex' in configuration:
            config_dict.update({EthernetInterfaceResources.DUPLEX: configuration.get('duplex')})
        return EthernetInterface(config_dict)

    def _add_ip_address(self, interface, address):
        return self.device.send_command(f'set interfaces ethernet {interface} address {address}')

    def _set_ip_addresses(self, interface, addresses):
        for address in addresses:
            self._add_ip_address(interface, address)

    def _clear_ipv4_addresses(self, interface):
        interface_lines = self.device.send_command(f'show interfaces ethernet {interface} address')
        delete_addresses = []
        for line in interface_lines:
            if line.strip().startswith('address'):
                address = line.strip().split(' ')[1]
                if address == 'dhcp':
                    delete_addresses.append(address)
                elif type(ip_interface(address)) is IPv4Interface:
                    delete_addresses.append(address)
        for address in delete_addresses:
            self._delete_ip_address(interface, address)

    def _delete_ip_address(self, interface, address):
        return self.device.send_command(f'delete interfaces ethernet {interface} address {address}')

    def _set_mtu(self, interface, mtu):
        return self.device.send_command(f'set interfaces ethernet {interface} mtu {mtu}')

    def fix_need(self, need):
        if need.attribute == EthernetInterfaceResources.MTU:
            if need.operation == Op.SET:
                self._set_mtu(need.module, need.value)
                self.complete(need)
        if need.attribute == EthernetInterfaceResources.IPV4_ADDRESSES:
            if need.operation == Op.SET:
                self._set_ip_addresses(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.CLEAR:
                self._clear_ipv4_addresses(need.module)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._delete_ip_address(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.ADD:
                self._add_ip_address(need.module, need.value)
                self.complete(need)