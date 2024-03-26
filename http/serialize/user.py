

def serialize_user(user, request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }