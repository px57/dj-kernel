

def serialize_to_timestamp(field): 
    """
        @description: 
    """
    if field is None:
        return None
    return field.timestamp()