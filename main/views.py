from django.shortcuts import render
from main.models import Project
from main.forms import ProjectForm
from .models import Award
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
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
        if form.cleaned_data["secret_code"] != settings.PROJECT_SECRET_CODE:
            form.add_error("secret_code", "Kode rahasia salah.")
        else:
            project = form.save(commit=False)
            project.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")

    context = {
        "name": "Angga Restha Rustyanto",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Angga Restha",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        secret_code = request.POST.get("secret_code", "")
        if secret_code != settings.PROJECT_SECRET_CODE:
            messages.error(request, "Kode rahasia salah, proyek tidak dihapus.")
            return redirect("main:show_projects")

        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")