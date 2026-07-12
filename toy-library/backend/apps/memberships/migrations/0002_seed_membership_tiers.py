from decimal import Decimal

from django.db import migrations

TIERS = [
    dict(
        code="SILVER",
        name="Silver",
        joining_fee=Decimal("25.00"),
        deposit_amount=Decimal("50.00"),
        renewal_fee=Decimal("12.50"),
        max_concurrent_checkouts=1,
        loan_period_days=14,
        complimentary_extension_days=2,
    ),
    dict(
        code="PLATINUM",
        name="Platinum",
        joining_fee=Decimal("35.00"),
        deposit_amount=Decimal("75.00"),
        renewal_fee=Decimal("17.50"),
        max_concurrent_checkouts=2,
        loan_period_days=14,
        complimentary_extension_days=3,
    ),
    dict(
        code="DIAMOND",
        name="Diamond",
        joining_fee=Decimal("40.00"),
        deposit_amount=Decimal("80.00"),
        renewal_fee=Decimal("20.00"),
        max_concurrent_checkouts=5,
        loan_period_days=21,
        complimentary_extension_days=5,
    ),
]


def seed_tiers(apps, schema_editor):
    MembershipTier = apps.get_model("memberships", "MembershipTier")
    for tier in TIERS:
        MembershipTier.objects.update_or_create(code=tier["code"], defaults=tier)


def unseed_tiers(apps, schema_editor):
    MembershipTier = apps.get_model("memberships", "MembershipTier")
    MembershipTier.objects.filter(code__in=[t["code"] for t in TIERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("memberships", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_tiers, unseed_tiers),
    ]
