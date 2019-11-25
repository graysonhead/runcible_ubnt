import vyattaconfparser
from runcible.drivers.driver import DriverBase
from runcible.protocols import SerialProtocol
from runcible_ubnt.protocols.ubnt_interactive_ssh import UBNTInteractiveSSH
from runcible_ubnt.providers.ERSystem import UBNTERSystemProvider
from runcible_ubnt.providers.ERinterfaces import UBNTEREthernetInterfacesProvider


class UBNTEdgeRouterDriver(DriverBase):
    """
    The driver is what associates providers to modules and assigns protocol classes.

    Additionally, the Driver can have the following methods that allow you to take preparation
    or cleanup steps:
    pre_plan_tasks
    post_plan_tasks
    pre_exec_tasks
    post_exec_tasks

    Each of these methods are passed the device instance when run, allowing you to
    use its methods to send commands or store key/value pairs
    """

    # The driver name is the key that a user would use to select the driver
    driver_name = "ubnt_edgerouter"

    # The provider map associates providers to modules
    module_provider_map = {
        "system": UBNTERSystemProvider,
        "ethernet_interfaces": UBNTEREthernetInterfacesProvider
    }
    # The protocol map maps protocols to identifier strings
    protocol_map = {
        "serial": SerialProtocol,
        "ssh": UBNTInteractiveSSH
    }

    # This method gets run before the device.plan() method is called
    @staticmethod
    def pre_plan_tasks(device):
        # Get the full configuration, then parse it and store it in the device key/value store so providers can
        # retrieve it
        raw_commands = device.send_command('show configuration | cat')
        first_line_index = None
        last_line_index = 0
        for line in raw_commands:
            if line.endswith('{') and not first_line_index:
                first_line_index = raw_commands.index(line)
            if line.strip() == '}':
                last_line_index = raw_commands.index(line, last_line_index + 1)
        conf_dict = vyattaconfparser.parse_conf('\n'.join(raw_commands[first_line_index:last_line_index]))
        device.store('configuration', conf_dict)

    @staticmethod
    def pre_exec_tasks(device):
        # Enter configuration mode before execution
        device.send_command('configure')

    # This method gets run after device.exec() completes its task, but before callbacks are rendered
    @staticmethod
    def post_exec_tasks(device):
        # These commands commit the changes, save them, and then close the configure terminal
        device.send_command('commit')
        device.send_command('save')
        device.send_command('exit')
