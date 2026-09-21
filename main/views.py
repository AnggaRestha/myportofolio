from django.shortcuts import render
from main.models import Project
from main.forms import ProjectForm, AwardForm
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
    json_response = get_awards_json(request)

    awards = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    awards = [award.object for award in awards]

    competitions = [a for a in awards if a.section == "competition"]
    certifications = [a for a in awards if a.section == "certification"]

    context = {
        "name": "Angga Restha Rustyanto",
        "competitions": competitions,
        "certifications": certifications,
    }
    return render(request, "awards.html", context)


def get_awards_json(request):
    awards = Award.objects.all()
    awards_json = serializers.serialize("json", awards)
    return HttpResponse(awards_json, content_type="application/json")


def create_award(request):
    form = AwardForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["secret_code"] != settings.PROJECT_SECRET_CODE:
            form.add_error("secret_code", "Kode rahasia salah.")
        else:
            award = form.save(commit=False)
            award.save()
            messages.success(request, "Award baru berhasil ditambahkan!")
            return redirect("main:show_awards")

    context = {
        "name": "Angga Restha Rustyanto",
        "form": form,
    }
    return render(request, "award_form.html", context)


def update_award(request, award_id):
    award = get_object_or_404(Award, pk=award_id)
    form = AwardForm(request.POST or None, instance=award)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["secret_code"] != settings.PROJECT_SECRET_CODE:
            form.add_error("secret_code", "Kode rahasia salah.")
        else:
            form.save()
            messages.success(request, "Award berhasil diperbarui!")
            return redirect("main:show_awards")

    context = {
        "name": "Angga Restha Rustyanto",
        "form": form,
        "award": award,
    }
    return render(request, "award_form.html", context)


def delete_award(request, award_id):
    award = get_object_or_404(Award, pk=award_id)

    if request.method == "POST":
        secret_code = request.POST.get("secret_code", "")
        if secret_code != settings.PROJECT_SECRET_CODE:
            messages.error(request, "Kode rahasia salah, award tidak dihapus.")
            return redirect("main:show_awards")

        award.delete()
        messages.success(request, "Award berhasil dihapus!")
        return redirect("main:show_awards")

    return redirect("main:show_awards")


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