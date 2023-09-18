from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Expense, Category
from django.db.models import Sum


# Create your views here.
def home(request):
    return render(request, 'home.html')

def expenses_index(request):
  expenses = Expense.objects.filter(user=request.user)
  categories = Category.objects.all()
  return render(request, 'expenses/index.html', {
    'expenses': expenses,
    'categories': categories
  })

def expenses_detail(request, expense_id):
  expense = Expense.objects.get(id=expense_id)
  return render(request, 'expenses/detail.html', { 'expense': expense })

class ExpenseCreate(CreateView):
  model = Expense
  fields = ['title', 'amount', 'date', 'category']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)  

class ExpenseUpdate(UpdateView):
  model = Expense
  fields = ['title', 'amount', 'date', 'category']

class ExpenseDelete(DeleteView):
  model = Expense
  success_url = '/expenses'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class CategoryCreate(CreateView):
  model = Category
  fields = '__all__'
