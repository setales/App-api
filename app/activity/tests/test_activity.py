"""
Tests for activity APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Activity

from activity.serializers import (
    ActivitySerializer,
    ActivityDetailSerializer,
)


ACTIVITY_URL = reverse('activity:activity-list')


def detail_url(activity_id):
    """Create and return an activity detail URL."""
    return reverse('activity:activity-detail', args=[activity_id])


def create_activity(user, **params):
    """Create and return a sample activity"""
    defaults = {
        'title': 'Sample activity title',
        'time_hours': 5,
        'price': Decimal('128.45'),
        'description': 'Sample description',
        'link': 'http://example.com/activity.pdf'
    }
    defaults.update(params)

    activity = Activity.objects.create(user=user, **defaults)
    return activity


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicActivityAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required to call API."""
        res = self.client.get(ACTIVITY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateActivityAPITests(TestCase):
    """Test uauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_activities(self):
        """Tests retrieving a list of activities"""
        create_activity(user=self.user)
        create_activity(user=self.user)

        res = self.client.get(ACTIVITY_URL)

        activities = Activity.objects.all().order_by('-id')
        serializer = ActivitySerializer(activities, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_activity_list_limited_to_user(self):
        """Test list of activities is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_activity(user=other_user)
        create_activity(user=self.user)

        res = self.client.get(ACTIVITY_URL)

        activities = Activity.objects.filter(user=self.user)
        serializer = ActivitySerializer(activities, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_acitivity_detail(self):
        """Test get activity detail."""
        activity = create_activity(user=self.user)

        url = detail_url(activity.id)
        res = self.client.get(url)

        serializer = ActivityDetailSerializer(activity)
        self.assertEqual(res.data, serializer.data)

    def test_create_activity(self):
        """Test creating a activity."""
        payload = {
            'title': 'Sample activity',
            'time_hours': 3,
            'price': Decimal('155.99'),
        }
        res = self.client.post(ACTIVITY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Activity.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test partial update of a activity."""
        original_link = 'https://example.com/activity.pdf'
        activity = create_activity(
            user=self.user,
            title='Sample activity title',
            link=original_link,
        )

        payload = {'title': 'New activity title'}
        url = detail_url(activity.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        activity.refresh_from_db()
        self.assertEqual(activity.title, payload['title'])
        self.assertEqual(activity.link, original_link)
        self.assertEqual(activity.user, self.user)

    def test_full_update(self):
        """Test full update of activity."""
        activity = create_activity(
            user=self.user,
            title='Sample activity title',
            link='https://exmaple.com/activity.pdf',
            description='Sample activity description.',
        )

        payload = {
            'title': 'New activity title',
            'link': 'https://example.com/new-activity.pdf',
            'description': 'New activity description',
            'time_hours': 7,
            'price': Decimal('72.50'),
        }
        url = detail_url(activity.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        activity.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(activity, k), v)
        self.assertEqual(activity.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the activity user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        activity = create_activity(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(activity.id)
        self.client.patch(url, payload)

        activity.refresh_from_db()
        self.assertEqual(activity.user, self.user)

    def test_activity_other_users_activity_error(self):
        """Test trying to delete another users activity gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        activity = create_activity(user=new_user)

        url = detail_url(activity.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Activity.objects.filter(id=activity.id).exists())
