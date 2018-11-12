from django.urls import path

from . import views

app_name = 'lists'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:list_id>/update/', views.update, name='update'),
    path('<int:list_id>/add/', views.add, name='add'),
    path('<int:list_id>/available/<int:choice_id>', views.make_available, name='make_available'),
    path('create/', views.create, name='create'),
]