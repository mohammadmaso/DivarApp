from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from .filters import CarFilter



from .models import Property, Car, ApartmantBuy
from .forms import SignUpForm, CarForm


def index(request):
    return render(request, './index.html')


def car(request):
    latest_car = Car.objects.order_by('-pub_date')[:20]
    context = {'latest': latest_car }
    return render(request, 'category.html', context)

def propertys(request):
    latest_property = ApartmantBuy.objects.order_by('-pub_date')[:20]
    context = {'latest': latest_property}
    return render(request, 'category.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('../')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def carCreate(request):
    template = 'importCar.html'
    form = CarForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {"form": form}
    return render(request, template, context)

def detailView(request, id):
    context ={}
    context["data"] = Car.objects.get(id = id)
    return render(request, 'detail.html', context)

def search(request):
    car_list = Car.objects.all()
    car_filter = CarFilter(request.GET, queryset=car_list)
    return render(request, 'search.html', {'filter': car_filter})
def my(request):
    if request.user.is_authenticated:
        latest_car = Car.objects.filter(author = request.user.id)
        context = {'latest': latest_car }
        return render(request, 'published.html', context)
    else:
        return HttpResponse("not user")
