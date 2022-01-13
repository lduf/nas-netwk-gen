# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
import ip_generator
import config
from tabulate import tabulate
import json

selected_interfaces = set()
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

def read_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def routers(topology):
    router_list = []
    for router in topology:
        router_list.append(router)
    return router_list

def interfaces(topology):
    interface_list = []
    for interface in topology:
        interface_list.append([topology[interface], interface])
    return interface_list

def protocols():
    protocols = ["ospf", "ip_address"]
    return protocols

def echo(text):
    global selected_interfaces
    selected_interfaces.add(text)
    print(selected_interfaces)
    input("\n{} is selected\n".format(text))
   


def action(router, param):
    global selected_interfaces
    if param == "interface_name" :
         # Create the root menu
        menu = MultiSelectMenu(f"Choose interfaces for {router}", "",
                           epilogue_text=("Please select one or more entries separated by commas, and/or a range of numbers. For example:  1,2,3   or   1-4   or   1,3-4"),
                           prologue_text=("Pleave save your selection and press enter to continue"),
                           exit_option_text='Save')  # Customize the exit text
        
        for interface in [x[0] for x in interfaces(topo[router]["interfaces"])] :
            interface = f"* {interface}" if interface in selected_interfaces else interface
            menu.append_item(FunctionItem(interface, echo, args=[interface]))
        # Show the menu
        menu.show()
        
    else :
        print("\nHello from action {}!!!\n".format(router))
        var = input("Please, fill the detail for {} : \n >>".format(param))
        print("\n{} is {}\n".format(param, var))

    Screen().input("Please, press [enter] to continue...")


if __name__ == '__main__':
    topo = read_data("topology.json")
    menu = ConsoleMenu("Network configuration", "Choose an action")
    #router_selection_menu = SelectionMenu(routers(topo))
    router_selection_menu = SelectionMenu("")
    router_selection_menu.title = "Choose a router"

    for router in routers(topo):
        # Creating a submenu for each router
        router_menu = SelectionMenu("")
        router_menu.title = f"{router} options"
        router_menu.prologue_text =tabulate(interfaces(topo[router]["interfaces"]), headers=["Interface", "Router"])
        router_submenu = SubmenuItem(router, router_menu, router_selection_menu)
        router_selection_menu.append_item(router_submenu)

        # Creating a submenu for each protocols
        protocols_selection_menu = SelectionMenu("")
        protocols_selection_menu.title = "Choose a protocol for {}".format(router)
        for protocol in protocols():
            protocol_menu = ConsoleMenu()
            protocol_menu.title = f"{protocol} options"
            parameters = config.get_commands_parameters(protocol)
            for param in parameters:
                param_menu = FunctionItem(param, action, args=[router, param])
                protocol_menu.append_item(param_menu)
            protocol_submenu = SubmenuItem(protocol, protocol_menu, protocols_selection_menu)
            protocols_selection_menu.append_item(protocol_submenu)


            
        protocols_selection_submenu = SubmenuItem("Configure protocol", protocols_selection_menu, router_menu)
        protocols_selection_submenu.title = "Choose a protocol for {}".format(router)

        router_menu.append_item(protocols_selection_submenu)

        

    
    

    submenu_router_selection_menu = SubmenuItem("Choose a router", router_selection_menu, menu)
    submenu_router_selection_menu.should_exit = False
    

    menu.append_item(submenu_router_selection_menu)

    # Finally, we call show to show the menu and allow the user to interact
    menu.show()
    menu.join()
    print(router_selection_menu.selected_option)
    
