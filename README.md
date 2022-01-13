# nas-netwk-gen
NAS project

BGP :
- politique en entrée sur les sessions BGP (péréférence locale en fonction du type de relation avec le peer) -> local pref
- filtrage : filer les routes des peer qu'avec les clients etc (cf community tagging)
En entrée sur les sessions ajouter une commande pour set les liens (community tagging)


[todo]

Proposition 1 (sans doute obsolète)
- etudier bgp pour répondre aux attentes de pierre (mathis + 
- finir la topo (fichier topo.py qui créer la topologie) (mathis + 
- completer config.json pour config finale
- API et main qui crache bien pile poil la config
- SSH pour rentrer la config dans les routeurs
- que ça tourne impec (wireshark pour vérif)
  
proposition 2 (sens inverse avec console pour protocoles)
- on dessine dans bgp
- on récupère la topo par gns3fy on l'écrit dans topo.json
- dans le terminal on demande au user quels protocoles sur quels routeurs
- completer config.json pour config finale
SUITE

proposition 3 (sens inverse + protocoles dans le routeur usage sur gns3)
- on dessine dans bgp + on indique dans routeur usage les protocoles
- on récupère la topo par gns3fy on l'écrit dans topo.json
- completer config.json pour config finale
SUITE
