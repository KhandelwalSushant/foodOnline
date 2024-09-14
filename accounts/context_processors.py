from vendor.models import Vendor

# context processor is a function which takes one argument that is request, 
# and return a dictionary that gets added to the request context.
# So, we are using it so that we all functions of sidebar can access the current user_profile from cover.html

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)