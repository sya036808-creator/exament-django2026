from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser

# Formulaire personnalisé pour l'inscription (surcharge celui de allauth)
class CustomSignupForm(SignupForm):
    # Ajout des champs Prénom, Nom et Rôle qui ne sont pas par défaut dans allauth
    first_name = forms.CharField(max_length=30, label='Prénom')
    last_name = forms.CharField(max_length=30, label='Nom')
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label='Rôle')

    # Redéfinition de la méthode save pour enregistrer nos champs personnalisés
    def save(self, request):
        # Sauvegarde de base de l'utilisateur
        user = super(CustomSignupForm, self).save(request)
        # Attribution des nouvelles valeurs à l'utilisateur
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        # Enregistrement en base de données
        user.save()
        return user

# Formulaire pour la mise à jour du profil utilisateur
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Champs qui pourront être modifiés dans le profil
        fields = ['first_name', 'last_name', 'email', 'avatar']
        # Définition des widgets pour appliquer des classes CSS Bootstrap ('form-control')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
