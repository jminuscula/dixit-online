

from rest_framework import serializers


class StatusField(serializers.Field):

    def to_representation(self, obj):
        if type(obj) is list:
            return [status.value for status in obj]
        return obj.value
