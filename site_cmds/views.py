from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from .models import UploadedFile
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm  # Assurez-vous d'importer votre formulaire correctement
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import get_object_or_404, redirect
from site_cmds.models import UploadedFile
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Document, Entrée, CoûtDocument, Décaissement
from .forms import DocumentForm, EntréeForm, CoûtDocumentForm, DécaissementForm, UploadFileForm


# Main

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'main/about.html')

def booking(request):
    return render(request, 'main/booking.html')

def service(request):
    return render(request, 'main/service.html')
#############################################################################################
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactForm

# Vue pour gérer le formulaire de contact
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('main/contact')  # Redirige vers la même page pour vider le formulaire
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier vos informations.")
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})

# Vue pour afficher les messages enregistrés
def list_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'list_messages.html', {'messages_list': messages_list})

# Vue pour afficher un message en détail
def message_detail(request, message_id):
    message = ContactMessage.objects.get(id=message_id)
    return render(request, 'message_detail.html', {'message': message})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ContactMessage

def delete_message(request, message_id):
    """ Vue pour supprimer un message via AJAX """
    if request.method == "POST":
        message = get_object_or_404(ContactMessage, id=message_id)
        message.delete()
        return JsonResponse({"success": True})  # Retourne une réponse JSON
    return JsonResponse({"success": False, "error": "Requête invalide"})


#############################################################################################
def plus1(request):
    return render(request, 'service/plus1.html')
def plus2(request):
    return render(request, 'service/plus2.html')
def plus3(request):
    return render(request, 'service/plus3.html')
def plus4(request):
    return render(request, 'service/plus4.html')
def plus5(request):
    return render(request, 'service/plus5.html')
def plus6(request):
    return render(request, 'service/plus6.html')
##############################################################################################


def team(request):
    return render(request, 'main/team.html')

