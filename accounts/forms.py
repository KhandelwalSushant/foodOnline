from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "PASSWORD DOES NOT MATCH!"
            )
        

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images_validator])

    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'})) ### this is the second way to make lattitude and longitude read only
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo','address','country','state','city','pincode','latitude','longitude']

    def  _init_(self, *args, **kwargs):
        super(UserProfileForm, self)._init_(*args, **kwargs)
        for  field in self.fields:
            if field=='latitude' or field=='longitude':
                self.fields[field].widget.attrs['readonly']='readonly'   #this _init_ function is the best way to make lattitude AND longitude  readonly in form. use this on preferance or the above is second