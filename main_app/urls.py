from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('expenses/', views.expenses_index, name='index'),
    path('expenses/<int:expense_id>/', views.expenses_detail, name='detail'),
    path('expenses/create/', views.ExpenseCreate.as_view(), name='expenses_create'),
    path('expenses/<int:pk>/update/', views.ExpenseUpdate.as_view(), name='expenses_update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDelete.as_view(), name='expenses_delete'),
    path('categories/create/', views.CategoryCreate.as_view(), name='ctg_create'),
    path('categories/<int:category_id>/', views.categories_detail, name='categories_detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='categories_update'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='categories_delete'),
    path('categories/', views.categories_index, name='categories_index'),
    path('budget/', views.budget_detail, name='budget_detail'),
    path('budget/create/', views.BudgetCreate.as_view(), name='budget_create'),
    path('budget/<int:pk>/update/', views.BudgetUpdate.as_view(), name='budget_update'),
]
