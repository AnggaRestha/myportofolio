from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, PasswordInput, Select

from main.models import Project, Award

class ProjectForm(ModelForm):
    secret_code = forms.CharField(
        label="Kode Rahasia",
        widget=PasswordInput(attrs={"placeholder": "Masukkan kode rahasia"}),
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/AnggaRestha/portfolio",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }
class AwardForm(ModelForm):
    secret_code = forms.CharField(
        label="Kode Rahasia",
        widget=PasswordInput(attrs={"placeholder": "Masukkan kode rahasia"}),
    )

    class Meta:
        model = Award
        fields = [
            "title",
            "description",
            "section",
            "badge_text",
            "location",
        ]

        labels = {
            "title": "Judul",
            "description": "Deskripsi",
            "section": "Kategori",
            "badge_text": "Badge / Label",
            "location": "Lokasi",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Juara 1 Hackathon Nasional",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pencapaianmu",
                    "rows": 3,
                }
            ),
            "section": Select(),
            "badge_text": TextInput(
                attrs={
                    "placeholder": "TOP 3 / EVENT / TP-LINK OMADA",
                    "maxlength": 100,
                }
            ),
            "location": TextInput(
                attrs={
                    "placeholder": "DKI Jakarta",
                    "maxlength": 100,
                }
            ),
        }