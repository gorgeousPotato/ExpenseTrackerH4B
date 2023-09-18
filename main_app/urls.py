from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('expenses/', views.expenses_index, name='index'),
    path('expenses/<int:expense_id>/', views.expenses_detail, name='detail'),
    path('expenses/create/', views.ExpenseCreate.as_view(), name='expenses_create')
]
