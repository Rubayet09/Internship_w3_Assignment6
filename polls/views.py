from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, Group
from .models import Location, Accommodation

def index(request):
    return JsonResponse({"message": "Welcome to the Property Management System"})

def property_owner_signup(request):
    """
    Allows property owners to sign up and be added to the 'Property Owners' group.
    """
    if request.method == 'POST':
        # Extract the form data from the POST request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Create a new user with the provided information
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Ensure that the 'Property Owners' group exists, and assign the user to it
        property_owners_group, _ = Group.objects.get_or_create(name='Property Owners')
        property_owners_group.user_set.add(user)
        
        # Respond with a success message
        return HttpResponse("Sign-up successful! You are now a Property Owner.")
    
    # Render the signup page if the method is GET
    return render(request, 'signup.html')

def location_list(request):
    """
    Retrieve a paginated list of locations.
    Query parameters:
    - `page`: Page number (default is 1)
    - `type`: Filter by location type (optional)
    """
    location_type = request.GET.get('type', None)
    locations = Location.objects.all().order_by('id')  

    if location_type:
        locations = locations.filter(location_type=location_type)

    paginator = Paginator(locations.values('id', 'title', 'location_type', 'country_code', 'city'), 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return JsonResponse({
        "total_pages": paginator.num_pages,
        "current_page": page.number,
        "locations": list(page)
    })

def location_children(request, location_id):
    """
    Retrieve child locations of a given location.
    """
    parent_location = get_object_or_404(Location, pk=location_id)
    children = parent_location.children.values('id', 'title', 'location_type', 'country_code', 'city')
    return JsonResponse({"parent": parent_location.title, "children": list(children)})

def accommodation_list(request):
    """
    Retrieve a paginated list of accommodations.
    Query parameters:
    - `page`: Page number (default is 1)
    - `published`: Filter by published status (optional)
    - `country`: Filter by country code (optional)
    """
    published = request.GET.get('published', None)
    country_code = request.GET.get('country', None)
    accommodations = Accommodation.objects.all()

    if published is not None:
        accommodations = accommodations.filter(published=bool(int(published)))

    if country_code:
        accommodations = accommodations.filter(country_code=country_code)

    paginator = Paginator(accommodations.values(
        'id', 'title', 'country_code', 'bedroom_count', 'usd_rate', 'published'), 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return JsonResponse({
        "total_pages": paginator.num_pages,
        "current_page": page.number,
        "accommodations": list(page)
    })

def accommodation_by_user(request, user_id):
    """
    Retrieve accommodations created by a specific user.
    """
    accommodations = Accommodation.objects.filter(user_id=user_id).values(
        'id', 'title', 'country_code', 'bedroom_count', 'usd_rate', 'published')
    return JsonResponse({"user_accommodations": list(accommodations)})


