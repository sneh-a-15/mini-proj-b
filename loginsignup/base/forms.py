from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CreateUserForm(UserCreationForm):
    fname = forms.CharField(max_length=30, required=False, help_text="")
    lname = forms.CharField(max_length=30, required=False, help_text="")
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=15, required=False)
    dob = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    class Meta:
        model = get_user_model()
        fields = ['fname', 'lname', 'email', 'phone', 'dob', 'gender', 'password1', 'password2']

    def save(self, commit=True):
        #print("D")
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.phone_number = self.cleaned_data['phone']
        user.birth_date = self.cleaned_data['dob']
        user.gender = self.cleaned_data['gender']

        user.username = self.cleaned_data['email']
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
        return user


class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)   