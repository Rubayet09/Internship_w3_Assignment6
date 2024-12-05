from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django import forms
from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from langdetect import detect, LangDetectException
import csv
from .models import Location, Accommodation, LocalizeAccommodation


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="CSV File", help_text="Upload a CSV file containing location data.")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'location_type', 'country_code', 'city')
    list_filter = ('location_type', 'country_code')
    change_list_template = "admin/location_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='polls_location_import_csv'),
        ]
        
        #[
        #     path('import-csv/', self.import_csv, name='import_csv'),
        # ]
        return custom_urls + urls

    def import_csv(self, request):
        """
        Handle CSV file upload and parse rows to create/update Location objects.
        """
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                skipped_rows = 0
                total_rows = 0

                for row in reader:
                    total_rows += 1
                    try:
                        # Parse the center field into a Point
                        center_coordinates = row['center'].replace("POINT(", "").replace(")", "").split()
                        if len(center_coordinates) != 2:
                            raise ValidationError("Invalid POINT format.")

                        center = Point(float(center_coordinates[0]), float(center_coordinates[1]))

                        # Create or update Location object
                        Location.objects.update_or_create(
                            id=row['id'],
                            defaults={
                                'title': row['title'],
                                'center': center,
                                'location_type': row['location_type'],
                                'country_code': row['country_code'],
                                'state_abbr': row['state_abbr'],
                                'city': row['city'],
                            }
                        )
                    except Exception as e:
                        skipped_rows += 1
                        self.message_user(request, f"Error on row {total_rows}: {e}", level="error")

                self.message_user(
                    request,
                    f"CSV import complete. {total_rows - skipped_rows} rows imported, {skipped_rows} rows skipped.",
                    level="success"
                )
                return HttpResponseRedirect(reverse('admin:polls_location_changelist'))

                # return HttpResponseRedirect("../")
        else:
            form = CSVUploadForm()

        return render(request, "admin/csv_form.html", {"form": form})


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'feed', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'published', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code')
    list_filter = ('published', 'country_code', 'review_score')

    def get_queryset(self, request):
        """
        Restrict the queryset to show only accommodations owned by the logged-in user
        if they are not a superuser.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_id=request.user)

    def save_model(self, request, obj, form, change):
        """
        Automatically associate the logged-in user as the owner of the accommodation
        when it is created.
        """
        if not change or not obj.user_id:
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        """
        Allow deletion only for accommodations owned by the logged-in user,
        unless they are a superuser.
        """
        if obj and not request.user.is_superuser:
            return obj.user_id == request.user
        return super().has_delete_permission(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Exclude the `user_id` field from the form for non-superusers.
        """
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('user_id', None)
        return form


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_id', 'language', 'description_short')
    search_fields = ('property_id__title', 'language')
    list_filter = ('language',)
    autocomplete_fields = ('property_id',)

    def get_queryset(self, request):
        """
        Restrict the queryset to show only localized accommodations
        owned by the logged-in user if they are not a superuser.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(property_id__user_id=request.user)

    def description_short(self, obj):
        """
        Shorten the description to display in the admin list.
        """
        return (obj.description[:50] + "...") if len(obj.description) > 50 else obj.description
    description_short.short_description = "Short Description"

    def save_model(self, request, obj, form, change):
        """
        Validate that the description and policy fields match the selected language.
        Restrict adding/editing localizations to only the owner of the property.
        """
        # Language validation for description
        try:
            detected_lang = detect(obj.description)
            if detected_lang != obj.language:
                raise ValidationError(f"The description must be written in {obj.language.upper()}.")
        except LangDetectException:
            raise ValidationError("Language detection failed. Please ensure the description is valid.")

        # Language validation for policy
        if isinstance(obj.policy, dict):
            for key, value in obj.policy.items():
                try:
                    detected_lang = detect(value)
                    if detected_lang != obj.language:
                        raise ValidationError(f"The policy field '{key}' must be written in {obj.language.upper()}.")
                except LangDetectException:
                    raise ValidationError(f"Language detection failed for policy field '{key}'.")

        if not request.user.is_superuser and obj.property_id.user_id != request.user:
            raise PermissionError("You can only manage localizations for your own properties.")
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        """
        Allow deletion only for localized accommodations owned by the logged-in user
        unless they are a superuser.
        """
        if obj and not request.user.is_superuser:
            return obj.property_id.user_id == request.user
        return super().has_delete_permission(request, obj)
