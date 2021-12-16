#!/usr/bin/python
import json
import sys
"""
This file is used to create the API to generate the GNS3 configurations command.
"""


"""
 @brief: This function is used to generate the GNS3 configurations command lines. It's a ±recursive function which calls all required_config function before returning the last command line.
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
    


def get_command():
    # Read the command requirements from the command.json file
    with open('command.json') as json_file:
        data = json.load(json_file)
        return data

def main():
    # Read the command requirements from the command.json file
    data = execute(sys.argv[1])
    # Create the API to generate the GNS3 configurations command
    print(data)

if __name__ == '__main__':
    main()

    