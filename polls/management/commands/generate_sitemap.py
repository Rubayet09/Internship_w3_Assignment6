import json
from django.core.management.base import BaseCommand
from polls.models import Location


class Command(BaseCommand):
    help = 'Generate sitemap.json'

    def handle(self, *args, **kwargs):
        # Get all locations ordered by title
        locations = Location.objects.order_by('title')

        # Dictionary to hold countries and their respective locations
        countries = {}

        # Iterate over locations and build the sitemap structure
        for location in locations:
            # Handle the country and add locations to it
            if location.country_code not in countries:
                countries[location.country_code] = {"name": location.country_code, "locations": []}
            
            # Sanitize the location title and prepare the URL
            location_slug = location.title.lower().replace(' ', '-')
            location_url = f"{location.country_code.lower()}/{location_slug}"

            # Append location to the appropriate country
            countries[location.country_code]["locations"].append(
                {location.title: location_url}
            )

        # Prepare the sitemap structure
        sitemap = [{"country": country, **data} for country, data in countries.items()]

        # Save the sitemap to a file
        try:
            with open('sitemap.json', 'w') as f:
                json.dump(sitemap, f, indent=4)
            self.stdout.write(self.style.SUCCESS("sitemap.json generated successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error writing sitemap.json: {str(e)}"))
