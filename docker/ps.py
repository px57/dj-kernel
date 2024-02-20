
import os
import docker
import json


def docker_ps():
    """
        @description: 
    """
    # Connexion au client Docker
    client = docker.from_env()

    # Récupération des conteneurs en cours d'exécution
    containers = client.containers.list()

    # Conversion des conteneurs en format JSON
    json_data = []
    for container in containers:
        json_data.append(container.attrs)

    return json_data

def docker_ps_json():
    """
        @description: 
    """
    docker_ps = docker_ps()
    return json.dumps(docker_ps, indent=4)

def choice_docker_container():
    """
        @description: 
    """
    # Récupération des conteneurs en cours d'exécution
    containers = docker_ps()

    # Affichage des conteneurs
    for i, container in enumerate(containers):
        print(f"{i+1}. {container['Name']}")

    # Choix du conteneur
    choice = int(input("Choisissez un conteneur: ")) - 1
    return containers[choice]

