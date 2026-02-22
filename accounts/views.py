from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Achievement
from .scoring import calculate_incoscore
from .forms import StudentRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure profile is created (signal should handle it, but for safety)
            StudentProfile.objects.get_or_create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    # Recalculate score on profile view for demo purposes
    calculate_incoscore(profile)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def add_achievement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        type = request.POST.get('type')
        desc = request.POST.get('description')
        date = request.POST.get('date')
        
        Achievement.objects.create(
            student=request.user.profile,
            title=title,
            type=type,
            description=desc,
            date_achieved=date
        )
        calculate_incoscore(request.user.profile)
        messages.success(request, "Achievement added and InCoScore updated!")
        return redirect('profile')
        
    return render(request, 'accounts/add_achievement.html')
def leaderboard(request):
    """
    Displays the student leaderboard ranked by InCoScore.
    """
    top_students = StudentProfile.objects.all().order_by('-incoscore')[:50]
    return render(request, 'accounts/leaderboard.html', {'top_students': top_students})
