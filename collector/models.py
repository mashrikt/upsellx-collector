import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute, JSONAttribute
from pynamodb.models import Model


class CollectorModel(Model):
    class Meta:
        table_name = 'collector-model'
        host = os.getenv('DB_HOST', 'dynamodb-local://dynamodb:8000')
        aws_access_key_id = os.getenv('AWS_KEY', 'anything')
        aws_secret_access_key = os.getenv('AWS_SECRET', 'fake')
        region = 'us-east-1'

    id = UnicodeAttribute(null=False)
    url = UnicodeAttribute(hash_key=True)
    website = JSONAttribute()
    fb = JSONAttribute()
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False)

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(CollectorModel, self).save()
