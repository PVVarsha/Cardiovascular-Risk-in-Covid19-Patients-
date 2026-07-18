from django.db import models
from django.contrib.auth.models import User
from PIL import Image



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


from django.db import models
from django.contrib.auth.models import User




class UserPredictModel(models.Model):
    image = models.ImageField(upload_to = 'images/')
    label = models.CharField(max_length=20,default='data')

    def __str__(self):
        return str(self.image)
    


   

from django.db import models

class Patient_info(models.Model):
    Age = models.FloatField()
    Gender = models.CharField(max_length=100)  # Example: consider using choices=(...) for gender
    BMI = models.FloatField()
    Smoking_Status = models.CharField(max_length=100)
    COVID_Severity = models.CharField(max_length=100)
    SpO2 = models.FloatField()  # Example: consider using BooleanField for binary fields
    Blood_Pressure = models.FloatField()
    Heart_Rate = models.FloatField()
    ECG_Result = models.CharField(max_length=100)
    Troponin_Level = models.FloatField()
    D_Dimer = models.FloatField()
    CRP = models.FloatField()
    Blood_Sugar = models.FloatField()
    Cholesterol_Level = models.FloatField()
    Hypertension = models.CharField(max_length=100)
    Diabetes = models.CharField(max_length=100)
    Vaccine_Given = models.CharField(max_length=100)
    label = models.CharField(max_length=100)

    def __str__(self):
        return f"Prediction: {self.label}"

   