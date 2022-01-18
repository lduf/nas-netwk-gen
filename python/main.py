import ip_generator
import config
import json
import re
import socket

def read_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def routeur_number(routeur_string):
    return re.findall(r'R(\d+)', routeur_string)[0]

def get_commands_for_routers(ip_topology):
    dict_commands_to_send = {}
    for router in ip_topology:
        # ajouter le routeur comme clé du dictionnaire
        dict_commands_to_send[router] = {}
        dict_commands_to_send[router]["console_ip"] = "127.0.0.1"
        dict_commands_to_send[router]["console_port"] = ip_topology[router]["console"]
        dict_commands_to_send[router]["commands"] = []

        for interface in ip_topology[router]["interfaces"]:
            # récupérer pour chaque interface de chaque routeur la liste des protocoles activés
            if "protocols" in ip_topology[router]["interfaces"][interface]:
                protocols_for_interface = ip_topology[router]["interfaces"][interface]["protocols"]

                list_commands_interface = []

                # faire appel à l'API de config pour récupérer la liste des commandes pour chaque protocol
                for protocol in protocols_for_interface:
                    # concaténer les deux dictionnaires (le dictionnaire de router + le dict d'interface)
                    parameters_interface = {**ip_topology[router]["interfaces"][interface]["parameters"], **ip_topology[router]["parameters"]}

                    # demander la liste des commandes et l'ajouter à la liste des commandes associées au routeur
                    list_commands_interface.extend(config.get_commands(protocol, parameters_interface))

            print(f"{router} : {interface} : {protocols_for_interface} : {list_commands_interface}")
            dict_commands_to_send[router]["commands"].extend(list_commands_interface)

    return dict_commands_to_send

def configurate_routers(dict_commands_to_send):
    cpt_router_config = 0
    # pour se connecter on a besoin de l'IP et du port
    # utile d'avoir le nom du routeur aussi
    for router in dict_commands_to_send:
        console_ip = dict_commands_to_send[router]["console_ip"]
        console_port = dict_commands_to_send[router]["console_port"]

        print(f"Configuration de {router} / Tentative de connexion à {console_ip}:{console_port}")

        try:
            # connexion
            router_console_sock = socket.socket()
            router_console_sock.connect((console_ip, console_port))

            for command in dict_commands_to_send[router]["commands"]:
                # convertir la command en bytes et rajouter '\r'
                command_bytes = bytes(command + '\r', 'utf-8')

                print(command_bytes)
                # envoi de la commande
                router_console_sock.send(command_bytes)

            print(f"Configuration de {router} (en théorie) terminée")
            cpt_router_config += 1

        except ConnectionRefusedError as e:
            print(f"Erreur - Lancer le serveur GNS3 avant de réessayer")

    print(f"Configuration terminée, {cpt_router_config}/{len(dict_commands_to_send)} routeurs configurés")



def main():
    topology_file = "topology.json"

    # génération des IP (se fera seulement si certaiens interfaces n'ont pas d'IP affectées)
    ip_topology = ip_generator.generate_ip_topology(topology_file)

    # récupération des commandes à envoyer à chaque routeur pour la configuration
    dict_commands_to_send = get_commands_for_routers(ip_topology)
    
    # faire la configuration sur chaque routeur
    configurate_routers(dict_commands_to_send)
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