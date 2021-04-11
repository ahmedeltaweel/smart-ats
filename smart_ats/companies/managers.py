from django.contrib.auth.models import BaseUserManager


class CompanyAdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().select_related("company")

    def create_user(self, username, email, password=None, company=None):
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(
            username=username, email=self.normalize_email(email), company=company
        )
        user.set_password(password)
        user.save()
        return user
