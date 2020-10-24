from django.contrib.auth.models import BaseUserManager


class CompanyAdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().select_related("company")

        """
        Creates and saves a User with the given email and password.
        """

    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuse(self, username, email, password):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
