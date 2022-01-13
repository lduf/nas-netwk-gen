#!/usr/bin/env python3
import gns3fy
import sys
from tabulate import tabulate
import json
from collections import defaultdict

'''
    L'objectif est de convertir le links_summary en topology exploitable par la suite des fichiers configs
    entrée : links_summary [(node1, interface1, node2, interface2), ...]
    sortie : topo json {node1: {"interface": {node: interface, node : interface}}, node2: {...}}
'''
def write_topology(links_summary, nodes_summary):
    #links_summary : [('R1', 'GigabitEthernet2/0', 'R3', 'GigabitEthernet1/0'), ('R3', 'GigabitEthernet3/0', 'R4', 'GigabitEthernet3/0'),...]

    topo = defaultdict(dict)

    for nodes in nodes_summary :
        topo[nodes[0]] = {}
    #(<class 'dict'>, {'R1': {}, 'R2': {}, 'R3': {}, 'R4': {}, 'R5': {}, 'R6': {}, 'R7': {}, 'R8': {}})

    for nodes in nodes_summary :
        topo[nodes[0]]["router_id"] = nodes[3]
        topo[nodes[0]]["parameters"] = {}

    for link in links_summary :
        topo[link[0]]["interfaces"] = {}
        topo[link[2]]["interfaces"] = {}

    for link in links_summary :
        topo[link[0]]["interfaces"][link[1]] = {}
        topo[link[0]]["interfaces"][link[1]]["neighbor"] = {"name" : link[2], "interface" : link[3]}
        topo[link[0]]["interfaces"][link[1]]["protocols"] = []
        topo[link[0]]["interfaces"][link[1]]["parameters"] = {}
        topo[link[0]]["interfaces"][link[1]]["ip"] = {}

        topo[link[2]]["interfaces"][link[3]] = {}
        topo[link[2]]["interfaces"][link[3]]["neighbor"] = {"name" : link[0], "interface" : link[1]}
        topo[link[2]]["interfaces"][link[3]]["protocols"] = []
        topo[link[2]]["interfaces"][link[3]]["parameters"] = {}
        topo[link[2]]["interfaces"][link[3]]["ip"] = {}

    print(topo)
    
    jsonString = json.dumps(topo, indent=4)

    fileName = sys.argv[1] if len(sys.argv) > 1 else "topology.json"
    file = open(fileName, "w")
    file.write(jsonString)
    file.close()

    return topo


# Define the server object to establish the connection
server = gns3fy.Gns3Connector("http://localhost:3080")
lab = gns3fy.Project(name="NAS_Mathis", connector=server)
lab.get()
#print(lab)
lab.open()
#print(lab.status)
#print(lab.stats)
#nodes_tab = lab.nodes()
#print(nodes_tab)

links_summary = lab.links_summary(is_print=False)
nodes_summary = lab.nodes_summary(is_print=False)

print(nodes_summary)

write_topology(links_summary, nodes_summary)