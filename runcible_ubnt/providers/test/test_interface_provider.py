import unittest
from unittest.mock import Mock
from runcible.core.test_utilities import append_operation_test_cases
from runcible_ubnt.providers.ERinterfaces import UBNTEREthernetInterfacesProvider

system_dict = {}
device = Mock()
prov = UBNTEREthernetInterfacesProvider(device, {})


def send_command(command):
    if 'show interfaces ethernet' in command:
        return []


device.send_command = send_command


class TestInterfaceNeedCompletion(unittest.TestCase):
    longMessage = True

append_operation_test_cases(prov, system_dict, TestInterfaceNeedCompletion)