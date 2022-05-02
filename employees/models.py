from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None, **kwargs):

        if not email:
            raise ValueError('must have user email')
        if not username:
            raise ValueError('must have user username')

        user = self.model(
            email=email,
            username=username,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **kwargs):

        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **kwargs,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Employee(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=15)
    rank = models.CharField(max_length=15, blank=True, default='')
    group = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
