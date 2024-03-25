from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from account.forms import SignInForm

# Create your views here.


def user_signin(request):
    if request.method != "POST":
        form = SignInForm()
        return render(request, "account/signin.html", {"form": form})

    form = SignInForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(
            request,
            username=cd["username"],
            password=cd["password"],
        )
        if user is None:
            return HttpResponse("Invalid credentials!")
        if not user.is_active:
            return HttpResponse("Disabled account")
        login(request, user)
        return HttpResponse("Authenticated successfully")


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})
