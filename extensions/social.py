from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.contrib.auth import decorators, get_user, models
from django.core.handlers.wsgi import WSGIRequest
from users.models import Profile

def get_user_owner(uid: int) -> tuple[bool, models.User | None]:
    try:
        user = models.User.objects.get(id=uid)
        return True, user
    except models.User.DoesNotExist:
        return False, None


@decorators.login_required(login_url='/login')
def profile_system(req: WSGIRequest, uid: int):
    viewer = get_user(req)
    is_exist, user = get_user_owner(uid)
    if not is_exist:
        return render(req, 'error.html', {'error_code': 404, 'content': 'Данного пользователя не существует!'}, status=404)
    profile = Profile.objects.get(user=user)
    profile.is_owner = viewer.id == uid
    if profile.is_private and not profile.is_owner:
        return render(req, 'error.html', {'error_code': 403, 'content': 'Профиль данного пользователя приватный!'}, status=403)
    if req.method == 'GET':
        return get_profile(req, user, profile, viewer)
    elif req.method == 'POST':
        if "delete" in req.POST.keys():
            return delete_profile(user, profile)
        return change_private(req, user)

def get_profile(req: WSGIRequest, user, profile, viewer):
    try:
        profile.total = profile.win + profile.lose
        profile.win_percent = int(profile.win / profile.total * 100)
        profile.lose_percent = 100 - profile.win_percent
    except ZeroDivisionError:
        profile.total, profile.win_percent, profile.lose_percent = 0, 0, 0
    return render(req, 'profile.html', {'profile': profile, 'user': user, 'viewer': viewer})

def change_private(req: WSGIRequest, user):
    profile = Profile.objects.get(user=user)
    if "change_private" in req.POST.keys():
        profile.is_private = True
    elif "change_open" in req.POST.keys():
        profile.is_private = False
    profile.save()
    return redirect(req.path)

def delete_profile(user: models.User, profile: Profile):
    if profile.is_owner:
        user.delete()
        return redirect('login')
