from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from account.forms import (
    ProfileEditForm,
    SignInForm,
    UserEditForm,
    UserRegistrationForm,
)
from account.models import Profile

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


def register(request):
    if request.method != "POST":
        user_form = UserRegistrationForm()
        context = {"user_form": user_form}
        return render(request, "account/register.html", context)

    user_form = UserRegistrationForm(request.POST)
    if not user_form.is_valid():
        context = {"user_form": user_form}
        return render(request, "account/register.html", context)

    # create a new user object but avoid saving it yet
    new_user = user_form.save(commit=False)
    new_user.set_password(user_form.cleaned_data["password"])
    # save the User object
    new_user.save()
    Profile.objects.create(user=new_user)
    context = {"new_user": new_user}
    return render(request, "account/register_done.html", context)


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


@login_required
def edit(request):
    if request.method != "POST":
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {"user_form": user_form, "profile_form": profile_form}
        return render(request, "account/edit.html", context)

    user_form = UserEditForm(instance=request.user, data=request.POST)
    profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST,
        files=request.FILES,
    )

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "account/edit.html", context)