def testimonial(request):
    return render(request, 'main/testimonial.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

################################################################################################
################################################################################################
# Gestion

def gestion(request):
    return render(request, 'ges_connect/gestion.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Créez l'utilisateur sans l'enregistrer tout de suite
            user.set_password(form.cleaned_data['password'])  # Définit le mot de passe de l'utilisateur
            user.save()  # Enregistre l'utilisateur dans la base de données
            
            # Spécifiez le backend à utiliser
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)  # Connectez l'utilisateur
            
            return redirect('login')  # Redirigez l'utilisateur vers la page d'accueil ou une autre vue
    else:
        form = RegisterForm()  # Affichez un formulaire vide pour une nouvelle requête

    return render(request, 'ges_connect/register.html', {'form': form})  # Renvoyez le formulaire au template

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('acces')  # Remplacez 'acces' par le nom de votre vue de redirection
            else:
                form.add_error(None, "Adresse e-mail ou mot de passe incorrect")
    else:
        form = LoginForm()
    return render(request, 'ges_connect/login.html', {'form': form})

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')


from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')  # Redirige vers la page de connexion

######################################################################################
######################################################################################
#Acces
from django.contrib.auth.decorators import login_required
@login_required
def acces_view(request):
    return render(request, 'acces.html')

def ress_hum_view(request):
    return render(request, 'ress_hum.html')

def ges_adm_view(request):
    return render(request, 'ges_adm.html')
######################################################################################
######################################################################################

def pj_view(request):
    return render(request, 'pj.html')

def ges_fin_view(request):
    return render(request, 'ges_fin.html')

def comp_view(request):
    return render(request, 'comp.html')

######################################################################################
######################################################################################

####################################################################################
#####################################################################################
from django.shortcuts import render
from .forms import UploadFileForm  # Assurez-vous que ce formulaire existe

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UploadFileForm()
    
    return render(request, 'files/upload_file.html', {'form': form})  # Vérifiez bien ce chemin
######################################################################################
def file_list_view(request):
    files = UploadedFile.objects.all()
    return render(request, 'files/file_list.html', {'files': files})  
######################################################################################
def delete_file_view(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file.delete()
    return redirect('file_list')
######################################################################################
######################################################################################
#####################################################################################
######################################################################################    
######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################   
######################################################################################
######################################################################################
######################################################################################


######################################################################################
######################################################################################
######################################################################################
def r_flux(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            # Vérifiez si un document avec cette date existe déjà
            if Document.objects.filter(date=date).exists():
                messages.error(request, "Un document avec cette date existe déjà.")
            else:
                form.save()
                messages.success(request, "Données enregistrées avec succès !")
                return redirect('comptabilité/r_flux')
        else:
            messages.error(request, "Erreur !!! Veuillez vérifier les champs.")
    else:
        form = DocumentForm()

    forms = Document.objects.all().order_by('date')

    return render(request, 'comptabilité/r_flux.html', {'form': form, 'forms': forms})
######################################################################################
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Document

def r_flux_detail(request, date):
    try:
        # Récupère un seul document basé sur la date
        document = get_object_or_404(Document, date=date)
    except Document.MultipleObjectsReturned:
        messages.error(request, "Plusieurs documents existent pour cette date. Veuillez corriger les doublons.")
        return redirect('comptabilité/doc_sum')
    except Document.DoesNotExist:
        messages.error(request, "Aucun document trouvé pour cette date.")
        return redirect('comptabilité/r_flux')

    # Passe l'objet document au template
    return render(request, 'comptabilité/r_flux_detail.html', {'form': document})
######################################################################################
def delete_r_flux(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.delete()
        return redirect('comptabilité/r_flux')  # Redirige après suppression
    
    return render(request, 'comptabilité/r_flux_confirm_delete.html', {'document': document})

######################################################################################
######################################################################################
######################################################################################
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Entrée
from .forms import EntréeForm

def r_vente(request):
    if request.method == 'POST':
        form = EntréeForm(request.POST)
        
        if form.is_valid():  # Vérifie d'abord si le formulaire est valide
            date = form.cleaned_data['date']  # Maintenant, on peut accéder aux données nettoyées

            # Vérifie si un document avec cette date existe déjà
            if Entrée.objects.filter(date=date).exists():
                messages.error(request, "Un document avec cette date existe déjà.")
            else:
                form.save()  # Enregistre l'entrée dans la base de données
                messages.success(request, "Données enregistrées avec succès !")
                return redirect('comptabilité/r_vente')  # Redirige après enregistrement
        else:
            messages.error(request, "Erreur !!! Veuillez vérifier les champs.")
    else:
        form = EntréeForm()

    # Récupérer toutes les entrées classées par date
    forms = Entrée.objects.all().order_by('date')

    return render(request, 'comptabilité/r_vente.html', {'form': form, 'forms': forms})

######################################################################################
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Document, Entrée

def r_vente_detail(request, date):
    try:
        # Récupère un seul document basé sur la date
        entrée = get_object_or_404(Entrée, date=date)
    except Entrée.MultipleObjectsReturned:
        messages.error(request, "Plusieurs documents existent pour cette date. Veuillez corriger les doublons.")
        return redirect('comptabilité/doc_sum')
    except Entrée.DoesNotExist:
        messages.error(request, "Aucun document trouvé pour cette date.")
        return redirect('comptabilité/r_vente')

    # Passe l'objet document au template
    return render(request, 'comptabilité/r_vente_detail.html', {'form': entrée})
######################################################################################
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Entrée

def delete_r_vente(request, pk):
    entrée = get_object_or_404(Entrée, pk=pk)
    
    if request.method == 'POST':  # Vérifie si la méthode est bien POST
        entrée.delete()
        return redirect('comptabilité/r_vente')  # Vérifie que ce nom existe bien

    return render(request, 'comptabilité/r_vente_confirm_delete.html', {'entrée': entrée})

######################################################################################
######################################################################################

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CoûtDocumentForm
from .models import CoûtDocument

def declaration(request):
    if request.method == 'POST':
        form = CoûtDocumentForm(request.POST)
        
        if form.is_valid():
            date = form.cleaned_data.get('date')  # 🔥 `date` est déjà un `datetime.date`, pas besoin de conversion
            
            if CoûtDocument.objects.filter(date=date).exists():
                messages.error(request, "Une déclaration avec cette date existe déjà.")
            else:
                form.save()
                messages.success(request, "Données enregistrées avec succès !")
                return redirect('comptabilité/declaration')
        else:
            messages.error(request, "Erreur !!! Veuillez vérifier les champs.")
    else:
        form = CoûtDocumentForm()

    forms = CoûtDocument.objects.all().order_by('date')

    return render(request, 'comptabilité/declaration.html', {'form': form, 'forms': forms})

######################################################################################
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import CoûtDocument

from django.shortcuts import render, get_object_or_404
from .models import CoûtDocument

def declaration_detail(request, pk):
    declaration = get_object_or_404(CoûtDocument, pk=pk)
    return render(request, 'comptabilité/declaration_detail.html', {'declaration': declaration})

######################################################################################
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CoûtDocument

# Code de suppression sécurisé (peut être stocké en BD)
DELETE_CODE = "1234"

def delete_declaration(request, pk):
    declaration = get_object_or_404(CoûtDocument, pk=pk)

    if request.method == "POST":
        entered_code = request.POST.get("delete_code", "")

        if entered_code == DELETE_CODE:
            declaration.delete()
            messages.success(request, "Déclaration supprimée avec succès.")
        else:
            messages.error(request, "Code de suppression incorrect !")

    return redirect('comptabilité/declaration')
######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################
######################################################################################
from django.shortcuts import render
from .models import Document

def summary_view(request):
    forms = Document.objects.all().order_by('-date')  # Récupère tous les documents
    return render(request, 'comptabilité/summary.html', {'forms': forms})

######################################################################################
######################################################################################
######################################################################################
######################################################################################
from django.shortcuts import render, redirect, get_object_or_404
from .models import Décaissement
from .forms import DécaissementForm

# 🟢 Liste des décaissements
def liste(request):
    decaissements = Décaissement.objects.all().order_by('-date', '-reference')
    return render(request, 'comptabilité/liste.html', {'decaissements': decaissements})

# 🟢 Ajouter un décaissement
from django.shortcuts import render, redirect
from .models import Décaissement
from .forms import DécaissementForm

def ajouter(request):
    if request.method == "POST":
        form = DécaissementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comptabilité/liste')
    else:
        form = DécaissementForm()
    return render(request, 'comptabilité/ajouter.html', {'form': form})

# 🟢 Modifier un décaissement
def modifier(request, pk):
    decaissement = get_object_or_404(Décaissement, pk=pk)
    if request.method == "POST":
        form = DécaissementForm(request.POST, instance=decaissement)
        if form.is_valid():
            form.save()
            return redirect('comptabilité/liste')
    else:
        form = DécaissementForm(instance=decaissement)
    return render(request, 'comptabilité/modifier.html', {'form': form, 'decaissement': decaissement})

# 🟢 Supprimer un décaissement
def supprimer_dec(request, pk):
    decaissement = get_object_or_404(Décaissement, pk=pk)
    if request.method == "POST":
        decaissement.delete()
        return redirect('comptabilité/liste')
    return render(request, 'comptabilité/supprimer_dec.html', {'decaissement': decaissement})

from .models import Décaissement

def rechercher_decaissements(request):
    date = request.GET.get('date')
    tresorier = request.GET.get('tresorier')

    decaissements = Décaissement.objects.all()

    if date:
        decaissements = decaissements.filter(date=date)
    if tresorier:
        decaissements = decaissements.filter(tresorier=tresorier)  # ✅ Pas de tresorier__nom car c'est un CharField

    return render(request, 'comptabilité/liste.html', {
        'decaissements': decaissements,
        'TRESORIER_CHOICES': Décaissement.TRESORIER_CHOICES  # ✅ Ajout des choix au contexte
    })


def detail_decaissement(request, pk):
    decaissement = get_object_or_404(Décaissement, pk=pk)
    return render(request, 'comptabilité/detail_decaissement.html', {'decaissement': decaissement})

from django.shortcuts import render
from django.db.models import Q
from .models import Décaissement  # ✅ Assurez-vous que votre modèle est bien importé

def filter_decaissements(request):
    date_filter = request.GET.get('date', '')  # ✅ Ajout d'une valeur par défaut vide
    tresorier_filter = request.GET.get('tresorier', '')

    # ✅ Appliquer un filtrage simultané si les deux valeurs sont fournies
    filters = Q()
    if date_filter:
        filters &= Q(date=date_filter)
    if tresorier_filter:
        filters &= Q(tresorier=tresorier_filter)

    decaissements = Décaissement.objects.filter(filters)

    # ✅ Récupérer dynamiquement la liste des trésoriers uniques depuis la base de données
    TRESORIER_CHOICES = Décaissement.objects.values_list('tresorier', 'tresorier').distinct()

    return render(request, 'comptabilité/liste.html', {
        'decaissements': decaissements,
        'TRESORIER_CHOICES': TRESORIER_CHOICES,
        'selected_date': date_filter,  # ✅ Pour conserver la valeur saisie
        'selected_tresorier': tresorier_filter
    })


######################################################################################
from django.shortcuts import render
from .models import Décaissement

def resultats_filtre(request):
    date = request.GET.get('date')
    tresorier = request.GET.get('tresorier')

    # Filtrer uniquement si les deux valeurs sont présentes
    if date and tresorier:
        decaissements = Décaissement.objects.filter(date=date, tresorier=tresorier)
    else:
        decaissements = Décaissement.objects.none()  # Aucune donnée si un des champs est vide

    return render(request, 'comptabilité/resultats_filtre.html', {'decaissements': decaissements})


######################################################################################
######################################################################################
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.shortcuts import get_list_or_404
from .models import Décaissement
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from num2words import num2words
from datetime import datetime
from .models import DecaissementReference

def generate_pdf_décaissement(request):
    date_filter = request.GET.get('date', None)
    tresorier_filter = request.GET.get('tresorier', None)

    # Filtrer les décaissements
    decaissements = Décaissement.objects.all()
    if date_filter:
        decaissements = decaissements.filter(date=date_filter)
    if tresorier_filter:
        decaissements = decaissements.filter(tresorier=tresorier_filter)

    if not decaissements.exists():
        return HttpResponse("Aucun décaissement trouvé pour ces critères.", status=404)
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  # Dimensions du PDF

    # Définition des marges
    BOTTOM_MARGIN = 100  # Marge en bas de la page

    # Position initiale pour le texte
    y = 800  # Première page commence à 800

    # Variables pour la gestion des pages
    page_number = 1
    is_first_page = True  # Indicateur pour la première page

    ### **1. En-tête du document**
    def draw_header():
        nonlocal y  # Pour modifier y globalement
        c.setFont("Times-Bold", 16)
        c.setFillColorRGB(0, 0, 0)  # Noir
        text_width = c.stringWidth("REPUBLIQUE DEMOCRATIQUE DU CONGO", "Times-Bold", 16)
        c.drawString((A4[0] - text_width) / 2, y, "REPUBLIQUE DEMOCRATIQUE DU CONGO")
        y -= 20

        c.setFont("Times-Bold", 12)
        c.setFillColorRGB(1, 0, 0)  # Rouge
        text_width = c.stringWidth("PROVINCE DU LUALABA", "Times-Bold", 12)
        c.drawString((A4[0] - text_width) / 2, y, "PROVINCE DU LUALABA")
        y -= 20

        c.setFont("Times-Bold", 13)
        c.setFillColorRGB(0, 0, 1)  # Bleu
        text_width = c.stringWidth("SOCIETE COOPERATIVE MINIERE POUR LE DEVELOPPEMENT ET LE SOCIAL", "Times-Bold", 13)
        c.drawString((A4[0] - text_width) / 2, y, "SOCIETE COOPERATIVE MINIERE POUR LE DEVELOPPEMENT ET LE SOCIAL")
        y -= 20

        c.setFillColorRGB(0, 0, 0)  # Noir
        c.setFont("Times-Bold", 14)
        text_width = c.stringWidth("CMDS COOP-CA", "Times-Bold", 14)
        c.drawString((A4[0] - text_width) / 2, y, "CMDS COOP-CA")
        text_width = c.stringWidth("_________________________________________________________________", "Times-Bold", 14)
        c.drawString((A4[0] - text_width) / 2, y, "_________________________________________________________________")
        y -= 40

    draw_header()       
    ### **2. Titre du document**
    
    # Définition de la police pour le titre
    c.setFont("Times-Bold", 13)

    # Formater la date
    formatted_date = datetime.strptime(date_filter, "%Y-%m-%d").strftime("%d/%m/%Y") if date_filter else "PERIODE SELECTIONNÉE"

    # Obtenir le mois et l'année en format requis
    mois_execution = datetime.strptime(date_filter, "%Y-%m-%d").strftime("%m") if date_filter else "XX"
    annee_execution = datetime.strptime(date_filter, "%Y-%m-%d").strftime("%y") if date_filter else "XX"

    # Vérifier si un numéro de référence existe déjà pour la date et le trésorier
    existing_ref = DecaissementReference.objects.filter(date=date_filter, tresorier=tresorier_filter).first()

    if existing_ref:
        # Si un numéro de référence existe déjà, on le réutilise
        numero_reference = existing_ref.numero_reference
    else:
        # Sinon, générer un nouveau numéro
        last_ref = DecaissementReference.objects.order_by('-id').first()
        new_number = last_ref.numero + 1 if last_ref else 1  # Si aucun enregistrement, commencer à 1

        # Génération automatique du numéro de référence
        numero_reference = f"{new_number:03d}/DEC/DFI-DG/{mois_execution}/{annee_execution}"

        # Enregistrer la nouvelle référence dans la base de données
        new_ref = DecaissementReference(numero=new_number, numero_reference=numero_reference, date=date_filter, tresorier=tresorier_filter)
        new_ref.save()

    # Titre principal
    title_main = f"LETTRE DE DECAISSEMENT DU {formatted_date}"

    # Sous-titre (numéro de référence)
    title_sub = f"enregistrée sous le numéro de référence : {numero_reference}"

    # Calcul et affichage du titre principal (centré)
    text_width_main = c.stringWidth(title_main, "Times-Bold", 13)
    c.drawString((A4[0] - text_width_main) / 2, y, title_main)

    # Affichage du sous-titre (centré en rouge sous le titre principal)
    c.setFillColorRGB(1, 0, 0)  # Rouge
    text_width_sub = c.stringWidth(title_sub, "Times-Bold", 13)
    c.drawString((A4[0] - text_width_sub) / 2, y - 15, title_sub)
    c.setFillColorRGB(0, 0, 0)  # Remettre en noir après

    # Ajustement de la position verticale
    y -= 30

    ### **3. Titre du document**
    c.setFont("Times-Bold", 13)
    title = f"A l'intention du trésorier {tresorier_filter if tresorier_filter else 'CAISSE DE LA CMDS COOP-CA'}"
    text_width = c.stringWidth(title, "Times-Bold", 13)
    c.drawString((A4[0] - text_width) / 2, y, title)
    y -= 25

    # Initialisation des totaux avant de les utiliser
    total_usd = sum(decaissement.amount_usd for decaissement in decaissements)
    total_cdf = sum(decaissement.amount_cdf for decaissement in decaissements)

    # Formater les montants en nombre avec le séparateur de milliers "."
    total_usd_str = f"{total_usd:,.0f}".replace(",", ".") + " USD"
    total_cdf_str = f"{total_cdf:,.0f}".replace(",", ".") + " CDF"

    # Convertir les montants en lettres avec une majuscule sur chaque mot
    total_usd_letters = " ".join(word.capitalize() for word in num2words(total_usd, lang='fr').split())
    total_cdf_letters = " ".join(word.capitalize() for word in num2words(total_cdf, lang='fr').split())

    # Texte du titre avec les montants en gras et rouge
    title = (
        "En vertu des pouvoirs qui nous sont conférés par nos Statuts et notre Règlement d’Ordre Intérieur, "
        "ainsi que conformément aux nouvelles dispositions en vigueur, moi, Vice-Président Chargé des Finances, " 
        "en collaboration avec le Directeur Général, autorisons par la présente le décaissement d’un montant total de "
        f"<b><font color='red'>{total_usd_str} ({total_usd_letters} Dollars Américains)</font></b> "
        "et de "
        f"<b><font color='red'>{total_cdf_str} ({total_cdf_letters} Francs Congolais)</font></b>, "
        "détaillé ci-dessous :"
    )
    # Définir la largeur maximale du texte pour respecter les marges
    max_width = A4[0] - 100  # Marge de 50 à gauche et à droite

    # Styles pour le texte du titre
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        name="Justified",
        fontName="Times-Roman",
        fontSize=13,
        leading=15,
        alignment=4,  # Texte justifié
    )

    # Création d'un paragraphe
    paragraph = Paragraph(title, style)

    # Vérifier la position y
    if y < 100:  # Évite que le texte soit trop bas
        y = 700  # Remet à une hauteur raisonnable

    # Affichage du texte
    paragraph.wrapOn(c, max_width, y)
    paragraph.drawOn(c, 50, y - paragraph.height)

    # Ajustement pour que le tableau ne chevauche pas
    y -= paragraph.height + 15  # Ajuste cette valeur si nécessaire

    ### **5. Création des details de décaissement**
    ###############################################
    c.setFont("Times-Roman", 14)

    # Définition des marges
    left_margin = 50
    right_margin = 50
    max_width = A4[0] - left_margin - right_margin  # Largeur max du texte

    # Ajuster y pour s'assurer que les détails restent visibles
    if y < 120:  # Éviter que y soit trop bas
        y = 120  

    # Style du texte
    style = ParagraphStyle(
        name="DecaissementStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=16,  # Ajuster l'espace entre les lignes
        alignment=4,  # Justifié,
    )

    # Afficher chaque décaissement sous forme de texte
    for decaissement in decaissements:
        amount_usd_formatted = f"{decaissement.amount_usd:,.0f}".replace(",", ".")
        amount_cdf_formatted = f"{decaissement.amount_cdf:,.0f}".replace(",", ".")

        ligne = (
            f"<b><font color='blue'>Réf: {decaissement.reference}</font></b> | "
            f"Montant: <b><font color='black'>{amount_usd_formatted} USD</font></b> et "
            f"<b><font color='black'>{amount_cdf_formatted} CDF</font></b> | "
            f"Motif: {decaissement.motif}"
        )

        paragraph = Paragraph(ligne, style)
        w, h = paragraph.wrap(max_width, 0)  # Obtenir la hauteur du texte formaté
        
        y -= h  # Déplacer y correctement en fonction de la hauteur du texte
        paragraph.drawOn(c, left_margin, y)  # Dessiner le texte

        y -= 6  # Espacement entre chaque ligne (ajuster selon le besoin)

        # Vérifier si on atteint le bas de la page
        if y < BOTTOM_MARGIN:
            c.showPage()  # Créer une nouvelle page
            y = 800  # Réinitialiser y pour la nouvelle page
            page_number += 1  # Incrémenter le numéro de page

            # Afficher le numéro de page (sauf sur la première page)
            if page_number > 1:
                c.setFont("Times-Roman", 10)
                c.drawString(width - 50, 20, f"Page {page_number}")  # Afficher en bas à droite

    # Texte de clôture
    text = "Tout en vous demandant d'enregistrer l'ensemble de décaissements effectués ci-dessus à la comptabilité et à la trésorerie, Nous vous prions d’accepter nos salutations."

    # Définir les marges
    left_margin = 50
    right_margin = 50
    max_width = A4[0] - left_margin - right_margin  # Largeur maximale du texte

    # Style pour le texte de clôture
    styles = getSampleStyleSheet()
    style = ParagraphStyle(
        name="ClotureStyle",
        fontName="Times-Roman",
        fontSize=12,
        leading=14,  # Espacement entre les lignes
        alignment=4,  # Texte justifié,
        leftIndent=0,  # Pas d'indentation à gauche
        rightIndent=0,  # Pas d'indentation à droite
    )

    # Créer un paragraphe avec le texte de clôture
    paragraph = Paragraph(text, style)

    # Calculer la hauteur du paragraphe
    paragraph.wrap(max_width, y)

    # Dessiner le paragraphe en respectant les marges
    paragraph.drawOn(c, left_margin, y - paragraph.height)

    # Ajuster la position y pour la suite du contenu
    y -= paragraph.height + 5  # Espacement supplémentaire après le texte de clôture
    
    # Signature
    text = "Pour la Société Coopérative"
    c.setFont("Times-Roman", 13)

    # Position du texte
    text_x = width / 2
    text_y = y - 40

    # Affichage du texte centré
    c.drawCentredString(text_x, text_y, text)

    # Calcul de la largeur du texte pour tracer la ligne en dessous
    text_width = c.stringWidth(text, "Times-Roman", 13)
    line_x_start = text_x - (text_width / 2)
    line_x_end = text_x + (text_width / 2)
    line_y = text_y - 2  # Ajuster légèrement la position de la ligne sous le texte

    # Dessiner la ligne sous le texte
    c.line(line_x_start, line_y, line_x_end, line_y)

    c.setFont("Times-Bold", 14)
    c.drawCentredString(width / 2, y - 60, "KATENGA KABOMBO Guelord")
    
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, y - 80, "Vice-Président Chargé des Finances")

    # Finaliser et fermer le PDF
    c.showPage()
    c.save()
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="decaissements.pdf"'
    return response




######################################################################################################
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate

def generate_pdf_document(request, form_id):
    form = get_object_or_404(Document, id=form_id)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    # Initialiser la variable 'y'
    y = 800

    def draw_header():
        # "République Démocratique du Congo" en noir
        c.setFont("Times-Bold", 16)
        c.setFillColorRGB(0, 0, 0)  # Noir
        text_width = c.stringWidth("REPUBLIQUE DEMOCRATIQUE DU CONGO", "Times-Bold", 16)
        c.drawString((A4[0] - text_width) / 2, 790, "REPUBLIQUE DEMOCRATIQUE DU CONGO")

        # "Province du Lualaba" en rouge
        c.setFont("Times-Bold", 12)
        c.setFillColorRGB(1, 0, 0)  # Rouge
        text_width = c.stringWidth("PROVINCE DU LUALABA", "Times-Bold", 12)
        c.drawString((A4[0] - text_width) / 2, 775, "PROVINCE DU LUALABA")

        # "Société Coop" en bleu
        c.setFont("Times-Bold", 13)
        c.setFillColorRGB(0, 0, 1)  # Bleu
        text_width = c.stringWidth("SOCIETE COOPERATIVE MINIERE POUR LE DEVELOPPEMENT ET LE SOCIAL", "Times-Bold", 13)
        c.drawString((A4[0] - text_width) / 2, 755, "SOCIETE COOPERATIVE MINIERE POUR LE DEVELOPPEMENT ET LE SOCIAL")

        c.setFillColorRGB(0, 0, 0)  # Noir
        c.setFont("Times-Bold", 14)
        text_width = c.stringWidth("CMDS COOP-CA", "Times-Bold", 14)
        c.drawString((A4[0] - text_width) / 2, 735, "CMDS COOP-CA")

    # En-tête
    draw_header()

    # Titre principal
    c.setFont("Times-Bold", 13)
    title = f"RAPPORT JOURNALIER DU {form.date.strftime('%d/%m/%Y')}"
    text_width = c.stringWidth(title, "Times-Bold", 13)
    c.drawString((A4[0] - text_width) / 2, 710, title)

    #######################################################################################################
    # Section "Flux d'entrée et de sortie des documents"
    c.setFont("Times-Bold", 13)
    text = "FLUX D'ENTREE ET DE SORTIE DES DOCUMENTS"
    text_width = c.stringWidth(text)  # Calcule la largeur du texte
    x_position = (A4[0] - text_width) / 2  # Centre le texte horizontalement

    # Dessine le texte à la position x calculée
    c.drawString(x_position, 680, text)

    # Données pour le tableau
    data_flux = [
        ['RUBRIQUE', 'Cobalt Intersite', 'Cobalt Transfert', 'Cuivre Intersite', 'Cuivre Transfert'],
        ['Existants', form.cobalt_intersite_existant, form.cobalt_transfert_existant, form.cuivre_intersite_existant, form.cuivre_transfert_existant],
        ['Reçus', form.cobalt_intersite_recu, form.cobalt_transfert_recu, form.cuivre_intersite_recu, form.cuivre_transfert_recu],
        ['Cumulés', form.cumulative_documents['cobalt_intersite'], form.cumulative_documents['cobalt_transfert'], form.cumulative_documents['cuivre_intersite'], form.cumulative_documents['cuivre_transfert']],
        ['Sorties', form.cobalt_intersite_sorti, form.cobalt_transfert_sorti, form.cuivre_intersite_sorti, form.cuivre_transfert_sorti],
        ['Restants', form.remaining_documents['cobalt_intersite'], form.remaining_documents['cobalt_transfert'], form.remaining_documents['cuivre_intersite'], form.remaining_documents['cuivre_transfert']],
    ]

    # Création et style du tableau
    table_flux = Table(data_flux, colWidths=[100] * 5)
    table_flux.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007bff")),  # En-tête bleu
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texte blanc dans l'en-tête
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f2f2f2"), colors.white]),  # Alternance des lignes
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#6c757d")),  # Bordures du tableau
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignement centré des cellules
        ('TEXTCOLOR', (1, 1), (-1, 1), colors.blue),  # Ligne "Existants" en bleu
        ('TEXTCOLOR', (1, 2), (-1, 2), colors.green),  # Ligne "Reçus" en vert
        ('TEXTCOLOR', (1, 3), (-1, 3), colors.black),  # Ligne "Cumulés" en noir
        ('TEXTCOLOR', (1, 4), (-1, 4), colors.red),  # Ligne "Sorties" en rouge
        ('TEXTCOLOR', (1, 5), (-1, 5), colors.blue),  # Ligne "Restants" en bleu
    ]))

    # Dessin du tableau
    x_position = 50
    y_position = 560
    table_flux.wrapOn(c, x_position, y_position)
    table_flux.drawOn(c, x_position, y_position)


    # Finalisation et enregistrement
    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="document.pdf"'

    return response
