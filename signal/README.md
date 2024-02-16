---
description: >-
  Signal est un petit utilitaire qui permet de creer des evenements, qui
  recoivent une liste de parametre en entree, et retourne un message.
---

# Signal



#### \[CREATE\_EVENT]

Pour creer un nouveaux signal ont doit tout d'abord pour une question de saine organisation lui creer un fichier signal.py  a l'interieur de l'application qui va l'executer ont fait donc.&#x20;

```sh
cd ./$app_name

touch signal.py 
```

Ensuite dans le fichier \_\_init\_\_.py  ont ajoute le code d'import du signal, pour que celui-ci soit executer lors du lancement de l'application.&#x20;

```python
from .signal import *
```

Finalement au sein du fichier signal.py ont creer notre signal, qui va permettre de gerer cette element.&#x20;

```python
from kernel.signal import SIGNAL_CENTER

SIGNAL_CENTER.create(
    'profile.load_me',
    description=
)
```

Ensuite devant les fonctions que l'ont tient a appeller lors de l'execution de cette fonction ont ajoute&#x20;

le binder 

#### \[BIND]

```
```

#### \[EXECUTE]

