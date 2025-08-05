from django.db import models


class LoanAccount(models.Model):
    loan_account = models.CharField(max_length=100, primary_key=True)

    loan_id = models.TextField(blank=True, null=True)
    customer_id = models.TextField(blank=True, null=True)
    loan_status = models.TextField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    branch_name = models.TextField(blank=True, null=True)
    branch_state = models.TextField(blank=True, null=True)
    scheme_name = models.TextField(blank=True, null=True)
    total_outstanding = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_overdue = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    principal_outstanding = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    od_principal_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    od_interest_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    balance_principal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_received_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    excess_amount = models.TextField(blank=True, null=True)
    closure_date = models.DateField(blank=True, null=True)
    asset_classification = models.TextField(blank=True, null=True)
    days_past_due_dpd = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    application_received_date = models.DateField(blank=True, null=True)
    sanction_date = models.DateField(blank=True, null=True)
    tenure = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    apr_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    interest_start_date = models.DateField(blank=True, null=True)
    maturity_date = models.DateField(blank=True, null=True)
    disbursal_date = models.DateField(blank=True, null=True)
    first_installment_due_date = models.DateField(blank=True, null=True)
    sanctioned_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    disbursal_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    net_disbursed_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    application_number = models.TextField(blank=True, null=True)
    cre_name = models.TextField(blank=True, null=True)
    cre_code = models.TextField(blank=True, null=True)
    installment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    ltv = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    no_of_balance_installments = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    last_receipt_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    last_receipt_date = models.DateField(blank=True, null=True)
    total_no_of_bounce = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    last_bounce_date = models.DateField(blank=True, null=True)
    last_bounce_reason = models.TextField(blank=True, null=True)
    closure_waive_off_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    repayment_mode = models.TextField(blank=True, null=True)
    payment_mode = models.TextField(blank=True, null=True)
    cibil_score = models.TextField(blank=True, null=True)
    rate_of_interest = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    delivery_order_no = models.TextField(blank=True, null=True)
    billed_int_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    billed_prin_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_accrued_interest = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    collateral_number = models.TextField(blank=True, null=True)
    repo_flag = models.TextField(blank=True, null=True)
    storeroom_status_flag = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    marital_status = models.TextField(blank=True, null=True)
    primary_mobile_number = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    asset_model = models.TextField(blank=True, null=True)
    manufacturer = models.TextField(blank=True, null=True)
    dealer = models.TextField(blank=True, null=True)
    sub_dealer = models.TextField(blank=True, null=True)
    asset_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    chasis_number = models.TextField(blank=True, null=True)
    engine_number = models.TextField(blank=True, null=True)
    registration_number = models.TextField(blank=True, null=True)
    accomodation_type = models.TextField(blank=True, null=True)
    residential_address = models.TextField(blank=True, null=True)
    residential_city = models.TextField(blank=True, null=True)
    residential_taluka = models.TextField(blank=True, null=True)
    residential_district = models.TextField(blank=True, null=True)
    residential_state = models.TextField(blank=True, null=True)
    residential_country = models.TextField(blank=True, null=True)
    residential_zipcode = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    permanent_city = models.TextField(blank=True, null=True)
    permanent_taluka = models.TextField(blank=True, null=True)
    permanent_district = models.TextField(blank=True, null=True)
    permanent_state = models.TextField(blank=True, null=True)
    permanent_country = models.TextField(blank=True, null=True)
    permanent_zipcode = models.TextField(blank=True, null=True)
    aadhar_no = models.TextField(blank=True, null=True)
    pan = models.TextField(blank=True, null=True)
    mis_date = models.DateField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "loan_account"
        app_label = "loan"
