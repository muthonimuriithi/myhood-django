from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/accounts/login/')
@csrf_protect
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/index')

@login_required(login_url='/accounts/login/')
@csrf_protect
def new_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile/profile.html', context)

def neighbourhoods(request):
    all_hoods = Neighbourhood.objects.all()
    all_hoods = all_hoods[::-1]
    context = {
        'all_hoods': all_hoods,
    }
    return render(request, 'neighbourhoods.html', context)

@login_required(login_url='/accounts/login/')
@csrf_protect
def create_neighbourhood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.admin = request.user
            neighbourhood.save()
            messages.success(
                request, 'You have succesfully created a Neighbourhood.Now proceed and join the Neighbourhood')
            return redirect('neighbourhood')
    else:
        form = NeighbourHoodForm()
    return render(request, 'new_hood.html', {'form': form})

@login_required(login_url='/accounts/login/')
@csrf_protect
def join_neighbourhood(request, id):
    neighbourhood = get_object_or_404(Neighbourhood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    messages.success(
        request, 'Success! You have succesfully joined this Neighbourhood ')
    return redirect('neighbourhood')

@login_required(login_url='/accounts/login/')
@csrf_protect
def leave_neighbourhood(request, id):
    neighbourhood = get_object_or_404(Neighbourhood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    messages.success(
        request, 'Success! You have succesfully exited this Neighbourhood ')
    return redirect('neighbourhood')

@login_required(login_url='/accounts/login/')
@csrf_protect
def single_neighbourhood(request, hood_id):
    neighbourhood = Neighbourhood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=neighbourhood)
    posts = Post.objects.filter(neighbourhood=neighbourhood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = neighbourhood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single-hood', neighbourhood.id)
    else:
        form = BusinessForm()
    context = {
        'neighbourhood': neighbourhood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'single_hood.html', context)

@login_required(login_url='/accounts/login/')
@csrf_protect
def create_post(request, hood_id):
    neighbourhood = Neighbourhood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.neighbourhood = neighbourhood
            post.user = request.user.profile
            post.save()
            messages.success(
                    request, 'You have succesfully created a Post')
            return redirect('single-hood', neighbourhood.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})

@login_required(login_url='/accounts/login/')
@csrf_protect
def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        context = {
            'results': results,
            'message': message
        }
        return render(request, 'search_results.html', context)
    else:
        message = "You haven't searched for any business"
    return render(request, "search_results.html")
