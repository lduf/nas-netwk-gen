# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
import ip_generator
import config
from tabulate import tabulate
import json
import sys
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
            interface_list.append([interface,"Ø",topology[interface]["ip"]["ip_address"], "Ø"])
    return interface_list

def protocols():
    protocols = ["ospf", "mpls"]
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
            if interface != "Loopback0":
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
    protocol_menu.prologue_text = tabulate(topo[router]["parameters"].items(), headers=["Parameter", "Value"])
    
    
    



def router_desc(router) :
    return tabulate(interfaces(topo[router]["interfaces"]), headers=["Interface", "Router", "IP", "Protocols"])
if __name__ == '__main__':
    
   #router_selection_menu = SelectionMenu(routers(topo))
    router_selection_menu = SelectionMenu("")
    router_selection_menu.title = "Choose a router"

    i =0
    router_menu = []
    router_submenu = []
    protocols_selection_menu = []
    protocol_menu = [[]]
    param_menu = [[]]
    protocol_submenu = [[]]
    protocols_selection_submenu = []
    for router in routers(topo):
        selected_interfaces[router] = set()
        # Creating a submenu for each router

        router_menu.append(ConsoleMenu(router, f"Please configure the {router} router")) # Creating a submenu for a router
        router_menu[i].prologue_text = router_desc(router)
     
        router_submenu.append(SubmenuItem(router, router_menu[i], router_selection_menu)) # Creating a submenu for each router
        router_selection_menu.append_item(router_submenu[i]) # Adding the submenu to the main menu
        
        # Creating a submenu for each protocols
        protocols_selection_menu.append(SelectionMenu(""))
        protocols_selection_menu[i].title = "Choose a protocol for {}".format(router)
        
        j = 0
        for protocol in protocols():
            protocol_menu.append([])
            protocol_menu[i].append(ConsoleMenu())
            protocol_menu[i][j].title = f"{protocol} options"
            options_list = config.get_commands_parameters(protocol)
            protocol_menu[i][j].prologue_text = tabulate(topo[router]["parameters"].items(), headers=["Parameter", "Value"])
            
            for param in options_list:
                param_menu.append([])
                param_menu[i].append(FunctionItem(param, action, args=[router, param, protocol, router_menu[i], protocol_menu[i][j]]))
                protocol_menu[i][j].append_item(param_menu[i][-1])
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
   

    jsonString = json.dumps(topo, indent=4)
    fileName = args.topology_file
    file = open(fileName, "w")
    file.write(jsonString)
    file.close()
