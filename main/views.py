from main.models import Project
from main.forms import ProjectForm, AwardForm
from .models import Award
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
import datetime
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse 
from django.core.exceptions import PermissionDenied        

from main.models import Experience

def is_editor_or_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Editor').exists())


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Angga Restha",
        "npm": "2506656444",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Angga Restha",
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
        "name": "Angga Restha",
        "competitions": competitions,
        "certifications": certifications,
        "is_editor": is_editor_or_admin(request.user),
    }
    return render(request, "awards.html", context)


def get_awards_json(request):
    awards = Award.objects.all()
    awards_json = serializers.serialize("json", awards)
    return HttpResponse(awards_json, content_type="application/json")

@login_required(login_url="/login/")
def create_award(request):
    if not is_editor_or_admin(request.user):
        raise PermissionDenied
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
        "name": "Angga Restha",
        "form": form,
    }
    return render(request, "award_form.html", context)

@login_required(login_url="/login/")
def update_award(request, award_id):
    if not is_editor_or_admin(request.user):
        raise PermissionDenied
    
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
        "name": "Angga Restha",
        "form": form,
        "award": award,
    }
    return render(request, "award_form.html", context)

@login_required(login_url="/login/")
def delete_award(request, award_id):
    if not is_editor_or_admin(request.user):
        raise PermissionDenied
    
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


@login_required(login_url="/login/")
def create_project(request):
    if not is_editor_or_admin(request.user):
        raise PermissionDenied
    
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
        "name": "Angga Restha",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Angga Restha",
        "title_query": title_query,
        "is_editor": is_editor_or_admin(request.user),
    }
    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    
    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not is_editor_or_admin(request.user):
        raise PermissionDenied

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

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. silakan login")
        return redirect("main:login")

    context = {
        "name" : "Angga Restha",
        "form" : form,
    }
    return render(request, "register.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Angga Restha",
            "form": form,
    }
    return render(request, "login.html", context)

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)