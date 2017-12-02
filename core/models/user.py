from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        # check that parameters are valid
        if not username:
            raise ValueError(
                "User must have a valid username")

        if not first_name:
            raise ValueError("User must have entered first name")

        if not last_name:
            raise ValueError("User must have entered last name")

        if not email:
            raise ValueError("User must have entered a username")

        username_exists = self.model.objects.filter(username=username)
        if username_exists.count() > 0:
            raise ValueError("{} already exists as a username".format(username))

        # create user from model
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # set the user's password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=40)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_module_leader = models.BooleanField(default=False)
    is_office_admin = models.BooleanField(default=False)
    is_year_tutor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_admin:
            return True
        return False
    
    def is_staff(self):
        return self.is_admin