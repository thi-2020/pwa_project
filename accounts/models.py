from django.db import models
from django.utils import timezone
# Create your models here.
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
class ExampleModel(DjangoCassandraModel):
    example_id   = columns.UUID(primary_key=True, default=uuid.uuid4)
    example_type = columns.Integer(index=True)
    created_at   = columns.DateTime(default=timezone.now)
    description  = columns.Text(required=False)



class Test2User(DjangoCassandraModel):
    id   = columns.UUID(primary_key=True, default=uuid.uuid4)
    first_name = columns.Text(required=False)
    last_name = columns.Text(required=False)
    email = columns.Text(required=False)
    phone = columns.Text(required=False)
    password = columns.Text(required=False)
    created_at  = columns.DateTime(default=timezone.now,primary_key=True,clustering_order="DESC")
    @property
    def is_authenticated(self):
        return True
    class Meta:
        get_pk_field='id'


class Sachin(DjangoCassandraModel):
    score = columns.Integer(primary_key=True)


class User(DjangoCassandraModel):
    id   = columns.UUID(primary_key=True, default=uuid.uuid4)
    first_name = columns.Text(required=False)
    last_name = columns.Text(required=False)
    username = columns.Text(required=False)
    email = columns.Text(required=False)
    phone = columns.Text(required=False)
    password = columns.Text(required=False)
    dob = columns.Date(required=False)
    created_at  = columns.DateTime(default=timezone.now,primary_key=True,clustering_order="DESC")

    class Meta:
        get_pk_field='id'

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None
    @property
    def is_authenticated(self):
        return True
    


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            print("@58 in model.py of accounts")
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)


class Invitation(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    sender_id = columns.UUID(required=True)
    email = columns.Text(max_length=150,required=True)
    created = columns.DateTime(default=timezone.now,primary_key=True,clustering_order="DESC")
    key = columns.Text(max_length=100)
    accepted = columns.Boolean(default=False)
    class Meta:
        get_pk_field='id'