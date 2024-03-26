from django.utils import timezone
import copy

def update_created_on(dbField):
    """
        @description: Mettre à jours le created_on;
    """
    dbField.created_on = timezone.now()
    return dbField

def copy_model(field):
    """
        @description: Réaliser une copie conforme de l'ancien éléments.
    """
    new_field = copy.deepcopy(field)
    new_field.id = None
    new_field.pk = None
    new_field.save()
    return new_field

def set__jointure_attr(dbList):
    """Ajoute l'attribue __jointure à l'ensemble des éléments qui en sont dépourvu."""
    for dbline in dbList:
        if not hasattr(dbline, '__jointure'):
            setattr(dbline, '__jointure', {})

def merge_jointure(dbMerge, dbMerged, join_field_merge, join_field_merged, jointure_name):
    """
        Envoit les informations d'un elements à l'intérieur d'un autres.
        @params:
            dbMerge  -> La liste des éléments vers lequel il faut réaliser la jointure
            join_field_merge(string) -> le nom du champs qui sert à joindre les data pour les donnée de dbMerge

            dbMerged -> La liste des éléments à envoyer dans la premieres
            join_field_merged(string) -> Le nom du champs de jointure de dbMerged

            jointure_name(string) -> Correspond au nom de jointure dans la base de données.
        @return:
            dbMerge -> Il s'agit ici
    """
    set__jointure_attr(dbMerge)
    for dbMerge_line in dbMerge:
        query = {
            join_field_merged: getattr(dbMerge_line, join_field_merge)
        }
        dbMerge_line.__jointure[jointure_name] = dbMerged.filter(**query)
    return dbMerge

def serialize_jointure(serialized_response, jointure, request):
    """
        Sert à serializer les jointures réaliser dans les models.
        @params:
            serialized_response(dict) -> le dictionnaire des éléments serializer.
            jointure(dict:models) -> le contenu de l'attribue __jointure du models.
            request(Httprequest) -> La requêtes http pour vérifier certain parametres;
    """
    for key in jointure:
        value = jointure[key]
        if isinstance(value, QuerySet):
            serialized_response[key] = []
            for value_line in value:
                serialized_response[key].append(value_line.serialize(request))
        elif type(value) == list or type(value) == dict or type(value) == bool:
            serialized_response[key] = value
        else:
            serialized_response[key] = value.serialize(request)
    return serialized_response
