from django.db import models


class DedupApi(models.Model):
    loan_account = models.TextField()
    loan_id = models.BigIntegerField(blank=True, null=True)
    file_no = models.TextField(blank=True, null=True)
    coapplicant_customer_id = models.TextField(blank=True, null=True)
    coapplicant_customer_name = models.TextField(blank=True, null=True)
   
    coapplicant_full_address = models.TextField(blank=True, null=True)
    coapplicant_landmark = models.TextField(blank=True, null=True)
    coapplicant_district = models.TextField(blank=True, null=True)
    coapplicant_city = models.TextField(blank=True, null=True)
    coapplicant_state = models.TextField(blank=True, null=True)
    
    coapplicant_zipcode = models.BigIntegerField(blank=True, null=True)
    coapplicant_mobile_no = models.TextField(blank=True, null=True)
    coapplicant_gender = models.CharField(max_length=20, blank=True, null=True)
    coapplicant_dob = models.DateField(blank=True, null=True)
    coapplicant_relationship = models.TextField(blank=True, null=True)
   
    guarantor_customer_id = models.TextField(blank=True, null=True)
    guarantor_customer_name = models.TextField(blank=True, null=True)
    guarantor_full_address = models.TextField(blank=True, null=True)
    guarantor_landmark = models.TextField(blank=True, null=True)
    guarantor_district = models.TextField(blank=True, null=True)
    
    guarantor_city = models.TextField(blank=True, null=True)
    guarantor_state = models.TextField(blank=True, null=True)
    guarantor_zipcode = models.BigIntegerField(blank=True, null=True)
    guarantor_mobile_no = models.TextField(blank=True, null=True)
    guarantor_gender = models.CharField(max_length=20, blank=True, null=True)
   
    guarantor_dob = models.DateField(blank=True, null=True)
    guarantor_relationship = models.TextField(blank=True, null=True)
    customer_id = models.TextField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
  
    customer_address = models.TextField(blank=True, null=True)
    landmark = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
   
    zipcode = models.BigIntegerField(blank=True, null=True)
    mobile_no = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    scheme_name = models.TextField(blank=True, null=True)
    
    branch_name = models.TextField(blank=True, null=True)
    disbursal_date = models.DateField(blank=True, null=True)
    total_outstanding = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_overdue = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    repo_flag = models.TextField(blank=True, null=True)
   
    loan_status = models.CharField(max_length=2, blank=True, null=True)
    data_source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dedup_api"
