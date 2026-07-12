from decimal import Decimal

import pytest

from apps.billing.models import LedgerEntry
from apps.billing.services import create_ledger_entry
from apps.checkouts import services as checkout_services
from apps.common.factories import MembershipFactory, MembershipTierFactory, ToyFactory, UserFactory
from apps.memberships import services
from apps.memberships.models import Membership


@pytest.mark.django_db
def test_signoff_blocked_by_active_checkout():
    membership = MembershipFactory()
    toy = ToyFactory()
    staff = UserFactory(is_staff=True)
    checkout_services.create_checkout(toy, membership.user, staff)

    with pytest.raises(ValueError, match="active or overdue checkouts"):
        services.process_signoff(membership, staff, Decimal("50.00"), "")


@pytest.mark.django_db
def test_signoff_blocked_by_outstanding_charge():
    membership = MembershipFactory()
    staff = UserFactory(is_staff=True)
    create_ledger_entry(
        user=membership.user,
        entry_type=LedgerEntry.EntryType.LATE_FEE,
        amount=Decimal("1.50"),
        direction=LedgerEntry.Direction.CHARGE,
    )

    with pytest.raises(ValueError, match="outstanding unpaid charges"):
        services.process_signoff(membership, staff, Decimal("50.00"), "")


@pytest.mark.django_db
def test_signoff_requires_reason_for_partial_refund():
    membership = MembershipFactory()
    staff = UserFactory(is_staff=True)

    with pytest.raises(ValueError, match="deduction_reason"):
        services.process_signoff(membership, staff, Decimal("30.00"), "")

    sign_off = services.process_signoff(membership, staff, Decimal("30.00"), "Toy returned damaged")
    membership.refresh_from_db()
    assert membership.status == Membership.Status.DISCONTINUED
    assert sign_off.deposit_amount_returned == Decimal("30.00")


@pytest.mark.django_db
def test_change_tier_upgrade_charges_deposit_difference_and_defers_tier_change():
    silver = MembershipTierFactory(code="SILVER", deposit_amount=Decimal("50.00"))
    diamond = MembershipTierFactory(code="DIAMOND", deposit_amount=Decimal("80.00"))
    membership = MembershipFactory(tier=silver)
    staff = UserFactory(is_staff=True)

    services.change_tier(membership, diamond, staff)
    membership.refresh_from_db()

    # Tier does not change yet -- an upgrade charge is pending payment.
    assert membership.tier == silver
    pending_charge = membership.user.ledger_entries.get()
    assert pending_charge.amount == Decimal("30.00")
    assert pending_charge.status == LedgerEntry.Status.PENDING

    from apps.billing.services import mark_paid

    mark_paid(pending_charge, staff)
    membership.refresh_from_db()
    assert membership.tier == diamond


@pytest.mark.django_db
def test_change_tier_downgrade_credits_immediately():
    diamond = MembershipTierFactory(code="DIAMOND", deposit_amount=Decimal("80.00"))
    silver = MembershipTierFactory(code="SILVER", deposit_amount=Decimal("50.00"))
    membership = MembershipFactory(tier=diamond)
    staff = UserFactory(is_staff=True)

    services.change_tier(membership, silver, staff)
    membership.refresh_from_db()

    assert membership.tier == silver
    credit = membership.user.ledger_entries.get()
    assert credit.amount == Decimal("30.00")
    assert credit.direction == LedgerEntry.Direction.CREDIT
    assert credit.status == LedgerEntry.Status.PAID
