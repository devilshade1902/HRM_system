from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.
class HRM_Users(AbstractUser):
    fname = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$',)])
    lname = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$',)])
    email1 = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="hrm_users_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="hrm_users_permissions",
        blank=True
    )
    
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
    
    