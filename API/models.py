import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not first_name:
            raise ValidationError('User should have a first name')

        if not first_name:
            raise ValidationError('User should have a last name')

        if not email:
            raise ValidationError('User should have an email')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email=email)
        )
        user.set_password(raw_password=password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password):
        superuser = self.create_user(first_name, last_name, email, password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        unique_together = [
            ['first_name', 'last_name']
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_username(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT)
    teacher = models.ForeignKey(to=User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, unique=True)
    payment_amount = models.BigIntegerField(default=0)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Pupil(models.Model):
    groups = models.ManyToManyField(to=Group)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ['first_name', 'last_name']
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Payment(models.Model):
    pupil = models.ForeignKey(to=Pupil, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    group_name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.BigIntegerField()
    month = models.DateField()
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.amount} - {self.group_name} - {self.month}'
