from dz import dz_array
from financial_system.models import User, UserNotification

'''
A context processor is a function that accepts an argument and returns a dictionary as its output.
In our case, the returning dictionary is added as the context and the biggest advantage is that,
it can be accessed globally i.e, across all templates. 
'''


def dz_static(request):
    # we can send data as {"dz_array":dz_array} than you get all dict, using <h1>{{ dz_array }}</h1>
    return {"dz_array": dz_array}


def current_user(request):
    #根据后端方法返回INXS
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(user_id=user_id)
        notifications = UserNotification.objects.filter(user_id=user_id)
        return {'current_user': user ,  "cur_notifications": notifications}
    else:
        return {'current_user': None}



