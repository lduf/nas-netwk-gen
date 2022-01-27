# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
#from sklearn import neighbors
import ip_generator
import config
from tabulate import tabulate
import json
import sys
import ipaddress
import argparse

nb = 0
menu = ConsoleMenu("Network configuration", "Choose an action")
selected_interfaces = dict()

parser = argparse.ArgumentParser(description='Run ip generation algorithm')
parser.add_argument('-f', '--topology_file', type=str, help='give the topology file name (default : topology.json)', metavar='', default="topology.json")
args = parser.parse_args()

"""
Voici l'arbre de la topologie
{
    Routers >
    …
        Protocols >
            …
            > Params
                [   Interfaces >
                    …
                ]
            
                
}

"""

def router_title() :
    global nb
    return f"{router} options / call {nb}"

def read_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def write_data(filename, data):
    with open(filename, 'w') as outfile:
        jsonString = json.dumps(topo, indent=4)
        outfile.write(jsonString)

topo = read_data(args.topology_file)

def routers(topology):
    router_list = []
    for router in topology:
        router_list.append(router)
    return router_list

def interfaces(topology):
    interface_list = []
    for interface in topology:
        if interface != "Loopback0":
            interface_list.append([interface,topology[interface]["neighbor"]["name"],topology[interface]["ip"]["ip_address"],topology[interface]["protocols"]])
        else :
            interface_list.append([interface,"Ø",topology[interface]["ip"]["ip_address"], topology[interface]["protocols"]])
    return interface_list

def protocols():
    protocols = ["ospf", "mpls", "bgp_en"]
    return protocols

def echo(text):
    global selected_interfaces
    selected_interfaces[router].add(text)
    print(selected_interfaces)
    input("\n{} is selected\n".format(text))
   

def enable(router, interface, protocol, menu):
    global selected_interfaces, topo, nb
    if protocol in topo[router]["interfaces"][interface]["protocols"] and interface in selected_interfaces[router]:
        selected_interfaces[router].remove(interface)
        topo[router]["interfaces"][interface]["protocols"].remove(protocol)
    else :
        selected_interfaces[router].add(interface)
        topo[router]["interfaces"][interface]["protocols"].append(protocol)

    menu.prologue_text = "Pleave save your selection and press enter to continue \n"
    for interface in selected_interfaces[router]:
        menu.prologue_text += f"\n{interface} is selected\n"
    
def enable_bgp(router, bgprouter, menu2, relation_type="peer"):
    (router_interface, bgp_type, neighbor_router_name,neighbor_interface_name, neighbor_as_number, neighbor_ip_address) = bgprouter
    weight = {"client":50, "peer":100, "provider":150}
    reverse = {"client":"provider", "peer":"peer", "provider":"client"}
    if bgp_type == "ebgp":
        bgp_type = f"ebgp_{relation_type}"

    neighbor_mask = topo[neighbor_router_name]["interfaces"][neighbor_interface_name]["ip"]["mask"]
    neighbor_network = ipaddress.ip_network(f"{neighbor_ip_address}{neighbor_mask}", strict=False)
    neighbor_network = str(neighbor_network.network_address)

    topo[router]["interfaces"][router_interface]["parameters"]["neighbor_ip"] = neighbor_ip_address
    topo[router]["interfaces"][router_interface]["parameters"]["neighbor_as"] = neighbor_as_number
    topo[router]["interfaces"][router_interface]["protocols"].append(bgp_type)
    topo[router]["interfaces"][router_interface]["parameters"]["relation_type"] = weight[relation_type]
    topo[router]["interfaces"][router_interface]["parameters"]["network"] = neighbor_network

    router_ip_address = topo[router]["interfaces"][router_interface]["ip"]["ip_address"]
    router_mask = topo[router]["interfaces"][router_interface]["ip"]["mask"]
    router_as_number = topo[router]["parameters"]["as_number"]
    router_network = ipaddress.ip_network(f"{router_ip_address}{router_mask}", strict=False)
    router_network = str(router_network.network_address)

    topo[neighbor_router_name]["interfaces"][neighbor_interface_name]["parameters"]["neighbor_ip"] = router_ip_address
    topo[neighbor_router_name]["interfaces"][neighbor_interface_name]["parameters"]["neighbor_as"] = router_as_number
    #topo[neighbor_router_name]["interfaces"][neighbor_interface_name]["protocols"].append(bgp_type)
    topo[neighbor_router_name]["interfaces"][neighbor_interface_name]["parameters"]["relation_type"] = weight[reverse[relation_type]]
    topo[neighbor_router_name]["interfaces"][neighbor_interface_name]["parameters"]["network"] = router_network

    write_data(args.topology_file, topo)

def add_bgp_neighbor(router, bgprouter, router_menu, protocol_menu):
    global menu
    (_, bgp_type, _,_, _, _) = bgprouter
    if bgp_type == "ebgp" :
        menu2 = ConsoleMenu("Please select one relation type")
        #menu2.epilogue_text=("Please select one relation type"),
        #menu2.prologue_text=("Pleave save your selection and press enter to continue \n"),
        #menu2.exit_option_text='Save' # Customize the exit text
        
        menu2.append_item(FunctionItem("Client", enable_bgp, args=[router,bgprouter, menu2, "client"], should_exit=True))
        menu2.append_item(FunctionItem("Peer", enable_bgp, args=[router, bgprouter, menu2, "peer"], should_exit=True))
        menu2.append_item(FunctionItem("Provider", enable_bgp, args=[router, bgprouter, menu2, "provider"], should_exit=True))
        # Show the menu
        menu2.show()
    else:
        enable_bgp(router, bgprouter, None, "peer")
    router_menu.prologue_text = router_desc(router)
    menu.draw()
  

def action(router, param, protocol, router_menu, protocol_menu):
    global selected_interfaces, menu, topo
    if param == "interface_name" :
         # Create the root menu
        menu2 = MultiSelectMenu(f"Choose interfaces for {router}", "",
                           epilogue_text=("Please select one or more entries separated by commas, and/or a range of numbers. For example:  1,2,3   or   1-4   or   1,3-4"),
                           prologue_text=("Pleave save your selection and press enter to continue \n"),
                           exit_option_text='Save')  # Customize the exit text
        for interface in selected_interfaces[router]:
            menu2.prologue_text += f"\n{interface} is selected\n"
        for interface in [x[0] for x in interfaces(topo[router]["interfaces"])] :
            interface = f"{interface}" if interface in selected_interfaces[router] else interface
            menu2.append_item(FunctionItem(interface, enable, args=[router,interface, protocol, menu2]))
        # Show the menu
        menu2.show()
    else :
        print(f"\nYou are configuring {router} detail\n".format(router))
        #print(router_desc(router))
        print("Current configuration for {}: {}".format(param, topo[router]["parameters"][param] if param in topo[router]["parameters"] else "Ø"))
 
        var = Screen().input("Please, fill the detail for {} : \n >>".format(param))
        print("\n{} is {}\n".format(param, var))
        if var != "":
            topo[router]["parameters"][param] = var
    
    router_menu.prologue_text = router_desc(router)
    options_list = config.get_commands_parameters(protocol)
    protocol_menu.prologue_text = protocols_desc(router, options_list)
    write_data(args.topology_file, topo)
    bgp_neighbor_selection[int(router[1:])] = draw_bgp_neighbors_menu(int(router[1:]))
    bgp_neighbor_selection[int(router[1:])].draw()
    

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def protocols_desc(router, protocol_options) :
    inter = intersection(protocol_options, topo[router]["parameters"].keys())
    info = {}
    for options in inter :
        info[options] = topo[router]["parameters"][options]

    return tabulate(info.items(), headers=["Parameter", "Value"])

def router_desc(router) :
    return tabulate(interfaces(topo[router]["interfaces"]), headers=["Interface", "Router", "IP", "Protocols"])


def bgp_neighbors(current_router, routers, neighbors_menu):
    # The first step is to get all the router in the same AS
    #The tuple is define like (bgp_type, router_name, as_number, ip_address)
    if "as_number" not in topo[current_router]["parameters"].keys():
        neighbors_menu.prologue_text = "You need to configure the AS number before adding BGP neighbors"
        return []
    else :
        current_as = topo[current_router]["parameters"]["as_number"]
    bgp_neighbors = []
    for router in routers:
        if router != current_router:
            if "as_number" in topo[router]["parameters"].keys() and  topo[router]["parameters"]["as_number"] == current_as:
                    bgp_neighbors.append(("Loopback0","ibgp", router, "Loopback0", current_as, topo[router]["interfaces"]["Loopback0"]["ip"]["ip_address"]))
    
    for interface in topo[current_router]["interfaces"]:
        if interface != "Loopback0":
            neighbor = topo[current_router]["interfaces"][interface]["neighbor"]
            if "as_number" in topo[neighbor["name"]]["parameters"].keys() and topo[neighbor["name"]]["parameters"]["as_number"] != current_as:
                bgp_neighbors.append((interface,"ebgp", neighbor["name"], neighbor["interface"],topo[neighbor["name"]]["parameters"]["as_number"], topo[neighbor["name"]]["interfaces"][neighbor["interface"]]["ip"]["ip_address"]))

    return bgp_neighbors

def draw_bgp_neighbors_menu(i):
    bgp_neighbor_selection.append(ConsoleMenu("")) # Sous menu pour les voisins disponibles
    bgp_neighbor_selection[-1].title = f"{protocol} options - please choose a neighbor"
    
    bgp_neighbor_submenu.append([])
    for bgprouter in bgp_neighbors(router,routers(topo),bgp_neighbor_selection[-1]): # On ajoute les voisins disponibles
        (router_interface, bgp_type, neighbor_router_name,neighbor_interface_name, neighbor_as_number, neighbor_ip_address) = bgprouter
        desc = f"({bgp_type}) neighbor {neighbor_router_name} AS {neighbor_as_number} with IP {neighbor_ip_address}"
        bgp_neighbor_submenu[i].append(FunctionItem(desc, add_bgp_neighbor, args=[router, bgprouter,router_menu[i], protocol_menu[i][j]]))
        bgp_neighbor_selection[-1].append_item(bgp_neighbor_submenu[i][-1])
    
    return bgp_neighbor_selection[i]
    
