from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from sn_profile.forms import SignupForm, SigninForm
from django.contrib.auth.decorators import login_required
from post.forms import PostForm


def profile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)

        if request.method == 'POST':
            form = PostForm(data=request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()

                redirecturl = request.POST.get('redirect', '/')

                return redirect(redirecturl)
        else:
            form = PostForm()

        return render(request, 'profile.html', {'form': form, 'user': user})
    else:
        return redirect('/')


def frontpage(request):
    if request.user.is_authenticated:
        return redirect('/' + request.user.username + '/')
    else:
        if request.method == 'POST':
            if 'signupform' in request.POST:
                signupform = SignupForm(data=request.POST)
                signinform = SigninForm()

                if signupform.is_valid():
                    username = signupform.cleaned_data['username']
                    password = signupform.cleaned_data['password1']
                    signupform.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('/')
            else:
                signinform = SigninForm(data=request.POST)
                signupform = SignupForm()

                if signinform.is_valid():
                    login(request, signinform.get_user())
                    return redirect('/')
        else:
            signupform = SignupForm()
            signinform = SigninForm()

        return render(request, 'frontpage.html', {'signupform': signupform, 'signinform': signinform})


def signout(request):
    logout(request)
    return redirect('/')


@login_required
def follow(request, username):
    user = User.objects.get(username=username)
    request.user.sn_profile.follows.add(user.sn_profile)

    return redirect('/' + user.username + '/')


@login_required
def stopfollow(request, username):
    user = User.objects.get(username=username)
    request.user.sn_profile.follows.remove(user.sn_profile)

    return redirect('/' + user.username + '/')


def follows(request, username):
    user = User.objects.get(username=username)
    sn_profiles = request.user.sn_profile.follows.select_related('user').all()

    return render(request, 'users.html', {'title': 'Follows', 'sn_profiles': sn_profiles})


def followers(request, username):
    user = User.objects.get(username=username)
    sn_profiles = request.user.sn_profile.followed_by.select_related('user').all()
    return render(request, 'users.html', {'title': 'Followers', 'sn_profiles': sn_profiles})


def friends(request, username):
    user = User.objects.get(username=username)
    sn_profiles1 = request.user.sn_profile.follows.select_related('user').all()
    sn_profiles2 = request.user.sn_profile.followed_by.select_related('user').all()
    sn_profiles = list(set(sn_profiles1) & set(sn_profiles2))
    return render(request, 'users.html', {'title': 'Friends', 'sn_profiles': sn_profiles})
