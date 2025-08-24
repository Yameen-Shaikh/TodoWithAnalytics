from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """Define a model manager for User model."""

    def _create_user(self, username, email, password=None, **extra_fields):
        """Create and save a User with the given username, email and password."""
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given username, email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)

    # Make sure USERNAME_FIELD is set to 'username'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    TIME_OF_DAY_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_of_day = models.CharField(max_length=20, choices=TIME_OF_DAY_CHOICES)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    is_backlog = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Activity(models.Model):
    TIME_OF_DAY_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_of_day = models.CharField(max_length=20, choices=TIME_OF_DAY_CHOICES, default='Morning')
    parent_activity = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ActivityLog(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.activity.title} - {self.date}'