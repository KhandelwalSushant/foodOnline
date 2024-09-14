from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import OneToOneField


# Create your models here.
class UserManager(BaseUserManager): # it will not contain any field
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user=self.model(
            email=self.normalize_email(email), #nomailze_email means if we provide upper case in email it will automatically make it lowercase
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password) #set_password is the method it will take the pass, encode it and store in the database
        user.save(using=self._db) #using=self._db is used to define which database should manager use for this 
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(  # we can't make a asuperuser directly here, so 1st we need to create a user then assign him as a superuser
            email = self.normalize_email(email),
            username = username,
            password=password,
            first_name = first_name,
            last_name = last_name,
        ) 
        user.is_admin = True
        user.is_active= True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser): # it will tipically store the user data that is field
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    roles = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.roles == 1:
            user_role = 'Vendor'
        elif self.roles == 2:
            user_role = 'Customer'
        return user_role
    
    # has_perm and has_module_perms will return true if the user is an active superuser or is an admin
    # and for inactive users it will always return false
    # by default only admin and superadmin can have access to this module

class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) # we are setting the blank and null = True because we don't know what will be the values of these fields
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True) # also we are going to send the signals
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'

    # now we will set the string representation of this model
    def __str__(self):
        return self.user.email

# this below is the first way to make the connection
# post_save.connect(post_save_create_profile_receiver, sender=User)

# second way is ->


