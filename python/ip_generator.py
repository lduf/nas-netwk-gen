#!/usr/bin/python
import json
import sys
"""
This file is used to generate ip addresses for a given router.
"""



def read_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

"""
@brief: This function is used to convert the json topology into the topology matrix.
@param: param_topology: The topology to be converted.
@return: The topology matrix [N*N].

@example:
    {
        "R1" : {
            "R2" : "gigabitEthernet 1/0"
        },
        "R2" : {
            "R1" : "fastEthernet 1/0"
        }
    }

    returns:
    
    [ l0/0 ; gigabitEthernet 1/0 ]
    [ fastEthernet 1/0 ; l0/0]

"""
def matrix_topology(param_topology):
    # initialize the matrix with NxN size
    N = len(param_topology)
    return [["l0/0" if x ==y else param_topology["R{}".format(y+1)]["R{}".format(x+1)] for x in range(N)] for y in range(N)]


def generate_ip(matrix_topology):
    ip_base = "10.0.{}.{}"
    netmask = "255.255.255.0"
    for router in matrix_topology:
        for neighbor in router:
            print("{} {} {}".format(ip_base.format(router.index(neighbor)+1), neighbor, netmask))

def main():
    # Read the command requirements from the command.json file
    topology = matrix_topology(read_data(sys.argv[1]))
    # Create the API to generate the GNS3 configurations command
    print(topology)
if __name__ == '__main__':
    main()
