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


def matrix_topology(param_topology):
    """
        :brief This function is used to convert the json topology into the topology matrix.
        :param: param_topology: The topology to be converted.
        :return: The topology matrix [N*N].

        :example:
            {
                "R1" : {
                    "R2" : "GigabitEthernet1/0"
                },
                "R2" : {
                    "R1" : "FastEthernet1/0"
                }
            }

            returns:
            
            [ Loopback0 ; gigabitEthernet1/0 ]
            [ fastEthernet 1/0 ; Loopback0]

    """
    # initialize the matrix with NxN size
    N = len(param_topology)
    return [["Loopback0" if x ==y else param_topology["R{}".format(y+1)]["interfaces"]["R{}".format(x+1)] for x in range(N)] for y in range(N)]


def generate_ip(matrix_topology):
    N = len(matrix_topology)
    ip_base = "10.0.{}.{}"
    netmask = "255.255.255.0"
    ip_topology = [[0 for j in range(N)] for i in range(N)]
    ip_domains = [i+1 for i in range(int(N**2/2))]
    for router in range(N):
        for neighbor in range(router, N):
            if router == neighbor :
                ip_topology[router][neighbor] = "{}.{}.{}.{}".format(router+1, router+1, router+1, router+1)
            elif (matrix_topology[router][neighbor] != 0 ):
                subdom = ip_domains.pop(0)
                ip_topology[router][neighbor] = ip_base.format(subdom, router+1)
                ip_topology[neighbor][router] = ip_base.format(subdom, neighbor+1)
    return ip_topology
   
def get_ip_topology(topology_file):
    topology = matrix_topology(read_data(topology_file))
    ip_topology = generate_ip(topology)
    return [[{"interface" : topology[i][j], "ip" : ip_topology[i][j]} for j in range(len(ip_topology[i]))] for i in range(len(ip_topology))]

if __name__ == '__main__':
     # Read the command requirements from the command.json file
    topology = matrix_topology(read_data(sys.argv[1]))
    # Create the API to generate the GNS3 configurations command
    print(topology)
    print(generate_ip(topology))
    