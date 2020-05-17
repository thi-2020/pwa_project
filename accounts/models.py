from django.db import models

# Create your models here.
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

class ExampleModel(DjangoCassandraModel):
    example_id   = columns.UUID(primary_key=True, default=uuid.uuid4)
    example_type = columns.Integer(index=True)
    created_at   = columns.DateTime()
    description  = columns.Text(required=False)



class Test2User(DjangoCassandraModel):
    id   = columns.UUID(primary_key=True, default=uuid.uuid4)
    first_name = columns.Text(required=False)
    last_name = columns.Text(required=False)
    email = columns.Text(required=False)
    phone = columns.Text(required=False)
    password = columns.Text(required=False)

    @property
    def is_authenticated(self):
        return True


class Sachin(DjangoCassandraModel):
    score = columns.Integer(primary_key=True)


class User(DjangoCassandraModel):
    id   = columns.UUID(primary_key=True, default=uuid.uuid4)
    first_name = columns.Text(required=False)
    last_name = columns.Text(required=False)
    email = columns.Text(required=False)
    phone = columns.Text(required=False)
    password = columns.Text(required=False)
    dob = columns.Date(required=False)

    @property
    def is_authenticated(self):
        return True