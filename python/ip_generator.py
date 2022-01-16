#!/usr/bin/python
import json
import sys
import tabulate
"""
This file is used to generate ip addresses for a given router.
"""

def read_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def write_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def generate_ip_topology(topology_file):
    ip_base = "10.0.{}.{}"
    netmask = "255.255.255.0"
    loopback_netmask = "255.255.255.255"
    subdomain = 1

    data_json = read_data(topology_file)

    # pour chaque routeur, parcourir ses interfaces et y associer une adresse IP
    for router in data_json.keys():
        # récupérer le numéro de router
        num_router_act = int(router[1:])

        # pour chaque interface
        for interface in data_json[router]["interfaces"]:
            if "neighbor" in data_json[router]["interfaces"][interface]:
                # récupérer les informations sur le voisin
                router_neighbor = data_json[router]["interfaces"][interface]["neighbor"]
                router_neighbor_interface = router_neighbor["interface"]
                router_neighbor_name = router_neighbor["name"]
                num_router_neighbor = int(router_neighbor["name"][1:])

                if len(data_json[router]["interfaces"][interface]["ip"]) == 0:
                    # configurer ip_address et mask du routeur actuel
                    data_json[router]["interfaces"][interface]["ip"]["ip_address"] = ip_base.format(subdomain, num_router_act)
                    data_json[router]["interfaces"][interface]["ip"]["mask"] = netmask
                    
                    # configurer ip_address et mask du routeur voisin
                    data_json[router_neighbor_name]["interfaces"][router_neighbor_interface]["ip"]["ip_address"] = ip_base.format(subdomain, num_router_neighbor)
                    data_json[router_neighbor_name]["interfaces"][router_neighbor_interface]["ip"]["mask"] = netmask

                    # incrémenter le numéro de subdomain
                    subdomain += 1

        # ajout de la loopback
        data_json[router]["interfaces"]["Loopback0"] = {}
        data_json[router]["interfaces"]["Loopback0"]["ip"] = {}
        data_json[router]["interfaces"]["Loopback0"]["ip"]["ip_address"] = "{0}.{0}.{0}.{0}".format(num_router_act)
        data_json[router]["interfaces"]["Loopback0"]["ip"]["mask"] = loopback_netmask

    return data_json

if __name__ == '__main__':
    # Read the command requirements from the command.json file
    filename = sys.argv[1]
    # topology = matrix_topology(read_data(filename))
    # Create the API to generate the GNS3 configurations command
    # print(get_ip_topology(filename))

    data_json = generate_ip_topology(filename)

    write_data(filename, data_json)
    