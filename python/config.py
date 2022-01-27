#!/usr/bin/python
import json
import sys
import re
import argparse

"""
This file is used to create the API to generate the GNS3 configurations command.
"""

parser = argparse.ArgumentParser(description='This script is used to get information about the commands')
parser.add_argument('-c', '--command', type=str, help='The command on which you want to get parameters list', metavar='')
args = parser.parse_args()

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


def extract_parameters_from_command(command, regex='\{(.*?)\}'):
    """
    Extract the parameters to ask to the router
    :param command: a command for a certain protocol or something similar
    :return: a set of parameters
    """
    # extract parameters from command string
    parameters = re.findall(regex, command)

    return set(parameters)

def replace_commands_with_values(commands, dict_args):
    for i in range(len(commands)):
        command = commands[i]
        command = replace_command_with_values(command, dict_args)
        commands[i] = command
    return commands

def replace_command_with_values(command, dict_args):
    """
    :param command: a command with a modulable parameter. ex: router ospf {ospf_process_id}
    :return: the command with the modulable parameter replaced by its value
    """
    # get the parameters
    params = extract_parameters_from_command(command)

    # replace with value(s)
    for param in params:
        p = '{' + param + '}'
        command = command.replace(p, dict_args[param])

    # return the command modified
    return command

def get_commands_parameters(command_name):
    commands = execute(command_name)
    parameters = set()

    for elem in commands:
        parameters |= extract_parameters_from_command(elem)
    return parameters

def get_command():
    # Read the command requirements from the command.json file
    with open('command.json') as json_file:
        data = json.load(json_file)
    return data

def get_commands(command_name, dict_args):
    commands_empty = execute(command_name)
    commands = replace_commands_with_values(commands_empty, dict_args)
    return commands

def get_command_list():
    """

    :return: toutes les commandes possibles lol
    """
    data = get_command()
    return data.keys()

if __name__ == '__main__':

    if args.command:
        # get the parameters to modify for this command
        parameters_command = get_commands_parameters(args.command)

        # Create the API to generate the GNS3 configurations command
        print("Command name: {0}\nParameters: {1}".format(args.command, parameters_command))