from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.
class HRM_Users(AbstractUser):
    role = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    # Disable password for regular users
    def save(self, *args, **kwargs):
        if not self.is_superuser:  # Only allow password for admins
            self.set_unusable_password()  # Prevents login
        super().save(*args, **kwargs)
    
class Department(models.Model):
    dept_name = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$',
                                                    message=("Name can contain only alphabets and spaces"),
                                                    code="invalid name")])
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        permissions = [
            ('can_add_department','can add department'),
            ('can_update_department','Can update department'),
            ('can_delete_department','Can delete department'),
        ]
    
    