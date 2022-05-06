from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password, **kwargs):

        if not email:
            raise ValueError('must have user email')
        if not password:
            raise ValueError('must have user password')
        if not username:
            raise ValueError('must have user username')

        user = self.model(
            email=email,
            username=username,
            password=password,
            **kwargs,
        )
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
    phone_number = models.CharField(max_length=31, blank=True, default='')

    class RankType(models.TextChoices):
        Confirm = 'CONFIRM'
        Normal = 'NORMAL'

    rank_type = models.CharField(
        max_length=15,
        choices=RankType.choices,
        default=RankType.Normal
    )
    group = models.ForeignKey('restaurants.Group', on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

