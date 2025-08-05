from rest_framework import serializers
from ..models.LoanMisSnapshot import LoanMisSnapshot


class LoanMisSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanMisSnapshot
        fields = "__all__"
