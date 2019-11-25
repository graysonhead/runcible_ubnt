from runcible.protocols.serial_protocol import SerialProtocol
from .check_output import check_output_for_errors
from runcible.core.errors import RuncibleNotConnectedError


class UBNTSerialProtocol(SerialProtocol):

    def send_implement(self, command):
        if self.client is None:
            raise RuncibleNotConnectedError("Activate with self.connect() before executing")
        self.client.write(f"{command}\r\n".encode('utf-8'))
        lines = self.client.readlines()
        decoded_lines = []
        for line in lines:
            decoded_lines.append(line.decode())
        check_output_for_errors(command, decoded_lines)
        return decoded_lines
