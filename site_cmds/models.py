from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    """ Vérifie que le fichier a une extension valide. """
    allowed_extensions = ['.pdf', '.docx', '.txt', '.xlsx', '.png', '.jpg', '.jpeg', '.gif']
    ext = os.path.splitext(value.name)[1].lower()  # Récupère l'extension en minuscules
    if ext not in allowed_extensions:
        raise ValidationError("Seuls les formats de fichiers non audio/vidéo sont autorisés (PDF, DOCX, TXT, images, etc.).")

class UploadedFile(models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField(upload_to='Dld/', validators=[validate_file_extension])
    uploaded_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Tronque le nom du fichier à 5 caractères avant d'enregistrer """
        file_name, file_extension = os.path.splitext(self.file.name)
        if len(file_name) > 5:
            new_name = f"{file_name[:5]}{file_extension}"
            self.file.name = new_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
##################################################################################################
##################################################################################################
# Rapport de flux_entrée et sortie en document
from django.db import models

class Document(models.Model):
    date = models.DateField(unique=True)

    # Documents existants
    cobalt_intersite_existant = models.PositiveIntegerField(default=0)
    cobalt_transfert_existant = models.PositiveIntegerField(default=0)
    cuivre_intersite_existant = models.PositiveIntegerField(default=0)
    cuivre_transfert_existant = models.PositiveIntegerField(default=0)

    # Documents reçus
    cobalt_intersite_recu = models.PositiveIntegerField(default=0)
    cobalt_transfert_recu = models.PositiveIntegerField(default=0)
    cuivre_intersite_recu = models.PositiveIntegerField(default=0)
    cuivre_transfert_recu = models.PositiveIntegerField(default=0)

    # Documents sortis
    cobalt_intersite_sorti = models.PositiveIntegerField(default=0)
    cobalt_transfert_sorti = models.PositiveIntegerField(default=0)
    cuivre_intersite_sorti = models.PositiveIntegerField(default=0)
    cuivre_transfert_sorti = models.PositiveIntegerField(default=0)

    @property
    def cumulative_documents(self):
        return {
            'cobalt_intersite': self.cobalt_intersite_existant + self.cobalt_intersite_recu,
            'cobalt_transfert': self.cobalt_transfert_existant + self.cobalt_transfert_recu,
            'cuivre_intersite': self.cuivre_intersite_existant + self.cuivre_intersite_recu,
            'cuivre_transfert': self.cuivre_transfert_existant + self.cuivre_transfert_recu,
        }

    @property
    def remaining_documents(self):
        cum = self.cumulative_documents
        return {
            'cobalt_intersite': cum['cobalt_intersite'] - self.cobalt_intersite_sorti,
            'cobalt_transfert': cum['cobalt_transfert'] - self.cobalt_transfert_sorti,
            'cuivre_intersite': cum['cuivre_intersite'] - self.cuivre_intersite_sorti,
            'cuivre_transfert': cum['cuivre_transfert'] - self.cuivre_transfert_sorti,
        }

    def __str__(self):
        return f"Document - {self.date}"

#################################################################################################
#################################################################################################
# Rapport de la vente des documents
class Entrée(models.Model):
    date = models.DateField()

    # Entrées spécifiques
    doc_chinois_usd = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    div_chinois_cdf = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    doc_congolais_usd = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    div_congolais_cdf = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    frais_de_depot_cdf = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    def __str__(self):
        return f"Entrée - {self.date}"
#################################################################################################
#################################################################################################
#Rapport de la déclaration des documents
from django.db import models

class CoûtDocument(models.Model):  # Correction du nom de la classe
    date = models.DateField()

    cobalt_intersite_cost = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    cobalt_transfert_cost = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    cuivre_intersite_cost = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    cuivre_transfert_cost = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    unit_price_intersite = models.DecimalField(max_digits=10, decimal_places=0, editable=False, default=350)
    unit_price_transfert = models.DecimalField(max_digits=10, decimal_places=0, editable=False, default=1000)
    total_price_intersite = models.DecimalField(max_digits=15, decimal_places=0, editable=False, default=0)
    total_price_transfert = models.DecimalField(max_digits=15, decimal_places=0, editable=False, default=0)

    number_of_intersite_items = models.PositiveIntegerField(default=0, editable=False)
    number_of_transfert_items = models.PositiveIntegerField(default=0, editable=False)
    total_number_of_items = models.PositiveIntegerField(default=0, editable=False)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        self.calculate_item_counts_and_totals()
        super(CoûtDocument, self).save(*args, **kwargs)  # Correction du super()

    def calculate_item_counts_and_totals(self):
        # Calcul du nombre d'items intersite et transfert
        self.number_of_intersite_items = int(self.cobalt_intersite_cost + self.cuivre_intersite_cost)
        self.number_of_transfert_items = int(self.cobalt_transfert_cost + self.cuivre_transfert_cost)

        # Calcul des prix totaux intersite et transfert
        self.total_price_intersite = self.number_of_intersite_items * self.unit_price_intersite
        self.total_price_transfert = self.number_of_transfert_items * self.unit_price_transfert

        # Calcul du nombre total d'items et du prix total
        self.total_number_of_items = self.number_of_intersite_items + self.number_of_transfert_items
        self.total_price = self.total_price_intersite + self.total_price_transfert  # Correction de l'erreur de syntaxe

    def __str__(self):
        return f"Déclaration du {self.date} - Total: {self.total_price} CDF"


#################################################################################################
#################################################################################################
#Rapport des decaissements
from django.db import models
from datetime import datetime

class Décaissement(models.Model):
    TRESORIER_CHOICES = [
        ('KASONGO', 'Kasongo'),
        ('TSHITSHI', 'Tshitshi'),
    ]

    date = models.DateField()
    tresorier = models.CharField(max_length=10, choices=TRESORIER_CHOICES)
    reference = models.CharField(max_length=50, unique=True, blank=True)
    motif = models.CharField(max_length=1000, blank=False, default="Motif inconnu")
    amount_usd = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    amount_cdf = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    def save(self, *args, **kwargs):
        if not self.reference:
            today = datetime.now().date()
            last_reference = Décaissement.objects.filter(date=today).order_by('-reference').first()

            if last_reference:
                last_number = int(last_reference.reference.split('/')[0])
                new_number = last_number + 1
            else:
                new_number = 1

            month = today.month
            year = today.year % 100

            self.reference = f"{new_number:03d}/DEC/{month:02d}/{year:02d}"

            # Ensure the reference is unique
            while Décaissement.objects.filter(reference=self.reference).exists():
                new_number += 1
                self.reference = f"{new_number:03d}/DEC/{month:02d}/{year:02d}"

        super(Décaissement, self).save(*args, **kwargs)

    def __str__(self):
        return f"Décaissement {self.reference} - {self.amount_usd} USD / {self.amount_cdf} CDF"


#################################################################################################
#################################################################################################
from django.db import models

class DecaissementReference(models.Model):
    numero = models.IntegerField(unique=True)
    numero_reference = models.CharField(max_length=255, unique=True)
    date = models.DateField()  # Assurez-vous qu'il est bien là
    tresorier = models.CharField(max_length=100)

    def __str__(self):
        return self.numero_reference


#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################


##################################################################################################
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=5000)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # ✅ Champ pour savoir si le message est lu
    date_sent = models.DateTimeField(auto_now_add=True)  # ✅ Champ pour la date et l'heure d'envoi du message

    def __str__(self):
        return f"{self.email} - {self.subject}"

