from django.db import models


class LoanAccount(models.Model):
    loan_account = models.CharField(max_length=100, primary_key=True)
    loan_id = models.BigIntegerField(blank=True, null=True)
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    product_id = models.CharField(max_length=100, blank=True, null=True)
    product_code = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    down_payment_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    loan_status = models.CharField(max_length=20, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    branch_state = models.CharField(max_length=100, blank=True, null=True)
    scheme_name = models.CharField(max_length=255, blank=True, null=True)
    scheme_code = models.CharField(max_length=100, blank=True, null=True)
    loan_application_type = models.CharField(max_length=100, blank=True, null=True)
    total_outstanding = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    od_principal_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    od_interest_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    balance_principal = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    closure_date = models.DateField(blank=True, null=True)
    asset_classification = models.CharField(max_length=100, blank=True, null=True)
    days_past_due = models.IntegerField(blank=True, null=True)
    application_received_date = models.DateField(blank=True, null=True)
    sanction_date = models.DateField(blank=True, null=True)
    tenure = models.IntegerField(blank=True, null=True)
    apr_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    interest_start_date = models.DateField(blank=True, null=True)
    maturity_date = models.DateField(blank=True, null=True)
    disbursal_date = models.DateField(blank=True, null=True)
    first_installment_due_date = models.DateField(blank=True, null=True)
    sanctioned_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    disbursal_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    net_disbursed_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    application_number = models.CharField(max_length=100, blank=True, null=True)
    cre_name = models.CharField(max_length=255, blank=True, null=True)
    cre_code = models.CharField(max_length=100, blank=True, null=True)
    installment_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    ltv = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    no_of_balance_installments = models.IntegerField(blank=True, null=True)
    last_receipt_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    last_receipt_date = models.DateField(blank=True, null=True)
    total_no_of_bounce = models.IntegerField(blank=True, null=True)
    last_bounce_date = models.DateField(blank=True, null=True)
    last_bounce_reason = models.TextField(blank=True, null=True)
    repayment_mode = models.CharField(max_length=100, blank=True, null=True)
    payment_mode = models.CharField(max_length=100, blank=True, null=True)
    cibil_score = models.CharField(max_length=100, blank=True, null=True)
    rate_of_interest = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    delivery_order_no = models.CharField(max_length=100, blank=True, null=True)
    total_accrued_interest = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    repo_flag = models.CharField(max_length=100, blank=True, null=True)
    storeroom_status_flag = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    primary_mobile_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    asset_model = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    dealer = models.CharField(max_length=100, blank=True, null=True)
    sub_dealer = models.CharField(max_length=100, blank=True, null=True)
    asset_cost = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    chasis_number = models.CharField(max_length=100, blank=True, null=True)
    engine_number = models.CharField(max_length=100, blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    accomodation_type = models.CharField(max_length=100, blank=True, null=True)
    residential_address = models.TextField(blank=True, null=True)
    residential_city = models.CharField(max_length=100, blank=True, null=True)
    residential_taluka = models.CharField(max_length=100, blank=True, null=True)
    residential_district = models.CharField(max_length=100, blank=True, null=True)
    residential_state = models.CharField(max_length=100, blank=True, null=True)
    residential_country = models.CharField(max_length=100, blank=True, null=True)
    residential_zipcode = models.IntegerField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    permanent_city = models.CharField(max_length=100, blank=True, null=True)
    permanent_taluka = models.CharField(max_length=100, blank=True, null=True)
    permanent_district = models.CharField(max_length=100, blank=True, null=True)
    permanent_state = models.CharField(max_length=100, blank=True, null=True)
    permanent_country = models.CharField(max_length=100, blank=True, null=True)
    permanent_zipcode = models.IntegerField(blank=True, null=True)
    aadhar_no = models.CharField(max_length=20, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    accrued_not_received_int = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    adjusted_amount_at_disbursal = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    advance_instl_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    anchor_code = models.CharField(max_length=100, blank=True, null=True)
    anchor_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    billed_instalment_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_prin_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_int_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_bounce_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_bounce_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_bounce_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_bounce_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    days_past_due_other_charge = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    last_dpd_date_other_charge = models.DateField(blank=True, null=True)
    disbursal_flag = models.CharField(max_length=100, blank=True, null=True)
    disbursal_status = models.CharField(max_length=100, blank=True, null=True)
    currency_code = models.CharField(max_length=100, blank=True, null=True)
    installment_plan = models.CharField(max_length=100, blank=True, null=True)
    interest_frequency = models.CharField(max_length=100, blank=True, null=True)
    interest_rate_type = models.CharField(max_length=100, blank=True, null=True)
    last_billed_duedate = models.DateField(blank=True, null=True)
    loan_purpose = models.CharField(max_length=255, blank=True, null=True)
    group_id = models.CharField(max_length=100, blank=True, null=True)
    markup = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    next_cycle_duedate = models.DateField(blank=True, null=True)
    accounting_classification = models.CharField(max_length=100, blank=True, null=True)
    external_asset_classification = models.CharField(
        max_length=100, blank=True, null=True
    )
    external_npa_date = models.DateField(blank=True, null=True)
    cashback_adjusted_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_cashback_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    other_payable_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_other_charges_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_other_charges_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    accrual_stop_date = models.DateField(blank=True, null=True)
    actual_closure_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    npa_date = models.DateField(blank=True, null=True)
    int_prov_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    prin_prov_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_tds_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    invs_billed_tds_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    invs_tds_paid_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    tds_paid_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    additional_tds_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_moratorium_int_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    capitalize_int_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_capitalized_int_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    npa_flag = models.CharField(max_length=100, blank=True, null=True)
    frequency = models.CharField(max_length=100, blank=True, null=True)
    partprepayment_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    bucket = models.CharField(max_length=100, blank=True, null=True)
    coapp_gurantor = models.CharField(max_length=3, blank=True, null=True)
    effective_interest_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    no_of_overdue_installments = models.IntegerField(blank=True, null=True)
    interest_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    recd_prin_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_int_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_lpi_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_lpi_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_lpi_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_lpi_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_lpf_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    billed_lpf_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_lpf_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    recd_lpf_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_interest_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    overdue_prin_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    unallocated_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    overdue_int_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    unalloc_int_prepaid_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    unalloc_instl_prepaid_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    payable_lpi_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    payable_lpi_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    payable_lpf_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    payable_lpf_tax_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    unbilled_interest_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    mis_date = models.DateField(blank=True, null=True)
    closure_waive_off_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_other_charges_waiver_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_prin_int_waiver_amt = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    unallocated_closure_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    sourcing_rmname = models.CharField(max_length=255, blank=True, null=True)
    residual_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    residual_amount_paid_by = models.CharField(max_length=100, blank=True, null=True)
    due_day = models.IntegerField(blank=True, null=True)
    collateral_number = models.CharField(max_length=500, blank=True, null=True)
    excess_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_overdue = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    total_received_amount = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    principal_outstanding = models.DecimalField(
        max_digits=18, decimal_places=2, blank=True, null=True
    )
    
    load_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "loan_account"
        app_label = "loan"
