from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import LoginForm, UserAccountCreationForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.
User = get_user_model()

#User Creation View
class UserCreation(View):
    def get(self, request, *args, **kwargs):
        form = UserAccountCreationForm()
        context = {
            'user_form':form
        }
        return render(request, 'account/register.html', context=context)
    
    def post(self, request, *args, **kwargs):
        form = UserAccountCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            # Creates Profile for new user
            Profile.objects.create(user = new_user)

            return render(request, 'account/register_done.html', {'new_user':new_user})
        
        context = {
            'user_form':form
        }
        return render(request, 'account/register.html', context=context)
    
user_creation_view = UserCreation.as_view()

#User Edit View
class UserEditView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/user_edit.html', {'user_form':user_form,
                                                          'profile_form':profile_form})

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data = request.POST)
        profile_form = ProfileEditForm(instance= request.user.profile, 
                                       data = request.POST, files= request.FILES)
        
        if user_form.is_valid()  and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "profile updated successfully!")
        else:
            messages.error(request, "Error updating your profile!")
        return render(request, 'account/user_edit.html', {'user_form':user_form,
                                                          'profile_form':profile_form})
    
user_edit_view = UserEditView.as_view()

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if not(User.objects.filter(username = username).exists()):
                return HttpResponse(f"No user exists with usrname: {username}")
            user = authenticate(username=username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse(f"sucessfully logged in as {user}")
                else:
                    return HttpResponse("Disabled account!")
            else: 
                return HttpResponse("Invalid credentials!")
            
        else:
            return HttpResponse(list(form.errors.values())) #list(form.errors.values())
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, "account/login.html", context)

def logout_view(request):
    logout(request)
    return HttpResponse("logged out")

@login_required
def dashboard(request):
    context = {
        "section":"dashboard"
    }
    return render(request, "account/dashboard.html", context)