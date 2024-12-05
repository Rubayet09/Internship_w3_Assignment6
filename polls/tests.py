from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import Point
from .models import Location, Accommodation, LocalizeAccommodation
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import csv


class LocationModelTestCase(TestCase):
    def test_location_creation(self):
        # Test creating a new Location object
        location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        self.assertEqual(location.title, 'Test Location')
        self.assertEqual(location.country_code, 'US')
        self.assertEqual(str(location.center.x), '10.0')
        self.assertEqual(str(location.center.y), '20.0')

    def test_location_update(self):
        # Test updating an existing Location object
        location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        location.title = 'Updated Test Location'
        location.save()
        updated_location = Location.objects.get(id='123')
        self.assertEqual(updated_location.title, 'Updated Test Location')

    def test_location_str_method(self):
        # Test the __str__ method of the Location model
        location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        self.assertEqual(str(location), 'Test Location')

class AccommodationModelTestCase(TestCase):
    def test_accommodation_creation(self):
        # Test creating a new Accommodation object
        user = User.objects.create_user(username='testuser', password='testpassword')
        location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        accommodation = Accommodation.objects.create(
            id='456',
            feed=0,
            title='Test Accommodation',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(11.0, 21.0),
            images={'image1': 'https://example.com/image1.jpg'},
            location_id=location,
            amenities={'wifi': True, 'pool': False},
            user_id=user,
            published=True
        )
        self.assertEqual(accommodation.title, 'Test Accommodation')
        self.assertEqual(accommodation.country_code, 'US')
        self.assertEqual(accommodation.bedroom_count, 2)
        self.assertEqual(str(accommodation.center.x), '11.0')
        self.assertEqual(str(accommodation.center.y), '21.0')

    def test_accommodation_update(self):
        # Test updating an existing Accommodation object
        user = User.objects.create_user(username='testuser', password='testpassword')
        location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        accommodation = Accommodation.objects.create(
            id='456',
            feed=0,
            title='Test Accommodation',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(11.0, 21.0),
            images={'image1': 'https://example.com/image1.jpg'},
            location_id=location,
            amenities={'wifi': True, 'pool': False},
            user_id=user,
            published=True
        )
        accommodation.title = 'Updated Test Accommodation'
        accommodation.save()
        updated_accommodation = Accommodation.objects.get(id='456')
        self.assertEqual(updated_accommodation.title, 'Updated Test Accommodation')

    def test_accommodation_str_method(self):
        # Test the __str__ method of the Accommodation model
        user = User.objects.create_user(username='testuser', password='testpassword')
        location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        accommodation = Accommodation.objects.create(
            id='456',
            feed=0,
            title='Test Accommodation',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(11.0, 21.0),
            images={'image1': 'https://example.com/image1.jpg'},
            location_id=location,
            amenities={'wifi': True, 'pool': False},
            user_id=user,
            published=True
        )
        self.assertEqual(str(accommodation), 'Test Accommodation')



class LocalizeAccommodationModelTestCase(TestCase):
    def setUp(self):
        # Create a user for the accommodation
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a Location object
        self.location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        
        # Create an Accommodation object
        self.accommodation = Accommodation.objects.create(
            id='456',
            feed=0,
            title='Test Accommodation',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(11.0, 21.0),
            images={'image1': 'https://example.com/image1.jpg'},
            location_id=self.location,
            amenities={'wifi': True, 'pool': False},
            user_id=self.user,
            published=True
        )

    @patch('polls.models.detect', return_value='en')  # Mock language detection to return 'en'
    def test_localize_accommodation_creation(self, mock_detect):
        # Test creating a new LocalizeAccommodation object
        localize_accommodation = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language='en',
            description='This is a test description.',
            policy={'check_in': 'Check-in at 3 PM', 'check_out': 'Check-out at 11 AM'}
        )
        self.assertEqual(localize_accommodation.language, 'en')
        self.assertEqual(localize_accommodation.description, 'This is a test description.')
        self.assertEqual(localize_accommodation.policy, {'check_in': 'Check-in at 3 PM', 'check_out': 'Check-out at 11 AM'})

    @patch('polls.models.detect', return_value='en')  # Mock language detection to return 'en'
    def test_localize_accommodation_update(self, mock_detect):
        # Test updating an existing LocalizeAccommodation object
        localize_accommodation = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language='en',
            description='This is a test description.',
            policy={'check_in': 'Check-in at 3 PM', 'check_out': 'Check-out at 11 AM'}
        )
        localize_accommodation.description = 'Updated test description.'
        localize_accommodation.policy = {'check_in': 'Check-in at 4 PM', 'check_out': 'Check-out at 12 PM'}
        localize_accommodation.save()
        
        # Fetch the updated object from the database
        updated_localize_accommodation = LocalizeAccommodation.objects.get(id=localize_accommodation.id)
        self.assertEqual(updated_localize_accommodation.description, 'Updated test description.')
        self.assertEqual(updated_localize_accommodation.policy, {'check_in': 'Check-in at 4 PM', 'check_out': 'Check-out at 12 PM'})


    def test_localize_accommodation_str_method(self):
        # Test the __str__ method of the LocalizeAccommodation model
        localize_accommodation = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language='en',
            description='This is a test description.',
            policy={'check_in': 'Check-in at 3 PM', 'check_out': 'Check-out at 11 AM'}
        )
        self.assertEqual(str(localize_accommodation), 'EN - Test Accommodation')



class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Parent Location
        self.location1 = Location.objects.create(
            id='123',
            title='Test Location 1',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )

        # Second Location
        self.location2 = Location.objects.create(
            id='456',
            title='Test Location 2',
            center=Point(11.0, 21.0),
            location_type='state',
            country_code='US',
            state_abbr='NY',
            city='New York'
        )

        # Child Location
        self.child_location = Location.objects.create(
            id='789',
            title='Child Location 1',
            center=Point(10.5, 20.5),
            location_type='neighborhood',
            country_code='US',
            state_abbr='CA',
            city='San Francisco',
            parent_id=self.location1
        )

        # Accommodations
        self.accommodation1 = Accommodation.objects.create(
            id='111',
            feed=0,
            title='Test Accommodation 1',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(12.0, 22.0),
            images={'image1': 'https://example.com/image1.jpg'},
            location_id=self.location1,
            amenities={'wifi': True, 'pool': False},
            user_id=self.user,
            published=True
        )
        self.accommodation2 = Accommodation.objects.create(
            id='112',
            feed=1,
            title='Test Accommodation 2',
            country_code='CA',
            bedroom_count=3,
            review_score=3.8,
            usd_rate=200.00,
            center=Point(13.0, 23.0),
            images={'image2': 'https://example.com/image2.jpg'},
            location_id=self.location2,
            amenities={'wifi': True, 'pool': True},
            user_id=self.user,
            published=False
        )

    def test_index_view(self):
        # Test the index view
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Welcome to the Property Management System'})


    def test_location_children_view(self):
        # Test the location_children view for a parent with children
        response = self.client.get(reverse('location_children', args=['123']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['parent'], 'Test Location 1')
        self.assertEqual(len(response.json()['children']), 1)
        self.assertEqual(response.json()['children'][0]['title'], 'Child Location 1')

        # Test the location_children view for a parent with no children
        response = self.client.get(reverse('location_children', args=['456']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['parent'], 'Test Location 2')
        self.assertEqual(len(response.json()['children']), 0)


    def test_accommodation_list_view(self):
        # Test the accommodation_list view
        response = self.client.get(reverse('accommodation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 2)

        # Test filtering by published status
        response = self.client.get(reverse('accommodation_list') + '?published=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 1)
        self.assertEqual(response.json()['accommodations'][0]['title'], 'Test Accommodation 1')

        # Test filtering by country code
        response = self.client.get(reverse('accommodation_list') + '?country=US')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 1)
        self.assertEqual(response.json()['accommodations'][0]['title'], 'Test Accommodation 1')


class AdminTestSuite(TestCase):
    def setUp(self):
        # Create a superuser and a regular user
        self.superuser = User.objects.create_superuser(
            username='superadmin',
            password='superpassword',
            email='superadmin@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='regularpassword',
            email='regularuser@example.com'
        )

        # Create a sample Location
        self.location = Location.objects.create(
            id='123',
            title='Test Location',
            center=Point(10.0, 20.0),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )

        # Create an Accommodation owned by the regular user
        self.accommodation = Accommodation.objects.create(
            id='456',
            feed=0,
            title='Test Accommodation',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(12.0, 22.0),
            images={'image1': 'https://example.com/image1.jpg'},
            location_id=self.location,
            amenities={'wifi': True, 'pool': False},
            user_id=self.regular_user,
            published=True
        )

        # Mock language detection to always return 'en' for tests
        with patch('polls.models.detect', return_value='en'):
            # Create a LocalizeAccommodation with mocked language detection
            self.localized_accommodation = LocalizeAccommodation.objects.create(
                property_id=self.accommodation,
                language='en',
                description='A beautiful property.',
                policy={'cancellation': 'Flexible policy'}
            )

        # Set up the client
        self.client = Client()

    @patch('polls.models.detect', return_value='en')  # Mock detect() to always return 'en'
    def test_location_admin_csv_import(self, mock_detect):
        # Log in as superuser
        self.client.login(username='superadmin', password='superpassword')

        # Create a mock CSV file
        csv_content = io.StringIO()
        csv_writer = csv.writer(csv_content)
        csv_writer.writerow(['id', 'title', 'center', 'location_type', 'country_code', 'state_abbr', 'city'])
        csv_writer.writerow([
            '789',
            'New Location',
            'POINT(30.0 40.0)',
            'city',
            'US',
            'CA',
            'San Jose'
        ])

        csv_file = SimpleUploadedFile(
            'locations.csv',
            csv_content.getvalue().encode('utf-8'),
            content_type='text/csv'
        )

        # Post the CSV file to the custom admin import view
        response = self.client.post(
            reverse('admin:polls_location_import_csv'),
            {'csv_file': csv_file},
            follow=True
        )

        # Assert the response and check that the new location is created
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Location.objects.filter(title='New Location').exists())

    