from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Profile
 

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)
 
 
def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile,}
    return render(request, 'users/user-profile.html', context)