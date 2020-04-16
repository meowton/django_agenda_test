from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from core.models import Event


# Create your views here.
def user_login(request):
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("/")


def submit_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Wrong user or password.")
    return redirect("/")


@login_required(login_url="/login/")
def list_events(request):
    user = request.user
    current_date = datetime.now() - timedelta(hours=3)
    event = Event.objects.filter(user=user, event_date__gt=current_date)
    response = {"event": event}
    return render(request, "agenda.html", response)


@login_required(login_url="/login/")
def list_old_events(request):
    user = request.user
    current_date = datetime.now() - timedelta(hours=3)
    event = Event.objects.filter(user=user, event_date__lt=current_date)
    response = {"event": event}
    return render(request, "agenda.html", response)


@login_required(login_url="/login/")
def event(request):
    id_event = request.GET.get("id")
    data = {}
    if id_event:
        data["event"] = Event.objects.get(id=id_event)
    return render(request, "event.html", data)


@login_required(login_url="/login/")
def submit_event(request):
    if request.POST:
        event_id = request.POST.get("event_id")
        title = request.POST.get("title")
        address = request.POST.get("address")
        date = request.POST.get("event_date")
        description = request.POST.get("description")
        user = request.user

        if event_id:
            Event.objects.filter(id=event_id).update(
                title=title,
                address=address,
                event_date=date,
                description=description,
            )
        else:
            Event.objects.create(
                user=user,
                title=title,
                address=address,
                event_date=date,
                description=description,
            )

    next_e = request.POST.get("next").replace("event/", "")
    return redirect(next_e)


@login_required(login_url="/login/")
def delete_event(request, event_id):
    user = request.user
    try:
        event = Event.objects.get(id=event_id)
    except Exception:
        raise Http404()

    if user == event.user:
        event.delete()
    else:
        raise Http404()

    next = request.GET.get("next")
    return redirect(next)
