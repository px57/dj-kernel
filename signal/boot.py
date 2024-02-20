from django.apps import AppConfig
from django.dispatch import Signal

# Création d'un signal personnalisé
model_ready = Signal()
