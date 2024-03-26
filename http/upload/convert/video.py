
import os
import mimetypes
import magic
import threading

CONVERT_LIST = {
  'video/mp4': "ffmpeg -i {{INPUT_FILE}} -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 -b:v 7M -maxrate 7M -bufsize 3M {{OUTPUT_FILE}}",
  'video/x-matroska': "ffmpeg -i {{INPUT_FILE}} -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 -b:v 7M -maxrate 7M -bufsize 3M {{OUTPUT_FILE}}",
  'video/x-ms-wmv': "ffmpeg -i {{INPUT_FILE}} -c:v libx264 -crf 23 -c:a aac -q:a 100 -b:v 7M -maxrate 7M -bufsize 3M {{OUTPUT_FILE}}",
  'video/x-msvideo': "ffmpeg -i {{INPUT_FILE}} -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 -b:v 7M -maxrate 7M -bufsize 3M {{OUTPUT_FILE}}",
  'video/quicktime': "ffmpeg -i {{INPUT_FILE}} -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 -b:v 7M -maxrate 7M -bufsize 3M {{OUTPUT_FILE}}",
  'video/webm': "ffmpeg -i {{INPUT_FILE}} -c:v libx264 -crf 19 -preset slow -c:a aac -b:a 192k -ac 2 -b:v 7M -maxrate 7M -bufsize 3M {{OUTPUT_FILE}}",
};


def ffmpegConvert(path, cmd, save='-saved'):
    """
        @description: Il s'agit ici de la fonction permettant de réaliser la conversion du fichiers.
    """
    pathWithoutExtension = '.'.join(path.split('.')[0:-1])
    outputPath = pathWithoutExtension + '-output.mp4'
    cmd = cmd.replace('{{INPUT_FILE}}', path)
    cmd = cmd.replace('{{OUTPUT_FILE}}', outputPath)

    if os.path.exists(outputPath):
        os.system('rm -rf ' + outputPath)

    os.system(cmd)
    
    if not os.path.exists(outputPath):
        return False

    return convertOutputPath(outputPath)

def convertOutputPath(path):
    """
        @description: Permet de convertir le nom du fichier de sortie.
        @param: path -> Le chemin absolue du fichier.
        @return: le chemin au sein du dossier media.
    """
    spl_media = path.split('media/')
    if len(spl_media) == 1:
        return path
    return spl_media[1]

class VideoConverter(threading.Thread):
    """
    Args:
        threading ([type]): [description]
    """
    
    def __init__(
        self, 
        fileSrc, 
        dbUploaded, 
        tp="avatar_video"
    ):
        """[summary]

        Args:
            fileSrc ([type]): La position de l'element telecharger
            dbUploaded ([type]): L'endroit au sauvegarder les modifications.
            tp (str, optional): 
                avatar_video -> Il s'agit d'indiquer que le type de conversion a realiser et avatar_video
                story_ads -> 
                uploaded_work -> 
        """
        threading.Thread.__init__(self)
        self.fileSrc = fileSrc
        self.dbUploaded = dbUploaded
        self.type = tp
        self.cmd = self.getVideoConverterCommand()

        if self.cmd is False:
            return;

        ffmpegConvert(self.fileSrc, self.cmd, '-before-convert')
        self.save_result_in_db()
        
    def save_result_in_db(self):
        """[summary]
        """
        if self.type == 'avatar_video': 
            self.dbUploaded.video.name = '.'.join(self.dbUploaded.video.name.split('.')[0:-1]) + '.mp4'
        elif self.type == 'story_ads': 
            self.dbUploaded.story_ads.name = '.'.join(self.dbUploaded.story_ads.name.split('.')[0:-1]) + '.mp4'
        elif self.type == 'uploaded_work':
            self.dbUploaded.uploaded_work.name = '.'.join(self.dbUploaded.uploaded_work.name.split('.')[0:-1]) + '.mp4'
        self.dbUploaded.save()

    def get_convert_list(self): 
        """[summary]
        """
        if self.type == 'avatar_video': 
            return VIDEO_AVATAR_CONVERT_LIST
        return PRODUCT_CONVERT_LIST

    def getVideoConverterCommand(self):
        """
            @description: Permet de récupérer le bonne éléments au bon moment.
        """
        m = magic.open(magic.MAGIC_MIME)
        m.load()
        mimetype = m.file(self.fileSrc)

        CONVERT_LIST = self.get_convert_list()
        
        if mimetype not in CONVERT_LIST:
            return False

        cmd = CONVERT_LIST[mimetype]
        return cmd

    def run(self):
        """
            @description: Lancer la conversion à ce niveaux la...
        """
        # -> Maintenant je supprime l'ancien fichiers que je remplace par le nouveaux.
        # -> Il serait pas mal d'avoir des vu un peu plus interessantes sur mon avenir;

def getVideoConverterCommand(fileSrc):
    """
        @description: Permet de récupérer le bonne éléments au bon moment.
    """
    global CONVERT_LIST

    m = magic.open(magic.MAGIC_MIME)
    m.load()
    mimetype = m.file(fileSrc)
    
    if mimetype not in CONVERT_LIST:
        return False

    cmd = CONVERT_LIST[mimetype]
    return cmd