if __name__ == '__main__':
    
  

   #router_selection_menu = SelectionMenu(routers(topo))
    router_selection_menu = SelectionMenu("") # Router selection menu : première page sur laquelle tous les autres menus sont attachés. On y voit la liste des routers
    router_selection_menu.title = "Choose a router"

    i =0
    router_menu = []
    router_submenu = []
    protocols_selection_menu = []
    protocol_menu = [[]]
    param_menu = [[]]
    protocol_submenu = [[]]
    protocols_selection_submenu = []
    bgp_neighbor_selection = []
    bgp_neighbor_submenu = [[]]

    '''
    Profondeur des menus :
    router_selection_menu
        router_menu
            

    '''
    
    for router in routers(topo):
        selected_interfaces[router] = set()
        # Creating a submenu for each router

        router_menu.append(ConsoleMenu(router, f"Please configure the {router} router")) # Creating a submenu for a router : on y voit les options de configuration pour un routeur donné
        router_menu[i].prologue_text = router_desc(router) # Description du routeur courrant
     
        router_submenu.append(SubmenuItem(router, router_menu[i], router_selection_menu)) # On ajoute le sous menu du routeur courrant à la liste des sous menus du menu principal
        router_selection_menu.append_item(router_submenu[i]) # Adding the submenu to the main menu
        
        # Creating a submenu for each protocols
        protocols_selection_menu.append(SelectionMenu(""))
        protocols_selection_menu[i].title = "Choose a protocol for {}".format(router)
        
        j = 0
        for protocol in protocols(): # Creating a submenu for each protocol
            protocol_menu.append([])
            protocol_menu[i].append(ConsoleMenu())
            protocol_menu[i][j].title = f"{protocol} options"

            options_list = config.get_commands_parameters(protocol) # Getting the list of options for a protocol
            protocol_menu[i][j].prologue_text = protocols_desc(router, options_list) # Current parameters for the protocol
            # TODO : display only the options that are relevant for the protocol

            

            for param in options_list: # For each option of the protocol
                param_menu.append([])
                param_menu[i].append(FunctionItem(param, action, args=[router, param, protocol, router_menu[i], protocol_menu[i][j]])) # adding the option to the submenu. It refers to the action function which will display the option and ask the user to fill the detail
                protocol_menu[i][j].append_item(param_menu[i][-1]) # Adding the option to the submenu
                
            if protocol == "bgp_en": ## Si le protocole est bgp, on ajoute les paramètres de bgp et on ajoute un sous menu qui contient les voisins
                '''
                bgp_neighbor_selection.append(ConsoleMenu("")) # Sous menu pour les voisins disponibles
                bgp_neighbor_selection[-1].title = f"{protocol} options - please choose a neighbor"
                
                bgp_neighbor_submenu.append([])
                for bgprouter in bgp_neighbors(router,routers(topo),bgp_neighbor_selection[-1]): # On ajoute les voisins disponibles
                    (router_interface, bgp_type, neighbor_router_name,neighbor_interface_name, neighbor_as_number, neighbor_ip_address) = bgprouter
                    desc = f"({bgp_type}) neighbor {neighbor_router_name} AS {neighbor_as_number} with IP {neighbor_ip_address}"
                    bgp_neighbor_submenu[i].append(FunctionItem(desc, add_bgp_neighbor, args=[router, bgprouter,router_menu[i], protocol_menu[i][j]]))
                    bgp_neighbor_selection[-1].append_item(bgp_neighbor_submenu[i][-1])
                '''
                bgp_neighbor_selection[i] = draw_bgp_neighbors_menu(i)
                param_menu[i].append(SubmenuItem("Add neighbor",bgp_neighbor_selection[i], protocol_menu[i][j]))
                protocol_menu[i][j].append_item(param_menu[i][-1])
                #bgp_neighbor_selection[-1].append_item(protocol_menu[i][j])

            protocol_submenu.append([])
            protocol_submenu[i].append(SubmenuItem(protocol, protocol_menu[i][j], protocols_selection_menu[i]))
            protocols_selection_menu[i].append_item(protocol_submenu[i][j])
            j += 1


            
        protocols_selection_submenu.append(SubmenuItem("Configure protocol", protocols_selection_menu[i], router_menu[i]))
        protocols_selection_submenu[i].title = "Choose a protocol for {}".format(router)

        router_menu[i].append_item(protocols_selection_submenu[i])
        i+=1


    submenu_router_selection_menu = SubmenuItem("Choose a router", router_selection_menu, menu)
    submenu_router_selection_menu.should_exit = False
    

    menu.append_item(submenu_router_selection_menu)
    # Finally, we call show to show the menu and allow the user to interact
    menu.show()
   
    write_data(args.topology_file, topo)
