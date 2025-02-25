from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmez le mot de passe")

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un compte avec cet email existe déjà.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        if not re.search(r'[A-Z]{4,}', password):
            raise ValidationError("Le mot de passe doit contenir au moins 4 lettres majuscules.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")
        if not re.search(r'\d', password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

###############################################################################################################
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label="Adresse e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')


###############################################################################################################

from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du fichier'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
######################################################################################################
from django import forms
from .models import Document
from datetime import date

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'  # Inclut tous les champs du modèle

    # Configuration du champ de date avec format compatible HTML5
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],  # Format attendu : année-mois-jour
        widget=forms.DateInput(
            format='%Y-%m-%d', 
            attrs={'placeholder': 'JJ-MM-AAAA', 'type': 'date'}
        ),
    )

    def clean_date(self):
            date_entree = self.cleaned_data['date']
            date_min = date(2010, 1, 1)
            date_max = date.today()

            if date_entree < date_min:
                raise forms.ValidationError("La date d'entrée ne peut pas être antérieure à 2010.")
            if date_entree > date_max:
                raise forms.ValidationError("La date d'entrée ne peut pas être dans le futur.")
            if Document.objects.filter(date=date_entree).exists():
                raise forms.ValidationError("Un document avec cette date existe déjà.")

            return date

#####################################################################################################
#####################################################################################################
from django import forms
from datetime import date  # Import correct
from .models import Entrée, Document  # Vérifie que `Document` est bien défini

class EntréeForm(forms.ModelForm):
    class Meta:
        model = Entrée
        fields = '__all__'  # Inclut tous les champs du modèle

    # Configuration du champ de date avec format compatible HTML5
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],  # Format attendu : année-mois-jour
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'placeholder': 'AAAA-MM-JJ', 'type': 'date'}
        ),
    )

    def clean_date(self):
        date_entree = self.cleaned_data['date']
        date_min = date(2010, 1, 1)
        date_max = date.today()

        if date_entree < date_min:
            raise forms.ValidationError("La date d'entrée ne peut pas être antérieure à 2010.")
        if date_entree > date_max:
            raise forms.ValidationError("La date d'entrée ne peut pas être dans le futur.")
        
        # Vérifier si un document avec cette date existe déjà
        if Document.objects.filter(date=date_entree).exists():
            raise forms.ValidationError("Un document avec cette date existe déjà.")

        return date_entree  # ✅ Retourne `date_entree` au lieu de `date`

    def clean(self):
        cleaned_data = super().clean()
        for field in ['doc_chinois_usd', 'div_chinois_cdf', 'doc_congolais_usd', 'div_congolais_cdf', 'frais_de_depot_cdf']:
            if cleaned_data.get(field, 0) < 0:
                self.add_error(field, "Le montant ne peut pas être négatif.")
        return cleaned_data

#####################################################################################################
#####################################################################################################
from django import forms
from .models import CoûtDocument  # Correction du nom de classe

class CoûtDocumentForm(forms.ModelForm):
    class Meta:
        model = CoûtDocument
        fields = '__all__'  # Inclut tous les champs du modèle

    # Champ de date formaté pour HTML5
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d', 
            attrs={'placeholder': 'JJ-MM-AAAA', 'type': 'date'}
        ),
    )

    def clean_date(self):
            date_entree = self.cleaned_data['date']  # Récupération correcte de la date
            date_min = date(2010, 1, 1)
            date_max = date.today()

            if date_entree < date_min:
                raise forms.ValidationError("La date d'entrée ne peut pas être antérieure à 2010.")
            if date_entree > date_max:
                raise forms.ValidationError("La date d'entrée ne peut pas être dans le futur.")
            if CoûtDocument.objects.filter(date=date_entree).exists():  # Correction du modèle utilisé
                raise forms.ValidationError("Un document avec cette date existe déjà.")

            return date_entree  # 🔥 Retourner `date_entree` au lieu de `date`

    def clean(self):
        cleaned_data = super().clean()
        for field in ['cobalt_intersite_cost', 'cobalt_transfert_cost', 'cuivre_intersite_cost', 'cuivre_transfert_cost']:
            if cleaned_data.get(field, 0) < 0:
                self.add_error(field, "Le coût ne peut pas être négatif.")
        return cleaned_data

#####################################################################################################
#####################################################################################################
from django import forms
from .models import Décaissement
from datetime import date

class DécaissementForm(forms.ModelForm):
    class Meta:
        model = Décaissement
        fields = ['date', 'tresorier', 'motif', 'amount_usd', 'amount_cdf']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'placeholder': 'JJ-MM-AAAA',
                    'type': 'date',
                }
            ),
            'tresorier': forms.Select(attrs={'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amount_usd': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount_cdf': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Champ date avec validation personnalisée
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'placeholder': 'JJ-MM-AAAA',
                'type': 'date',
            }
        ),
    )

    def clean_date(self):
        """Validation pour s'assurer que la date est entre 2010 et aujourd'hui"""
        date_saisie = self.cleaned_data.get('date')
        date_min = date(2010, 1, 1)
        date_max = date.today()

        if date_saisie < date_min or date_saisie > date_max:
            raise forms.ValidationError(f"La date doit être comprise entre {date_min.strftime('%d-%m-%Y')} et aujourd'hui ({date_max.strftime('%d-%m-%Y')}).")

        return date_saisie

#####################################################################################################
#####################################################################################################


#####################################################################################################
#####################################################################################################


#####################################################################################################
#####################################################################################################
from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Votre Nom', 
                'id': 'name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Votre Email', 
                'id': 'email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Objet', 
                'id': 'subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Laissez un message ici', 
                'id': 'message',
                'style': 'height: 150px;'
            }),
        }



