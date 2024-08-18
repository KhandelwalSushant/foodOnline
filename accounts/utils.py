#only for helper functions

def detectUser(user):
    if user.roles == 1:
        redirectUrl = 'vendordashboard'
        return redirectUrl
    elif user.roles == 2:
        redirectUrl = 'custdashboard'
        return redirectUrl
    elif user.roles == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl