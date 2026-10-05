from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, PasswordInput, Select
from django.utils.html import strip_tags # Tambahkan import ini

from main.models import Project, Award

class ProjectForm(ModelForm):
    secret_code = forms.CharField(
        label="Kode Rahasia",
        widget=PasswordInput(attrs={"placeholder": "Masukkan kode rahasia"}),
    )

    class Meta:
        model = Project
        fields = ["title", "description", "tech_stack", "project_url", "project_image_url"]
        
    
    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        return strip_tags(title)

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        return strip_tags(description)
        
    def clean_tech_stack(self):
        tech_stack = self.cleaned_data.get("tech_stack", "")
        return strip_tags(tech_stack)

class AwardForm(ModelForm):
    secret_code = forms.CharField(
        label="Kode Rahasia",
        widget=PasswordInput(attrs={"placeholder": "Masukkan kode rahasia"}),
    )

    class Meta:
        model = Award
        fields = ["title", "description", "section", "badge_text", "location"]
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: Juara 1 Hackathon Nasional 2026",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan singkat tentang pencapaian, peran, atau kompetisi yang kamu ikuti...",
                    "rows": 3,
                }
            ),
            "section": Select(),
            "badge_text": TextInput(
                attrs={
                    "placeholder": "Contoh: TOP 3 / EVENT / TP-LINK OMADA",
                    "maxlength": 100,
                }
            ),
            "location": TextInput(
                attrs={
                    "placeholder": "Contoh: DKI Jakarta / Online",
                    "maxlength": 100,
                }
            ),
        }
        

    # Tambahkan method clean_<field> di sini
    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        return strip_tags(title)

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        return strip_tags(description)

    def clean_badge_text(self):
        badge_text = self.cleaned_data.get("badge_text", "")
        return strip_tags(badge_text)

    def clean_location(self):
        location = self.cleaned_data.get("location", "")
        return strip_tags(location)

class AwardCreateForm(AwardForm):
    secret_code = None