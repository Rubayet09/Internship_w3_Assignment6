from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("locations/", views.location_list, name="location_list"),
    path("accommodations/", views.accommodation_list, name="accommodation_list"),
    
    path("locations/<str:location_id>/children/", views.location_children, name="location_children"),

    #path('signup/', views.property_owner_signup, name='property_owner_signup'),
    path('signup/', views.property_owner_signup, name='signup'),  # This maps the /signup/ URL

]