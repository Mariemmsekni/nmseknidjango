
from .models import Produits
from .Forms import ProduitForm
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponseRedirect
from django.template import loader 
from .Forms import FournisseurForm
from .models import Fournisseur,Categorie,CartItem
from django.urls import reverse
from django.db.models import Q
from .Forms import CartItemForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .Forms import ProduitForm, FournisseurForm,UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.models import Categorie
from magasin.serializers import CategorySerializer
from magasin .serializers import ProduitSerializer
from rest_framework import viewsets


def index(request): 
    return render(request,'magasin/acceuil.html');

@login_required
def home(request):
    context = {'val': "Menu Acceuil"}
    return render(request, 'registration/home.html', context)
def vitrine(request):
    produits = Produits.objects.all()
    return render(request, 'magasin/vitrine.html', {'produits': produits})

def nouveauProduit(request):
    if request.method == "POST": 
        form = ProduitForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('magasin:vitrine'))
    else: 
        form = ProduitForm() 

    categories = Categorie.objects.all()
    fournisseurs = Fournisseur.objects.all()

    return render(request, 'magasin/majProduits.html', {'form': form, 'categories': categories, 'fournisseurs': fournisseurs})

def nouveauFournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('magasin:listFournisseur'))
    else:
        form = FournisseurForm()
        fournisseurs = Fournisseur.objects.all()
    return render(request, 'magasin/ajoutFour.html', {'form': form, 'fournisseurs': fournisseurs})
def listFournisseur(request):
    fournisseurs = Fournisseur.objects.all()  
    return render(request, 'magasin/Fournisseur.html', {'fournisseurs': fournisseurs})
def listProduit(request):
    produits = Produits.objects.all()  
    return render(request, 'magasin/mesProduits.html', {'produits': produits})

def search_view(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        articles = Produits.objects.filter(
            Q(libelle__icontains=search_query) |
            Q(description__icontains=search_query)
             
           
            
        )
        fournisseurs = Fournisseur.objects.filter(
            Q(nom__icontains=search_query) |
            Q(adresse__icontains=search_query) |
            Q(telephone__icontains=search_query) |
            Q(email__icontains=search_query)
        ).distinct()

    if articles.exists():
        return render(request, 'magasin/vitrine.html', {'list': articles})
    elif fournisseurs.exists():
        return render(request, 'magasin/Fournisseur.html', {'fournisseurs': fournisseurs})
    else:
        return render(request, 'magasin/vitrine.html')


def modifierProd(request, produit_id):
    produit = get_object_or_404(Produits, pk=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('magasin:listProduit')
    else:
        form = ProduitForm(instance=produit)
    
    return render(request, 'magasin/modifierProd.html', {'form': form})
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produits, pk=produit_id)

    if request.method == 'POST':
        produit.delete()
        return redirect('magasin:listProduit')
    else:
        return render(request, 'magasin/supprimer_produit.html', {'produit': produit})
def add_to_cart(request, article_id):
    article = Produits.objects.get(pk=article_id)
    if request.method == "POST":
        form = CartItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(article=article)
            cart_item.quantity += quantity
            cart_item.save()
            return redirect('magasin:view_cart')
    else:
        form = CartItemForm()
    return render(request, 'magasin/add_to_cart.html', {'form': form, 'article': article})

def view_cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.article.prix * item.quantity for item in cart_items)
    return render(request, 'magasin/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})
def place_order(request):
    return render(request, 'magasin/order_confirmation.html')
def logout(request):
    CartItem.objects.all().delete()
    return redirect('magasin:vitrine')
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'success': True})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Bonjour {username}, votre compte a été créé avec succès !')
            return redirect('home')  # Assurez-vous que 'home' est le nom de votre URL de page d'accueil
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class CategoryAPIView(APIView):
  def get(self, *args, **kwargs):
    categories = Categorie.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
class ProduitAPIView(APIView):
    def get(self, request, format=None):
        produits = Produits.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)
class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer
    
    def get_queryset(self):
        queryset = Produits.objects.all()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset