import os
from django.core.exceptions import ValidationError

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] #cover-image.jpg
    # (By giving [1] (this [1] is index here.) in this line we give extention  of the image, in this case jpg. and [0]  will give us the name of the image, in this case cover-image)
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    if not ext.lower() in valid_extensions:
        raise  ValidationError('Unsupported file extension. Allowed  extensions are: ' + str(valid_extensions))

