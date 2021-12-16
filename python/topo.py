#!/usr/bin/env python3

import gns3fy
from tabulate import tabulate

# Define the server object to establish the connection
server = gns3fy.Gns3Connector("http://localhost:3080")

# Show the available projects on the server
print(
    tabulate(
        server.projects_summary(is_print=False),
        headers=["Project Name", "Project ID", "Total Nodes", "Total Links", "Status"],
    )
)

# creation of a new project
#lab = gns3fy.Project(name="test_lab1", connector=server)
#lab.create()

lab = gns3fy.Project(name="NAS_Mathis", connector=server)
lab.get()
print(lab)
lab.open()
print(lab.status)
print(lab.stats)

'''
for template in server.get_templates():
    print(f"Template: {template['name']} -- ID: {template['template_id']}")

Template: c7200 -- ID: ea5c5303-dace-4499-a85d-e7d28d2d4531
Template: Cloud -- ID: 39e257dc-8412-3174-b6b3-0ee3ed6a43e9
Template: NAT -- ID: df8f4ea9-33b7-3e96-86a2-c39bc9bb649c
Template: VPCS -- ID: 19021f99-e36f-394d-b4a1-8aaa902ab9cc
Template: Ethernet switch -- ID: 1966b864-93e7-32d5-965f-001384eec461
Template: Ethernet hub -- ID: b4503ea9-d6b6-3695-9fe4-1db3b39290b0
Template: Frame Relay switch -- ID: dd0f6f3a-ba58-3249-81cb-a1dd88407a47
Template: ATM switch -- ID: aaa764e2-b383-300f-8a0e-3493bbfdb7d2

'''

R10 = gns3fy.Node(
project_id=lab.project_id,
connector=server,
name="R10",
template="c7200"
)
R10.create()



