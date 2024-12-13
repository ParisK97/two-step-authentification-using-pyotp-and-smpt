from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserInfo(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=False)
    numbers = models.CharField(max_length=10, unique=True)
    id_number = models.CharField(max_length=13, unique=True)
    address = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name', '-id_number']

    groups = models.ManyToManyField(
        Group,
        related_name="userinfo_set",  
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="userinfo_set",  
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


    def __str__(self):
        return f'Account for: {self.first_name} {self.last_name} with id number {self.id_number}'

    

