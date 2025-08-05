from django.db import models


class LoanMisSnapshot(models.Model):
    loan_account = models.TextField(blank=True, null=True)
    accrued_not_received_int = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    adjusted_amount_at_disbursal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    advance_instl_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    anchor_code = models.TextField(blank=True, null=True)
    anchor_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    no_of_balance_installments = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    billed_instalment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    billed_bounce_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    billed_bounce_tax_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    recd_bounce_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    recd_bounce_tax_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    days_past_due_other_charge = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    last_dpd_date_other_charge = models.DateField(blank=True, null=True)
    disbursal_flag = models.TextField(blank=True, null=True)
    disbursal_status = models.TextField(blank=True, null=True)
    currency_code = models.TextField(blank=True, null=True)
    installment_plan = models.TextField(blank=True, null=True)
    interest_frequency = models.TextField(blank=True, null=True)
    interest_rate_type = models.TextField(blank=True, null=True)
    last_billed_duedate = models.DateField(blank=True, null=True)
    loan_purpose = models.TextField(blank=True, null=True)
    group_id = models.TextField(blank=True, null=True)
    markup = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    next_cycle_duedate = models.DateField(blank=True, null=True)
    total_no_of_bounce = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    external_asset_classification = models.TextField(blank=True, null=True)
    external_npa_date = models.DateField(blank=True, null=True)
    cashback_adjusted_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_cashback_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    other_payable_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    recd_other_charges_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    recd_other_charges_tax_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    accrual_stop_date = models.DateField(blank=True, null=True)
    actual_closure_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    npa_date = models.DateField(blank=True, null=True)
    int_prov_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    prin_prov_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    billed_tds_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    invs_billed_tds_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    invs_tds_paid_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    tds_paid_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    additional_tds_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_moratorium_int_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    capitalize_int_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    total_capitalized_int_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    npa_flag = models.TextField(blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    partprepayment_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    unallocated_amt = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    bucket = models.TextField(blank=True, null=True)
    coapp_guarantor = models.TextField(blank=True, null=True)
    effective_interest_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    no_of_overdue_installments = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    mis_date = models.DateField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "loan_mis_snapshot"
