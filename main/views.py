from django.shortcuts import render

from main.forms import ProjectForm
from .models import Award
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


from main.models import Experience


def show_main(request):
    context = {
        "name": "Angga Restha",
        "npm": "2506656444",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Angga Restha Rustyanto",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_awards(request):
    competitions = Award.objects.filter(section='competition')
    certifications = Award.objects.filter(section='certification')
    
    context = {
        'name': 'Angga Restha Rustyanto',
        'competitions': competitions,
        'certifications': certifications,
    }
    return render(request, 'awards.html', context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Angga Restha Rustyanto",
        "form": form,
    }
    return render(request, "projects_form.html", context)