import pytest
from rest_framework.test import APIClient

from apps.common.factories import MembershipFactory, MembershipTierFactory, ToyFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def member():
    return UserFactory()


@pytest.fixture
def staff_user():
    return UserFactory(is_staff=True)


@pytest.fixture
def member_client(member):
    client = APIClient()
    client.force_authenticate(user=member)
    return client


@pytest.fixture
def staff_client(staff_user):
    client = APIClient()
    client.force_authenticate(user=staff_user)
    return client


@pytest.fixture
def silver_tier():
    return MembershipTierFactory(code="SILVER")


@pytest.fixture
def active_membership(member, silver_tier):
    return MembershipFactory(user=member, tier=silver_tier)


@pytest.fixture
def toy():
    return ToyFactory()
