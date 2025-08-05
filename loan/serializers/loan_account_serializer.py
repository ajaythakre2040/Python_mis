from rest_framework import serializers
from ..models.LoanAccount import LoanAccount


class LoanAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanAccount
        fields = "__all__"
