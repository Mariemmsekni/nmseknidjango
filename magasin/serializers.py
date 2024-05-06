from rest_framework.serializers import ModelSerializer
from magasin.models import Categorie,Produits
class CategorySerializer(ModelSerializer):
    class Meta:
      model = Categorie
      fields = ['id', 'name']

class ProduitSerializer(ModelSerializer):
    class Meta:
         model = Produits
         fields = ['libelle', 'description', 'categorie','type']