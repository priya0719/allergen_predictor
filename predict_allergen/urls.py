from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict', views.predict, name='predict'),
    path('data_sets', views.data_sets, name='data_sets'),
    path('method_description', views.method_description, name='method_description'),
    path('allergen_dataset', views.allergen_dataset, name='allergen_dataset'),
    path('non_allergen_dataset', views.non_allergen_dataset, name='non_allergen_dataset')
]