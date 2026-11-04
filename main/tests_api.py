import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from main.models import Award


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AwardEditorPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        User = get_user_model()

        self.editor = User.objects.create_user(
            username="test_editor",
            password="testpass123"
        )

        self.user_biasa = User.objects.create_user(
            username="test_user",
            password="testpass123"
        )

        self.superuser = User.objects.create_superuser(
            username="test_owner",
            email="owner@example.com",
            password="testpass123"
        )

        editor_group, _ = Group.objects.get_or_create(
            name="Editor"
        )
        self.editor.groups.add(editor_group)

        self.award = Award.objects.create(
            title="Award Percobaan",
            description="Deskripsi award percobaan",
            section="competition",
            badge_text="TOP 3",
            location="Jakarta"
        )

        self.list_url = reverse("api:award-list")
        self.detail_url = reverse(
            "api:award-detail",
            kwargs={"award_id": self.award.id}
        )

    def test_visitor_can_read(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_modify(self):
        self.client.force_authenticate(
            user=self.user_biasa
        )

        response = self.client.patch(
            self.detail_url,
            {"title": "Judul Baru"},
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_editor_can_patch(self):
        self.client.force_authenticate(
            user=self.editor
        )

        response = self.client.patch(
            self.detail_url,
            {"title": "Award Diedit Editor"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.award.refresh_from_db()

        self.assertEqual(
            self.award.title,
            "Award Diedit Editor"
        )

    def test_editor_cannot_create(self):
        self.client.force_authenticate(
            user=self.editor
        )

        response = self.client.post(
            self.list_url,
            {
                "title": "Award Baru",
                "description": "Dibuat oleh editor",
                "section": "competition",
                "badge_text": "TOP 1",
                "location": "Jakarta"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_editor_cannot_delete(self):
        self.client.force_authenticate(
            user=self.editor
        )

        response = self.client.delete(
            self.detail_url
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            Award.objects.filter(
                pk=self.award.pk
            ).exists()
        )

    def test_superuser_can_delete(self):
        self.client.force_authenticate(
            user=self.superuser
        )

        response = self.client.delete(
            self.detail_url
        )

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Award.objects.filter(
                pk=self.award.pk
            ).exists()
        )