from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Expense, Category, Budget
from django.db.models import Sum



# Create your views here.
def require_budget(view_function):
  def _wrapped_view(request, *view_args, **decorator_kwargs):
    if Budget.objects.filter(user=request.user).exists():
      return view_function(request, *view_args, **decorator_kwargs)
    else:
      return redirect('budget_create')
  return _wrapped_view


def home(request):
    return render(request, 'home.html')

@require_budget
@login_required
def expenses_index(request):
  expenses = Expense.objects.filter(user=request.user)
  categories = Category.objects.all()
  category_expenses = Category.objects.filter(expense__user = request.user).annotate(total_expenses = Sum('expense__amount'))
  budgets = Budget.objects.filter(user=request.user)
  budget = budgets[0]
  sum = 0
  for expense in expenses:
    if expense.date >= budget.start_date and expense.date <= budget.end_date:
      sum += expense.amount
  percent_left = int(((budget.amount - sum) / budget.amount) * 100)
  amount_left = budget.amount - sum
  return render(request, 'expenses/index.html', {
    'expenses': expenses,
    'categories': categories,
    'category_expenses': category_expenses,
    'budget': budget,
    'sum': sum,
    'amount_left': amount_left,
    'percent_left': percent_left
  })

@require_budget
@login_required
def expenses_detail(request, expense_id):
  expense = Expense.objects.get(id=expense_id)
  return render(request, 'expenses/detail.html', { 'expense': expense })


@require_budget
@login_required
def categories_detail(request, category_id):
  category = Category.objects.get(id=category_id)
  expenses = Expense.objects.filter(category=category, user=request.user)
  return render(request, 'main_app/category_detail.html', { 'category': category, 'expenses': expenses})

@require_budget
@login_required
def categories_index(request):
  categories = Category.objects.filter(user=request.user)
  return render(request, 'main_app/category_index.html', { 'categories': categories})

@require_budget
@login_required
def budget_detail(request):
  budgets = Budget.objects.filter(user=request.user)
  budget = budgets[0]
  expenses = Expense.objects.filter(user=request.user)
  sum = 0
  for expense in expenses:
    if expense.date >= budget.start_date and expense.date <= budget.end_date:
      sum += expense.amount
  percent_left = int(((budget.amount - sum) / budget.amount) * 100)
  amount_left = budget.amount - sum
  return render(request, 'main_app/budget_detail.html', { 
    'budget': budget,
    'sum': sum,
    'amount_left': amount_left,
    'percent_left': percent_left
  })

@require_budget
@login_required
def charts(request):
  expenses = Expense.objects.filter(user=request.user)
  categories = Category.objects.all()
  category_expenses = Category.objects.filter(expense__user = request.user).annotate(total_expenses = Sum('expense__amount'))
  return render(request, 'main_app/charts.html', {
    'expenses': expenses,
    'categories': categories,
    'category_expenses': category_expenses,
  })

@require_budget
@login_required
def charts(request):
  category_expenses = Category.objects.filter(expense__user = request.user).annotate(total_expenses = Sum('expense__amount'))
  return render(request, 'main_app/charts.html', { 
    'category_expenses': category_expenses,
    })


class ExpenseCreate(LoginRequiredMixin, CreateView):
  model = Expense
  fields = ['title', 'amount', 'date', 'category']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)  
  
  def get_form(self, form_class=None):
        form = super(ExpenseCreate, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form


class ExpenseUpdate(LoginRequiredMixin, UpdateView):
  model = Expense
  fields = ['title', 'amount', 'date', 'category']

class ExpenseDelete(LoginRequiredMixin, DeleteView):
  model = Expense
  success_url = '/expenses'

class CategoryCreate(LoginRequiredMixin, CreateView):
  model = Category
  fields = ['title']

class CategoryUpdate(LoginRequiredMixin, UpdateView):
  model = Category
  fields = ['title']

class CategoryDelete(LoginRequiredMixin, DeleteView):
  model = Category
  success_url = '/categories'

class BudgetCreate(LoginRequiredMixin, CreateView):
  model = Budget
  fields = ['amount', 'start_date', 'end_date']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form) 
  
class BudgetUpdate(LoginRequiredMixin, UpdateView):
  model = Budget
  fields = ['amount', 'start_date', 'end_date']

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      categories = Category.objects.bulk_create(
        [
          Category(title='Groceries', icon='fa-cart-shopping', user=user, color="rgba(54, 162, 235, 0.7)"),
          Category(title='Bills', icon='fa-file-invoice-dollar', user=user, color="rgba(255, 206, 86, 0.7)"),
          Category(title='Shopping', icon='fa-credit-card', user=user, color="#F2C654"),
          Category(title='Car', icon='fa-car-on', user=user, color="#845FFC"),
          Category(title='House', icon='fa-house', user=user, color="#00B7A8"),
          Category(title='Entertainment', icon='fa-champagne-glasses', user=user, color="#EE8EF0"),
        ]
      )
      return redirect('budget_create')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

