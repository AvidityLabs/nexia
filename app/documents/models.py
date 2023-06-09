from django.utils import timezone
from django.db import models
from api.models import (
    BaseModel,
    User
)

from usecases.models import (
    UseCase
)
# Create your models here.
class DocumentManager(models.Manager):
    def favourites(self, **kwargs):
        """Draft.objects.favourites().count()"""
        return self.filter(created_at__lte=timezone.now(), **kwargs)


class Document(BaseModel):
    # Choices for document_type field
    DOCUMENT_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('doc', 'DOC'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
        # Add more choices as needed
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    use_case = models.ForeignKey(
        UseCase, on_delete=models.CASCADE, blank=True, null=True)
    document_type = models.CharField(
        max_length=10, choices=DOCUMENT_TYPE_CHOICES, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    is_saved = models.BooleanField(default=False)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.title if self.title else f"Draft {self.id}"

    objects = DocumentManager()