from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs): # User class created above is sender and this function is receiver
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile is created")
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            #create the userprofile if not exist
            profile=UserProfile.objects.get(user=instance)
            print('Profile was not exist, but I created one')
        print('user is updated')

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'this user is being saved')

