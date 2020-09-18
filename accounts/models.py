from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
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

    profile_photo = models.FileField(upload_to='image/profile_photo/', null=True,blank=True, 
        verbose_name="profile_photo",
        default='/image/profile_photo/default.png')

    cover_photo = models.FileField(upload_to='image/cover_photo/', null=True,blank=True, 
        verbose_name="cover_photo")

    complete_status = models.IntegerField(default=1)

    dob = models.DateField(null=True,blank=True)
    current_city = models.CharField(max_length = 500,null=True,blank=True)
    no_of_friend = models.IntegerField(default=0)
    no_of_followers = models.IntegerField(default=0)
    no_of_following = models.IntegerField(default=0)

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.username)









    
    # def save(self, *args, **kwargs):

    #     if not self.make_thumbnail():
    #         # set to a default thumbnail
    #         raise Exception('Could not create thumbnail - is the file type valid?')

    #     super(Photo, self).save(*args, **kwargs)



# import os.path
# from PIL import Image
# from io import BytesIO
# from django.core.files.base import ContentFile
   

# class Photo(models.Model):
#     photo = models.ImageField(upload_to='photos')
#     thumbnail = models.ImageField(upload_to='thumbs', editable=False)



#     def make_thumbnail(self):

#         image = Image.open(self.photo)
#         image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

#         thumb_name, thumb_extension = os.path.splitext(self.photo.name)
#         thumb_extension = thumb_extension.lower()

#         thumb_filename = thumb_name + '_thumb' + thumb_extension

#         if thumb_extension in ['.jpg', '.jpeg']:
#             FTYPE = 'JPEG'
#         elif thumb_extension == '.gif':
#             FTYPE = 'GIF'
#         elif thumb_extension == '.png':
#             FTYPE = 'PNG'
#         else:
#             return False    # Unrecognized file type

#         # Save thumbnail to in-memory file as StringIO
#         temp_thumb = BytesIO()
#         image.save(temp_thumb, FTYPE)
#         temp_thumb.seek(0)

#         # set save=False, otherwise it will run in an infinite loop
#         self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
#         temp_thumb.close()

#         return True



#     def __str__(self):
#         return str(self.user)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class Invitation(BaseModel):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='invitation')
    receiver_email = models.EmailField(null=True,blank=True)
    receiver_phone = models.CharField(max_length=200,null=True,blank=True)
    invitation_key = models.CharField(max_length=200)
    accepted = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created_at',)

class Connection(BaseModel):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='connection_sent')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='connection_received')
    # accepted = models.BooleanField(default=False)
    # rejected = models.DateTimeField(blank=True, null=True)

    def clean(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")



    class Meta:
        verbose_name = ("Connection")
        verbose_name_plural = ("Connections")
        unique_together = ("from_user", "to_user")


class ConnectionRequest(models.Model):
    """ Model to represent friendship requests """

    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="connection_requests_sent")
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="connection_requests_received",)

    message = models.TextField(("Message"), blank=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = ("Connection Request")
        verbose_name_plural = ("Connection Requests")
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return "%s" % self.from_user_id

    def accept(self):
        """ Accept this connection request """
        Connection.objects.create(from_user=self.from_user, to_user=self.to_user)

        Connection.objects.create(from_user=self.to_user, to_user=self.from_user)

        # friendship_request_accepted.send(
        #     sender=self, from_user=self.from_user, to_user=self.to_user
        # )
        from_user.no_of_friend += 1
        from_user.save()

        to_user.no_of_friend += 1
        to_user.save()


        self.delete()

        # Delete any reverse requests
        ConnectionRequest.objects.filter(from_user=self.to_user, to_user=self.from_user).delete()



        return True

    def reject(self):
        """ reject this connection request """
        self.rejected = timezone.now()
        self.save()
        # friendship_request_rejected.send(sender=self)
        # bust_cache("requests", self.to_user.pk)

    # def cancel(self):
    #     """ cancel this friendship request """
    #     self.delete()
    #     friendship_request_canceled.send(sender=self)
    #     bust_cache("requests", self.to_user.pk)
    #     bust_cache("sent_requests", self.from_user.pk)
    #     return True

    # def mark_viewed(self):
    #     self.viewed = timezone.now()
    #     friendship_request_viewed.send(sender=self)
    #     self.save()
    #     bust_cache("requests", self.to_user.pk)
    #     return True




class Follow(models.Model):
    """ Model to represent Following relationships """
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers",)
    created = models.DateTimeField(default=timezone.now)
    

    class Meta:
        verbose_name = ("Following Relationship")
        verbose_name_plural = ("Following Relationships")
        unique_together = ("from_user", "to_user")



    def clean(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValidationError("Users cannot follow themselves.")
        super(Follow, self).save(*args, **kwargs)



class VisibilitySettings(BaseModel):

    types = [
    ('connections only','connections only'),
    ('everyone','everyone'),
    ('myself only','myself only'),
    ('connections and followers only','connections and followers only')
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='visibility_settings')

    who_can_see_your_likes_and_comments = models.CharField(        
        max_length=50,
        choices=types,
        default="everyone")

    who_can_see_your_connection_list = models.CharField(        
        max_length=50,
        choices=types,
        default="everyone")


    # def get_visibilty_options(self): 
    #     print("came here")
    #     return self.types

    class Meta:
        verbose_name_plural = ("Visibility Settings")
