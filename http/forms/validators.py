"""Here add all forms validators."""

from uuid import UUID


def is_uuid(uuid_string, version=4):
    """Validate if uuid is ok."""
    if not uuid_string:
        return False
    try:
        # Si uuid_string est un code hex valide mais pas un uuid valid,
        # UUID() va quand même le convertir en uuid valide. Pour se prémunir
        # de ce problème, on check la version original (sans les tirets) avec
        # le code hex généré qui doivent être les mêmes.
        uid = UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False


def not_is_uuid(uuid_string, version=4):
    """Validate if uuid is not ok."""
    return not is_uuid(uuid_string, version=version)
