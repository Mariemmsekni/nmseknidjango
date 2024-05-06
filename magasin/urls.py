from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import CategoryAPIView
from .views import ProduitAPIView


app_name = 'magasin'
urlpatterns = [
    path('', views.index, name='index'),
    path('vitrine/', views.vitrine, name='vitrine'),
    path('nouvProduit/', views.nouveauProduit, name='nouveauProd'),
    path('nouvFournisseur/', views.nouveauFournisseur, name='nouveauFour'),
    path('listFournisseur/', views.listFournisseur, name='listFournisseur'),
    path('listProduit/', views.listProduit, name='listProduit'),
    path('search/', views.search_view, name='search'),
    path('modifierProd/<int:produit_id>/', views.modifierProd, name='modifierProd'),
    path('supprimer-produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
    path('add_to_cart/<int:article_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'), 
    path('cart/remove/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('place_order/', views.place_order, name='place_order'),
    path('logout/', views.logout, name='logout'),
    path('api/category/', CategoryAPIView.as_view()),
    path('api/produits/', ProduitAPIView.as_view()),

    
]

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('accounts/', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='accounts')),
    path('', views.home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
