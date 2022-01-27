# nas-netwk-gen

## Introduction to the project : 

The original goal of the project is to automate the production of a topology configuration on the gns3 software, including the following protocols OSPF, MPLS and BGP.  
The project and its files are subdivided into two distinct but communicating parts, in the GNS folder you will find different topologies that can be used, some are blank and others are pre-configured.   
For example, the most advanced and detailed configuration with the optimal and targeted final configuration is located in \GNS\NAS_Final.  
The automation part works like this, first you have to produce or use a gns3 topology with nodes and links, but without configuration. Then you can move on to the next part.


## Python Usage : 

The python files are in the python folder. Please make sure to install all the required packages before running the python files.

```bash
pip3 install -r requirements.txt
```
It is possible that the installation of the gns3fy library is quite complex, if need be, you can use this precise branch :
```bash
pip install gns3fy @ git+https://github.com/davidban77/gns3fy@583c9aa0a64bac9cb3fdd9631a3af151496cb56e
```

### Get the current topology from GNS3

We are using `gns3fy` library to get the project's topology. You may run the following :

```bash
python3 topo.py [-h] [-o] gns3_file
```
Your lab gns3 needs to be open.

```bash
usage: topo.py [-h] [-o] gns3_file

Get the current GNS3 topology

positional arguments:
  gns3_file             the GNS3 project name

optional arguments:
  -h, --help            show this help message and exit
  -o , --topology_file 
                        the topology file name (default : topology.json)
```

### Auto-generate an IP topology

You have the possibility to auto-generate ip address for your topology. You may have a `topology.json`before runnning this script. The IP address is given with the following format : 10.0.Y.X where Y is an incremental value and X the router number.

Loopback addresses are also generated according to the following format X.X.X.X where X is the router number

You may run the following : 

```bash
python3 ip_generator.py [-h] [-f]
```

```bash
usage: ip_generator.py [-h] [-f]

Run ip generation algorithm

optional arguments:
  -h, --help            show this help message and exit
  -f , --topology_file 
                        give the topology file name (default : topology.json)
```

### Use a client to help you to generate the json configuration file

You can use `cli.py` to help you to generate the configuration file. This menu can help you to assign protocols to each routers' interfaces. 

Supported protocols :

- OSPF
- MPLS
- BGP

After selecting a router, you can choose which protocol to configure. The necessary parameters are requested. The BGP configuration is only possible after you have entered the AS numbers of the routers. **In the current version a bug forces the user to quit the client after having filled the AS numbers and to restart the client in order to generate the BGP configuration**.

The client allows to generate automatically the json configuration file. To simplify the use of the menu, simplifications have been made regarding the protocol parameters. 

*Example:*

- *When configuring i-BGP, the IP for the routers is always the Loopback address.*
- *e-BGP will always ask the type of relationship (client, peer, provider) and predefined weights will be applied.  If an R1 --> R2 relationship is defined, the client automatically generates the R2 --> R1 relationship.*

The configuration is saved with each entry.

```bash
python3 cli.py [-h] [-f]
```

```bash
usage: cli.py [-h] [-f]

Run ip generation algorithm

optional arguments:
  -h, --help            show this help message and exit
  -f , --topology_file 
                        give the topology file name (default : topology.json)
```

Menu improvement: 

- Better display of selected configurations (especially in BGP)
- Support of other functions (ip_topology.py, topo.py, main.py) to launch directly these scripts from the user interface  

The use of this front end client is not mandatory, it just allows an additional layer of abstraction to improve the user experience  
If you want you can write the file topology.json, which will be read by main.py, by hand. Here is the syntax to adopt.  


## Json topology :

Here below is an exemple of the description of a router on the topology file (this first exemple shows a basic router inside an ospf area)  

```
"R1": { //router number
        "router_id": "996e4fd9-9ca0-4b18-9ac5-8d5d14a58192", //gns3 router id
        "parameters": { //global router parameters
            "ospf_process_id": "1",
            "router_id": "1.1.1.1",
            "area_id": "1"
        },
        "console": 6000, //console telnet port
        "interfaces": { 
            "GigabitEthernet2/0": { //Name of the interface
                "neighbor": { //Neighbor on the other end of the link
                    "name": "R3",
                    "interface": "GigabitEthernet1/0"
                },
                "protocols": [ //protocols activated on the router
                    "ip_address", //this line depicts the editing of the interfaces with specific ip address
                    "ospf",
                    "mpls"
                ],
                "parameters": { //More parameters about the interface (some are redundant)
                    "ip_address": "10.0.1.1",
                    "mask": "255.255.255.0",
                    "interface_name": "GigabitEthernet2/0"
                },
                "ip": { //Parameters of the ip_address protocol
                    "ip_address": "10.0.1.1",
                    "mask": "255.255.255.0"
                }
            },
```

### GNS3 project configuration from the topology file

You need to use the main.py script to run the configuration.

The configuration uses a connection to GNS sockets. Therefore the GNS3 project must be open and the simulation started. 
**Probable issue:** If the command terminals of the routers are not open, the connection to the sockets may not work

```bash
python3 main.py [-h] [-f]
```

```bash
usage: main.py [-h] [-f]

Run ip generation algorithm

optional arguments:
  -h, --help            show this help message and exit
  -f , --topology_file 
                        give the topology file name (default : topology.json)
```