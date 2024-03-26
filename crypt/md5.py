import hashlib
import os

def md5_file(file_path):
    """
        @description: 
    """
    if os.path.exists(file_path) is False:
        raise FileNotFoundError(f'The file {file_path} does not exist')
    
    with open(file_path, 'rb') as file:
        # Créer un objet de hachage MD5
        md5_hash = hashlib.md5()

        # Lire le fichier par blocs pour éviter de charger le fichier entier en mémoire
        while chunk := file.read(8192):
            md5_hash.update(chunk)

    # Récupérer la valeur MD5 sous forme de chaîne hexadécimale
    md5_digest = md5_hash.hexdigest()
    
    return md5_digest