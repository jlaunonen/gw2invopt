from django.http import HttpResponse
from django.shortcuts import render

from .fetcher import Progress, update_characters
from .models import Character


def index(request):
    return render(
        request,
        "gw2inv_app/index.html",
        {
            "characters": Character.objects.all(),
        },
    )


def full_update(request):
    progress = Progress(lambda: None)
    update_characters(progress)  # FIXME: This may be a long operation.
    return HttpResponse(f"Done {progress.current} / {progress.target}".encode())
