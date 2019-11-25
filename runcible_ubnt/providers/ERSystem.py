from runcible.modules.system import System, SystemResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


# Map the values returned by the vyos parser to their respective values in the runcible interface
attribute_map = {
    "host-name": SystemResources.HOSTNAME
}


class UBNTERSystemProvider(ProviderBase):
    """
    The only two methods that a provider needs to provide are get_cstate (which fetches the current state of the
    module's attributes on the target device. And the fix_needs method, which takes the need objects provided by the
    parent class and fixes them.
    """
    provides_for = System

    supported_attributes = [
        SystemResources.HOSTNAME
    ]

    def get_cstate(self):
        """
        Gets current state of all attributes in the module on target device
        :returns:
            Module instance
        """

        config_dict = {}
        # Get the config from the device KV store
        config = self.device.retrieve('configuration')
        system_dict = config.get('system', {})
        for key, value in system_dict.items():
            if key in attribute_map:
                config_dict.update({attribute_map[key]: value})
        return System(config_dict)

    def _set_hostname(self, hostname):
        return self.device.send_command(f"set system host-name {hostname}")

    def fix_needs(self):
        for need in self.needed_actions:
            if need.attribute is SystemResources.HOSTNAME:
                if need.operation is Op.SET:
                    self._set_hostname(need.value)
                    self.complete(need)
