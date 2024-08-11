from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput
from .models import User, Profile
from .function import traitementEmail, traitementTel
from django.contrib.auth import authenticate as django_authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control','type':'text','name': 'email',
                                       'placeholder':'E-mail'}),
                                label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class':'form-control','type':'password', 'name':'password1',
                                           'placeholder':'Mot de passe'}),
                                    label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'class':'form-control','type':'password', 'name': 'password2',
                                           'placeholder':'Confirmer'}),
                                    label="Password (again)")
    '''added attributes so as to customise for styling, like bootstrap'''
    class Meta:
        model = User
        fields = ['email','password1','password2']
        field_order = ['email','password1','password2']
        
    def clean(self):
        """
        Verifies that the values entered into the password fields match
        NOTE : errors here will appear in 'non_field_errors()'
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and 'email' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please try again!")
            else:
                if traitementEmail(self.cleaned_data['email']) == True:
                    pass
                else:
                    raise forms.ValidationError("Caractère non autorisé.")
        return self.cleaned_data
    
    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form): # Note: forms.Form NOT forms.ModelForm
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control','type':'text','name': 'email','placeholder':'E-mail'}),
                                label='Email')
    password = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class':'form-control','type':'password', 'name':
                                        'password','placeholder':'Password'}),
                                label='Password')
    
    class Meta:
        fields = ['email', 'password']
        
    def clean(self):
        cleaned_data = super(AuthenticationForm, self).clean()
        if 'password' in self.cleaned_data and 'email' in self.cleaned_data:
            if traitementEmail(self.cleaned_data['email']) == True:
                user = django_authenticate(email=self.cleaned_data['email'],
                                               password=self.cleaned_data['password'])
                if user is not None:
                    pass
                else:
                    raise forms.ValidationError("Donnée incorrecte.")
            else:
                raise forms.ValidationError("Caractère non autorisé.")
        return self.cleaned_data
        
        
        
class Edition_mailForm(forms.Form): # Note: forms.Form NOT forms.ModelForm
    email = forms.EmailField(widget=forms.TextInput(
                                attrs={'class': 'form-control','type':'email','name': 'email','placeholder':'E-mail'}),
                                label='Email', required=True)
    
    class Meta:
        fields = ['email']
        
    def clean(self):
        cleaned_data = super(Edition_mailForm, self).clean()
        if 'email' in self.cleaned_data:
            if traitementEmail(self.cleaned_data['email']) == True:
                pass
            else:
                raise forms.ValidationError('Caractères non autorisé.')
        return self.cleaned_data
        
        
        
class Edition_passwordForm(forms.Form): # Note: forms.Form NOT forms.ModelForm
    password = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class':'form-control','type':'password', 'name':
                                        'password','placeholder':'Mot de passe'}),
                                label='Password', required=True)
    newpassword = forms.CharField(widget=forms.PasswordInput(
                                attrs={'class':'form-control','type':'password', 'name':
                                        'newpassword','placeholder':'Nouveau mot de passe'}),
                                label='Password', required=True)
    
    class Meta:
        fields = ['password', 'newpassword']
        
        
        

class Profiles(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            "nom": TextInput(attrs={"placeholder":"Nom"}),
            "prenom": TextInput(attrs={"placeholder":"Prenom"}),
            "contact": TextInput(attrs={"type":"tel","placeholder":"Contact"}),
            "ville": TextInput(attrs={"list":"regions","placeholder":"Régions"}),
        }
    
    def clean(self):
        cleaned_data = super(Profiles, self).clean()
        if 'nom' in self.cleaned_data:
            if traitementEmail(self.cleaned_data['nom']) == True:
                pass
            else:
                raise forms.ValidationError('Caractères non autorisé.')
        if 'prenom' in self.cleaned_data:
            if traitementEmail(self.cleaned_data['prenom']) == True:
                pass
            else:
                raise forms.ValidationError('Caractères non autorisé.')
            
        if 'contact' in self.cleaned_data:
            if traitementTel(self.cleaned_data['contact']) == True:
                pass
            else:
                raise forms.ValidationError('Erreur ! Contact non autoriser.')
        return self.cleaned_data