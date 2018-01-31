from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user manager object that is built on top
    of the one provided in django for User model. Allows
    for creation of basic and super users.
    """

    def create_user(self, username, first_name,
                    last_name, email, password=None):
        """
        Method to allow for creation of basic users
        for the User model.
        """

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

        # check to see that the username is not taken
        username_exists = self.model.objects.filter(username=username)
        if username_exists.count() > 0:
            # if it is taken, raise exception.
            raise ValueError(
                "{} already exists as a username".format(username)
            )

        # create user from model
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # set the user's password
        if password is None:
            psw = self.model.objects.make_random_password()
            user.set_password(psw)
        else:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name,
                         email, password=None):
        """
        Method that allows for superusers to be created.
        from User model.
        """
        # create basic user
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # make an admin
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom user model that overrides the default
    django one to provide permissions for application.
    """

    # Model properties
    username = models.CharField(
        unique=True,
        max_length=40,
        error_messages={
            'unique': 'This username has already been added to the system'
        }
    )
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

    # Django flags for fields
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    # user manager
    objects = UserManager()

    class Meta:
        ordering = ['username']

    # Methods to access properties
    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns full name of user
        """
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        """
        Return just the first name
        """
        return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Override has_perm to return true since
        we are not using this feature of django.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Method to check if the user is active
        or an admin.
        """
        if self.is_active and self.is_admin:
            return True
        return False

    def is_staff(self):
        """
        Method to determine is the user is
        part of the application staff.
        """
        return self.is_admin
