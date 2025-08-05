from rest_framework import serializers
from loan.models.DedupApi import DedupApi


class DedupApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = DedupApi
        fields = "__all__"
