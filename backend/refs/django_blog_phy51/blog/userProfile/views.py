from django.shortcuts import render, redirect
from .forms import UserUpdateForm, ProfileForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'userProfile/profile.html',
                             context)

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'userProfile/profile_edit.html', context)