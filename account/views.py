from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm


"""
You decorate your view with the login_required decorator of the
authentication framework. The login_required decorator checks
whether the current user is authenticated. If the user is
authenticated, it executes the decorated view; if the user is not
authenticated, it redirects the user to the login URL with the
originally requested URL as a GET parameter named next .
By doing this, the login view redirects users to the URL that they
were trying to access after they successfully log in. Remember that
you added a hidden input in the form of your login template for
this purpose.
You can also deﬁne a section variable. You will use this variable to
track the site's section that the user is browsing. Multiple views
may correspond to the same section. This is a simple way to deﬁne
the section that each view corresponds to.
"""
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})