from django.db import models
from datetime import date
from django.db.models import Sum
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
class Categorie(models.Model):
    TYPE_CHOICES = [
        ('Al', 'Alimentaire'),
        ('Mb', 'Meuble'),
        ('Sn', 'Sanitaire'),
        ('Vs', 'Vaisselle'),
        ('Vt', 'Vêtement'),
        ('Jx', 'Jouets'),
        ('Lg', 'Linge de Maison'),
        ('Bj', 'Bijoux'),
        ('Dc', 'Décor'),
        ('EL','Electromanager')
    ]

    name = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Alimentaire')

    def __str__(self):
        return self.get_name_display()
    
class Fournisseur(models.Model):
    nom=models.CharField(max_length=100)
    adresse=models.TextField()
    email=models.EmailField()
    telephone=models.CharField(max_length=8)  
    def __str__(self):
            return self.nom



class Produits(models.Model):
    libelle = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    TYPE_CHOICES = [
        ('em', 'emballé'),
        ('fr', 'Frais'),
        ('cs', 'Conserve')
    ]
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='em')
    img = models.ImageField(blank='True')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    Fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)





    def __str__(self):
     return f"{self.libelle} {self.description} {self.prix} {self.type}"
class ProduitNC(Produits):
    duree_garantie = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle
class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    produits = models.ManyToManyField('Produits')

    def __str__(self):
            return str(self.dateCde)
        
@receiver(m2m_changed, sender=Commande.produits.through)
def update_total_cde(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        total = instance.produits.aggregate(total=Sum('prix'))['total']
        instance.totalCde = total if total else 0
        instance.save()
class CartItem(models.Model):
    article = models.ForeignKey(Produits, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    

    
