# yourapp/management/commands/seed_loan_accounts.py

from django.core.management.base import BaseCommand
from loan.models.LoanAccount import LoanAccount
from datetime import date
import random


class Command(BaseCommand):
    help = "Seed loan accounts into the LoanAccount model"

    def handle(self, *args, **kwargs):
        # List of sample data to insert into LoanAccount model
        loan_data = [
            {
                "loan_account": f"LN00{n}",
                "loan_id": f"LID00{n}",
                "customer_id": f"CID00{n}",
                "loan_status": random.choice(["Active", "Closed", "Overdue"]),
                "customer_name": f"Customer {n}",
                "branch_name": f"Branch {random.choice(['A', 'B', 'C', 'D'])}",
                "branch_state": f"State {random.choice(['X', 'Y', 'Z'])}",
                "scheme_name": f"Scheme {random.choice(['A', 'B', 'C'])}",
                "total_outstanding": round(random.uniform(1000, 20000), 2),
                "total_overdue": round(random.uniform(100, 1000), 2),
                "principal_outstanding": round(random.uniform(1000, 15000), 2),
                "od_principal_amt": round(random.uniform(50, 500), 2),
                "od_interest_amt": round(random.uniform(10, 100), 2),
                "balance_principal": round(random.uniform(1000, 15000), 2),
                "total_received_amount": round(random.uniform(1000, 5000), 2),
                "excess_amount": str(round(random.uniform(0, 500), 2)),
                "closure_date": None,
                "asset_classification": random.choice(["Class A", "Class B"]),
                "days_past_due_dpd": round(random.uniform(0, 60), 2),
                "application_received_date": date(2025, 1, random.randint(1, 28)),
                "sanction_date": date(2025, 2, random.randint(1, 28)),
                "tenure": round(random.uniform(6, 36), 2),
                "apr_rate": round(random.uniform(5, 15), 2),
                "interest_start_date": date(2025, 3, random.randint(1, 28)),
                "maturity_date": date(2026, 3, random.randint(1, 28)),
                "disbursal_date": date(2025, 4, random.randint(1, 28)),
                "first_installment_due_date": date(2025, 5, random.randint(1, 28)),
                "sanctioned_amount": round(random.uniform(10000, 25000), 2),
                "disbursal_amount": round(random.uniform(10000, 24000), 2),
                "net_disbursed_amount": round(random.uniform(10000, 23000), 2),
                "application_number": f"APP00{n}",
                "cre_name": f"CRE{random.randint(1, 10)}",
                "cre_code": f"CRE{random.randint(1, 10)}",
                "installment_amount": round(random.uniform(1000, 5000), 2),
                "ltv": round(random.uniform(50, 90), 2),
                "no_of_balance_installments": random.randint(1, 12),
                "last_receipt_amount": round(random.uniform(500, 1000), 2),
                "last_receipt_date": date(2025, 6, random.randint(1, 28)),
                "total_no_of_bounce": random.randint(0, 3),
                "last_bounce_date": (
                    None
                    if random.random() < 0.8
                    else date(2025, 5, random.randint(1, 28))
                ),
                "last_bounce_reason": (
                    None
                    if random.random() < 0.8
                    else random.choice(["Insufficient Funds", "Technical Error"])
                ),
                "closure_waive_off_amount": 0.0,
                "repayment_mode": random.choice(["EMI", "Bullet"]),
                "payment_mode": random.choice(["Online", "Cheque", "Cash"]),
                "cibil_score": f"{random.randint(650, 800)}",
                "rate_of_interest": round(random.uniform(5, 15), 2),
                "delivery_order_no": f"DO00{n}",
                "billed_int_amt": round(random.uniform(100, 1500), 2),
                "billed_prin_amt": round(random.uniform(1000, 15000), 2),
                "total_accrued_interest": round(random.uniform(10, 1000), 2),
                "collateral_number": f"COLL00{n}",
                "repo_flag": random.choice(["Y", "N"]),
                "storeroom_status_flag": random.choice(["Y", "N"]),
                "gender": random.choice(["Male", "Female"]),
                "marital_status": random.choice(["Single", "Married"]),
                "primary_mobile_number": f"9{random.randint(100000000, 999999999)}",
                "dob": date(
                    1980 + random.randint(0, 20),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
                "asset_model": f"Model {random.choice(['X', 'Y', 'Z'])}",
                "manufacturer": random.choice(["Manufacturer A", "Manufacturer B"]),
                "dealer": random.choice(["Dealer A", "Dealer B"]),
                "sub_dealer": random.choice(["Sub Dealer A", "Sub Dealer B"]),
                "asset_cost": round(random.uniform(5000, 50000), 2),
                "chasis_number": f"CH1234{n}",
                "engine_number": f"EN1234{n}",
                "registration_number": f"REG1234{n}",
                "accomodation_type": random.choice(["Owned", "Rented"]),
                "residential_address": f"Address {n}",
                "residential_city": f"City {random.choice(['A', 'B', 'C'])}",
                "residential_taluka": f"Taluka {random.choice(['X', 'Y', 'Z'])}",
                "residential_district": f"District {random.choice(['A', 'B', 'C'])}",
                "residential_state": f"State {random.choice(['X', 'Y', 'Z'])}",
                "residential_country": f"Country {random.choice(['India', 'US', 'UK'])}",
                "residential_zipcode": f"{random.randint(100000, 999999)}",
                "permanent_address": f"Permanent Address {n}",
                "permanent_city": f"Permanent City {n}",
                "permanent_taluka": f"Permanent Taluka {n}",
                "permanent_district": f"Permanent District {n}",
                "permanent_state": f"Permanent State {n}",
                "permanent_country": f"Permanent Country {n}",
                "permanent_zipcode": f"{random.randint(100000, 999999)}",
                "aadhar_no": f"1234 5678 9012",
                "pan": f"ABCDE{random.randint(1000, 9999)}F",
                "mis_date": date.today(),
                "created_at": date.today(),
            }
            for n in range(1, 11)  # Creating 10 rows
        ]

        # Inserting the rows into the LoanAccount model
        for data in loan_data:
            LoanAccount.objects.create(**data)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded 10 LoanAccount records.")
        )
