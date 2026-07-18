from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from .models import UserPredictModel,Patient_info

from tensorflow import keras
from PIL import Image, ImageOps
from . import forms
import os




def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

from .models import Profile

def profile(request):
    user = request.user
    # Ensure the user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})



   
def Deploy_10(request): 
    print("HI")
    if request.method == "POST":
        form = forms.UserPredictForm(files=request.FILES)
        if form.is_valid():
            print('HIFORM')
            form.save()
        obj = form.instance

        result1 = UserPredictModel.objects.latest('id')
        models = keras.models.load_model('F:/Heart disease Final project/heart disease/Deploy/Project/App/keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open("F:/Heart disease Final project/heart disease/Deploy/Project/" + str(result1)).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        classes = ['Abnormal heart beats','Cardiomyopathy','COVID-19','Myocardial Infarction','Normal']
        prediction = models.predict(data)
        idd = np.argmax(prediction)
        a = (classes[idd])
        if a == 'Abnormal heart beats':
            a = 'Abnormal heart beats'
        elif a == 'Cardiomyopathy':
            a = 'Cardiomyopathy'
        elif a == 'COVID-19':
            a = 'COVID-19'
        elif a == 'Myocardial Infarction':
            a = 'Myocardial Infarction'
        elif a == 'Normal':
            a = 'Normal'

        else:
            a = 'WRONG INPUT'

        data = UserPredictModel.objects.latest('id')
        data.label = a
        data.save()

        
        return render(request, 'app/result.html',{'form':form,'obj':obj,'predict':a})
    else:
        form = forms.UserPredictForm()
    return render(request, 'app/10_Deploy.html',{'form':form})

import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
import joblib
from .forms import Patient_info_Form

# Load trained model
Model1 = joblib.load('F:/Heart disease Final project/heart disease/Deploy/Project/App/heart.pkl')

def Deploy_9(request):
    if request.method == 'POST':
        form = Patient_info_Form(request.POST)
        if form.is_valid():
            try:
                # Extract cleaned data from form (all numeric or categorical mapped to numeric)
                Age = float(form.cleaned_data['Age'])
                Gender = float(form.cleaned_data['Gender'])
                BMI = float(form.cleaned_data['BMI'])
                Smoking_Status = float(form.cleaned_data['Smoking_Status'])
                COVID_Severity = float(form.cleaned_data['COVID_Severity'])
                SpO2 = float(form.cleaned_data['SpO2'])
                Blood_Pressure = float(form.cleaned_data['Blood_Pressure'])
                Heart_Rate = float(form.cleaned_data['Heart_Rate'])
                ECG_Result = float(form.cleaned_data['ECG_Result'])
                Troponin_Level = float(form.cleaned_data['Troponin_Level'])
                D_Dimer = float(form.cleaned_data['D_Dimer'])
                CRP = float(form.cleaned_data['CRP'])
                Blood_Sugar = float(form.cleaned_data['Blood_Sugar'])
                Cholesterol_Level = float(form.cleaned_data['Cholesterol_Level'])
                Hypertension = float(form.cleaned_data['Hypertension'])
                Diabetes = float(form.cleaned_data['Diabetes'])
                Vaccine_Given = float(form.cleaned_data['Vaccine_Given'])

                # Put features into DataFrame with column names
                feature_names = [
                    "Age", "Gender", "BMI", "Smoking_Status", "COVID_Severity", "SpO2",
                    "Blood_Pressure", "Heart_Rate", "ECG_Result", "Troponin_Level",
                    "D_Dimer", "CRP", "Blood_Sugar", "Cholesterol_Level",
                    "Hypertension", "Diabetes", "Vaccine_Given"
                ]

                features_df = pd.DataFrame([[
                    Age, Gender, BMI, Smoking_Status, COVID_Severity, SpO2,
                    Blood_Pressure, Heart_Rate, ECG_Result, Troponin_Level,
                    D_Dimer, CRP, Blood_Sugar, Cholesterol_Level,
                    Hypertension, Diabetes, Vaccine_Given
                ]], columns=feature_names)

                # Prediction
                prediction = Model1.predict(features_df)[0]

                if prediction == 0:
                    a = "High Risk"
                elif prediction == 1:
                    a = "Medium Risk"
                elif prediction == 2:
                    a = "Low Risk"
                else:
                    a = "Unknown"

                # Save result in DB
                instance = form.save(commit=False)
                instance.label = a
                instance.save()

                # Render result
                return render(request, 'app/5_Teamates.html', {'prediction_text': a})

            except Exception as e:
                return HttpResponse(f"❌ Error while predicting: {str(e)}")

    else:
        form = Patient_info_Form()

    return render(request, 'app/9_Deploy.html', {'form': form})


from .models import Patient_info

def report(request):
    return render(request,'app/report.html')

def patient_list(request):
    patients = Patient_info.objects.all()
    return render(request, 'app/patient_list.html', {'patients': patients})

def database(request):
    models = UserPredictModel.objects.all()
    return render(request, 'app/img_database.html', {'models':models})

def matrix(request):
    return render(request,'app/matrix.html')


def logout_view(request):  
    auth_logout(request)
    return redirect('/')