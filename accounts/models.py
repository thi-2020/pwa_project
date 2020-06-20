from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email,username, password, **extra_fields):
        #this is a private method and should not be used anywhere by anyone
        """Create and save a User with the given email and password."""
        is_staff = extra_fields.get('is_staff')
        if is_staff is True:
            user = self.model(username=username, **extra_fields)
        else:            
            if not email:
                raise ValueError('The given email must be set')
            email = self.normalize_email(email)
            user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,username, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,username, password, **extra_fields)

    def create_superuser(self,username,password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(None,username,password, **extra_fields)


class User(AbstractUser):

    email = models.EmailField()
    phone = models.CharField(max_length=10,blank=True,null=True)
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.username)






class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_profile')
    image = models.FileField(upload_to='image/users/', null=True,blank=True, verbose_name="image")
    
    dob = models.DateField(null=True,blank=True)




    def __str__(self):
        return str(self.user)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class Invitation(BaseModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='invitation')
    receiver_email = models.EmailField(null=True,blank=True)
    receiver_phone = models.CharField(max_length=200,null=True,blank=True)
    invitation_key = models.CharField(max_length=200)
    accepted = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created_at',)