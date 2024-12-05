from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from django.contrib.auth.models import User


from langdetect import detect, LangDetectException
from django.core.exceptions import ValidationError

class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = models.PointField()
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    location_type = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3)
    city = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = models.PointField()
    images = models.JSONField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.JSONField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    #for partition
    class Meta:
        indexes = [
            models.Index(fields=['feed']),  # Index for feed partitioning
        ]


class LocalizeAccommodation(models.Model):
    id = models.BigAutoField(primary_key=True)  # Auto-incrementing primary key
    property_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="localized_versions")
    language = models.CharField(max_length=2)  # Language code
    description = models.TextField()  # Localized description
    policy = models.JSONField()  # JSONB dictionary for localized policies

    def __str__(self):
        return f"{self.language.upper()} - {self.property_id.title}"

    class Meta:
        unique_together = ('property_id', 'language')  # Ensure unique language per accommodation
        indexes = [
            models.Index(fields=['language']),
        ]

    def clean(self):
        """
        Validate that the `description` and `policy` fields are in the selected language.
        """
        # Validate `description`
        try:
            detected_lang = detect(self.description)
            if detected_lang != self.language:
                raise ValidationError({
                    'description': f"The description must be written in {self.language.upper()}."
                })
        except LangDetectException:
            raise ValidationError({'description': "Language detection failed. Please ensure the text is valid."})

        # Validate `policy` field values
        if isinstance(self.policy, dict):
            for key, value in self.policy.items():
                try:
                    detected_lang = detect(value)
                    if detected_lang != self.language:
                        raise ValidationError({
                            'policy': f"Policy value for '{key}' must be written in {self.language.upper()}."
                        })
                except LangDetectException:
                    raise ValidationError({
                        'policy': f"Language detection failed for policy value '{key}'. Please ensure the text is valid."
                    })
        else:
            raise ValidationError({'policy': "Policy must be a valid JSON object."})

    def save(self, *args, **kwargs):
        """
        Ensure validation is enforced on save.
        """
        self.clean()
        super().save(*args, **kwargs)


