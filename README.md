# nas-netwk-gen

## Usage : 

The python files are in the python folder. Please make sure to install all the required packages before running the python files.

```bash
pip3 install -r requirements.txt
```



### Get the current topology from GNS3

We are using `gns3fy` library to get the project's topology. You may run the following :

```bash
python3 topo.py [-h] [-o] gns3_file
```

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



## Json topology :

