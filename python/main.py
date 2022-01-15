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

def main():
    topology_file = "topology.json"

    # génération des IP (se fera seulement si certaiens interfaces n'ont pas d'IP affectées)
    ip_topology = ip_generator.generate_ip_topology(topology_file)

    for router in ip_topology:
        for interface in ip_topology[router]["interfaces"]:
            protocols_for_interface = []
            # récupérer pour chaque interface de chaque routeur la liste des protocoles activés
            if "protocols" in ip_topology[router]["interfaces"][interface]:
                protocols_for_interface = ip_topology[router]["interfaces"][interface]["protocols"]
                print(f"{router} : {interface} : {protocols_for_interface}")

                # faire appel à l'API de config pour récupérer la liste des commandes pour chaque protocol
                parameters_interface = ip_topology[router]["interfaces"][interface]["parameters"]
                for protocol in protocols_for_interface:
                    # en theorie on a un dict avec tous les paramètres possibles
                    # donc plus besoin de faire un premier appel API pour avoir la liste des paramètres à fournir

                    # demander la liste des commandes
                    commands_for_protocol = config.get_commands(protocol, parameters_interface)
                    pass

                # générer un dictionnaire ayant pour clé le nom des routeurs et pour valeurs les commandes

    # faire la configuration sur chaque routeur
    pass


if __name__ == '__main__':
    # topology = read_data("topology.json")
    # ip_topology = ip_generator.get_ip_topology("topology.json")
    # i = 1
    # for router in ip_topology:
    #     print("Router {}".format(i))
    #     i+=1
    #     for neighbor in router:
    #         commands = config.get_commands("ip_address", neighbor)
    #         print(commands)
    main()