import ip_generator
import config
import json
import re

def read_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def routeur_number(routeur_string):
    return re.findall(r'R(\d+)', routeur_string)[0]


if __name__ == '__main__':
    topology = read_data("topology.json")
    ip_topology = ip_generator.get_ip_topology("topology.json")
    
    for router in topology:
        R = routeur_number(router)
        for neighbor in router:
           config.get_commands("ip_address", {"mask" : "255.255.255.0", "ip_address" : neighbor["ip"], "interface_name" : neighbor["interface"]})

    print(ip_topology)