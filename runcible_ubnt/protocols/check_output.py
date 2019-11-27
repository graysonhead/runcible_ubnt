from runcible.core.errors import RuncibleExecutionError


def check_output_for_errors(command, lines):
    for line in lines:
        if 'exit discard' in line.lower() :
            raise RuncibleExecutionError(f"Command {command} appears to have failed: {lines}")