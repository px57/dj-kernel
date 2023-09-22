from django.db import models
from kernel.models.base_metadata_model import BaseMetadataModel
import uuid

class UploadedImage(BaseMetadataModel):
    src = models.ImageField(upload_to='upload_files/%m-%Y')
    real_name = models.CharField(max_length=250, default='')

class UploadVideo(BaseMetadataModel):
    src = models.ImageField(upload_to='upload_files/%m-%Y')
    real_name = models.CharField(max_length=250, default='')

class SeecuboxFile(BaseMetadataModel):
    src = models.FileField(upload_to='upload_files/%m-%Y')
    real_name = models.CharField(max_length=250, default='')
