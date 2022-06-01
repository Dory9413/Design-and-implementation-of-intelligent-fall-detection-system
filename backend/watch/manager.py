from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields['firstname'] = '-'
        extra_fields['lastname'] = '-'
        extra_fields['watch_code'] = '-'
        extra_fields['gender'] = True
        super_user = self.create_user(username, password, **extra_fields)
        return super_user
