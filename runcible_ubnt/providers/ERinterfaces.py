from runcible.providers.provider_array import ProviderArrayBase
from runcible.modules.ethernet_interfaces import EthernetInterfaces
from runcible.modules.ethernet_interface import EthernetInterface
from runcible_ubnt.providers.ERinterface import UBNTERInterfaceProvider


class UBNTEREthernetInterfacesProvider(ProviderArrayBase):
    provides_for = EthernetInterfaces
    sub_module_provider = UBNTERInterfaceProvider

    def _create_module(self, need):
        pass

    def get_cstate(self):
        interfaces = EthernetInterfaces({})
        config = self.device.retrieve('configuration')
        interface_dict = config.get('interfaces', {})
        if interface_dict:
            ethernet_interface_dict = interface_dict.get('ethernet', {})
        else:
            ethernet_interface_dict = {}
        for key, value in ethernet_interface_dict.items():
            interfaces.ethernet_interfaces.append(UBNTERInterfaceProvider.get_cstate(key, value))

        return interfaces


