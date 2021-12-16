#!/usr/bin/python
import json
import sys
import re
"""
This file is used to create the API to generate the GNS3 configurations command.
"""


"""
 @brief: This function is used to generate the GNS3 configurations command lines. It's a ±recursive function which calls
  all required_config function before returning the last command line.
 @param: command: The command to be executed.

"""
def execute(command):
    data = get_command()[command]
    if "required_config" in list(data):
        intermediary_command = []
        for i in range(len(data["required_config"])):
           # print("{} : {}".format(command, data["required_config"]))
            intermediary_command += execute(data["required_config"][i])
        return intermediary_command + data["command"]
    return data["command"]


def extract_parameters_from_command(regex, command):
    """
    Extract the parameters to ask to the router
    :param command: a command for a certain protocol or something similar
    :return: a set of parameters
    """
    # extract parameters from command string
    parameters = re.findall(regex, command)

    return set(parameters)


def replace_with_value(command):
    """
    :param command: a command with a modulable parameter. ex: router ospf {ospf_process_id}
    :return: the command with the modulable parameter replaced by its value
    """

    # replace with value(s)

    # return the command modified
    pass

def get_commands_parameters(regex, commands):
    parameters = set()
    for elem in commands:
        parameters |= extract_parameters_from_command(regex, elem)
    return parameters


def get_command():
    # Read the command requirements from the command.json file
    with open('command.json') as json_file:
        data = json.load(json_file)
        return data

if __name__ == '__main__':
    command_name = sys.argv[1]
    # Read the command requirements from the command.json file
    commands = execute(command_name)

    # get the parameters to modify for this command
    regex_command = r'\{(.*?)\}'
    parameters_command = get_commands_parameters(regex_command, commands)

    # generate the commands completed and return them

    # Create the API to generate the GNS3 configurations command
    print("Command name: {0}\nCommands for {0}: {1}\nParameters: {2}".format(command_name, commands, parameters_command))