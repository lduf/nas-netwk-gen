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
    i = 1
    for router in ip_topology:
        print("Router {}".format(i))
        i+=1
        for neighbor in router:
            commands = config.get_commands("ip_address", neighbor)
            print(commands)

print(config.get_commands_parameters("ospf"))