##################################################################################################
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate

def generate_pdf_coûtdocument(request, form_id):
    form = get_object_or_404(CoûtDocument, id=form_id)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    # Initialiser la variable 'y'
    y = 800

    def draw_header():
        # "République Démocratique du Congo" en noir
        c.setFont("Times-Bold", 16)
        c.setFillColorRGB(0, 0, 0)  # Noir
        text_width = c.stringWidth("REPUBLIQUE DEMOCRATIQUE DU CONGO", "Times-Bold", 16)
        c.drawString((A4[0] - text_width) / 2, 790, "REPUBLIQUE DEMOCRATIQUE DU CONGO")

        # "Province du Lualaba" en rouge
        c.setFont("Times-Bold", 12)
        c.setFillColorRGB(1, 0, 0)  # Rouge
        text_width = c.stringWidth("PROVINCE DU LUALABA", "Times-Bold", 12)
        c.drawString((A4[0] - text_width) / 2, 775, "PROVINCE DU LUALABA")

        # "Société Coop" en bleu
        c.setFont("Times-Bold", 13)
        c.setFillColorRGB(0, 0, 1)  # Bleu
        text_width = c.stringWidth("SOCIETE COOPERATIVE MINIERE POUR LE DEVELOPPEMENT ET LE SOCIAL", "Times-Bold", 13)
        c.drawString((A4[0] - text_width) / 2, 755, "SOCIETE COOPERATIVE MINIERE POUR LE DEVELOPPEMENT ET LE SOCIAL")

        c.setFillColorRGB(0, 0, 0)  # Noir
        c.setFont("Times-Bold", 14)
        text_width = c.stringWidth("CMDS COOP-CA", "Times-Bold", 14)
        c.drawString((A4[0] - text_width) / 2, 735, "CMDS COOP-CA")

    # En-tête
    draw_header()

    # Titre principal
    c.setFont("Times-Bold", 13)
    title = f"RAPPORT JOURNALIER DU {form.date.strftime('%d/%m/%Y')}"
    text_width = c.stringWidth(title, "Times-Bold", 13)
    c.drawString((A4[0] - text_width) / 2, 710, title)

    #######################################################################################################
    # Section "Flux d'entrée et de sortie des documents"
    c.setFont("Times-Bold", 13)
    text = "RAPPORTS 'DECLARATION DES DOCUMENTS'"
    text_width = c.stringWidth(text)  # Calcule la largeur du texte
    x_position = (A4[0] - text_width) / 2  # Centre le texte horizontalement

    # Dessine le texte à la position x calculée
    c.drawString(x_position, 680, text)

    # Coûts d'achat des documents' 
    c.setFont("Times-Bold", 13)
    text = "10. COÛT D'ACHAT DES DOCUMENTS"
    text_width = c.stringWidth(text)  # Calcule la largeur du texte
    x_position = (A4[0] - text_width) / 2  # Centre le texte horizontalement

    # Dessine le texte à la position x calculée
    c.drawString(x_position, 750, text)

    # Préparation des données pour le tableau
    data_achat = [
        ['RUBRIQUE','Cobalt Intersite', 'Cobalt Transfert', 'Cuivre Intersite', 'Cuivre Transfert'],
        ['Nombre', form.cobalt_intersite_cost, form.cobalt_transfert_cost, form.cuivre_intersite_cost, form.cuivre_transfert_cost]
    ]

    # Création du tableau
    table_flux = Table(data_achat, colWidths=[100, 100, 100, 100, 100])
    table_flux.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#fd7e14")),  # En-tête bleu
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texte blanc dans l'en-tête
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f2f2f2")),  # Couleur de fond des lignes
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f2f2f2"), colors.white]),  # Alternance de lignes
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#6c757d")),  # Bordures du tableau
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignement centré des cellules
    ]))

    # Positionnement du tableau
    x_position = 50
    y_position = 710
    table_flux.wrapOn(c, x_position, y_position)
    table_flux.drawOn(c, x_position, y_position)

    ####################################################################################################

    # Calcul_Coûts d'achat des documents' 
    c.setFont("Times-Bold", 13)
    text = "A. PRIX/COÛT D'ACHAT DES DOCUMENTS"
    text_width = c.stringWidth(text)  # Calcule la largeur du texte
    x_position = (A4[0] - text_width) / 2  # Centre le texte horizontalement

    # Dessine le texte à la position x calculée
    c.drawString(x_position, 690, text)

    # Préparation des données pour le tableau
    data_achat = [
        ['RUBRIQUE','Prix Unitaire Int.', 'Prix Unitaire Trs', 'Total Intersite', 'Total Transfert'],
        ['Prix', form.unit_price_intersite, form.unit_price_transfert, form.total_price_intersite, form.total_price_transfert]
    ]

    # Création du tableau
    table_flux = Table(data_achat, colWidths=[100, 100, 100, 100, 100])
    table_flux.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#fd7e14")),  # En-tête bleu
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texte blanc dans l'en-tête
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f2f2f2")),  # Couleur de fond des lignes
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f2f2f2"), colors.white]),  # Alternance de lignes
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#6c757d")),  # Bordures du tableau
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignement centré des cellules
    ]))

    # Positionnement du tableau
    x_position = 50
    y_position = 650
    table_flux.wrapOn(c, x_position, y_position)
    table_flux.drawOn(c, x_position, y_position)


    ##################################################################################################
    # Calcul_Coûts d'achat des documents' 
    c.setFont("Times-Bold", 13)
    text = "B. OPERATIONS D'ACHAT"
    text_width = c.stringWidth(text)  # Calcule la largeur du texte
    x_position = (A4[0] - text_width) / 2  # Centre le texte horizontalement

    # Dessine le texte à la position x calculée
    c.drawString(x_position, 630, text)

    # Préparation des données pour le tableau
    data_achat = [
        ['RUBRIQUE','Intersite', 'Transfert', 'Total Intersite', 'Total Transfert'],
        ['Nombre', form.number_of_intersite_items, form.number_of_transfert_items, form.total_number_of_items, form.total_price]
    ]

    # Création du tableau
    table_flux = Table(data_achat, colWidths=[100, 100, 100, 100, 100])
    table_flux.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#fd7e14")),  # En-tête bleu
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texte blanc dans l'en-tête
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f2f2f2")),  # Couleur de fond des lignes
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f2f2f2"), colors.white]),  # Alternance de lignes
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#6c757d")),  # Bordures du tableau
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignement centré des cellules
    ]))

    # Positionnement du tableau
    x_position = 50
    y_position = 590
    table_flux.wrapOn(c, x_position, y_position)
    table_flux.drawOn(c, x_position, y_position)


    # Finalisation et enregistrement
    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="coûtdocument.pdf"'

    return response

###########################################################################################


##############################################################################################
