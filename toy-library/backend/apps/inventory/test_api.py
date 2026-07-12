import pytest

from apps.common.factories import ToyFactory

from .models import Toy


@pytest.mark.django_db
class TestToyList:
    def test_requires_authentication(self, api_client):
        res = api_client.get("/api/toys/")
        assert res.status_code == 401

    def test_authenticated_member_can_list(self, member_client, toy):
        res = member_client.get("/api/toys/")
        assert res.status_code == 200
        assert len(res.data["results"]) == 1

    def test_status_filter(self, member_client):
        ToyFactory(status=Toy.Status.AVAILABLE)
        ToyFactory(status=Toy.Status.BROKEN)

        res = member_client.get("/api/toys/?status=AVAILABLE")

        assert res.status_code == 200
        assert all(t["status"] == "AVAILABLE" for t in res.data["results"])

    def test_search_filter(self, member_client):
        ToyFactory(model_name="Wooden Train", make="Acme")
        ToyFactory(model_name="Puzzle Cube", make="Other")

        res = member_client.get("/api/toys/?search=Train")

        assert res.status_code == 200
        assert len(res.data["results"]) == 1
        assert res.data["results"][0]["model_name"] == "Wooden Train"


@pytest.mark.django_db
class TestToyCreate:
    def test_member_cannot_create_toy(self, member_client):
        res = member_client.post("/api/toys/", {"model_name": "New Toy", "make": "Acme"})
        assert res.status_code == 403

    def test_staff_can_create_toy_starting_in_intake(self, staff_client):
        res = staff_client.post("/api/toys/", {"model_name": "New Toy", "make": "Acme"})

        assert res.status_code == 201
        assert res.data["status"] == "INTAKE"

    def test_status_field_is_read_only_on_create(self, staff_client):
        res = staff_client.post(
            "/api/toys/", {"model_name": "New Toy", "make": "Acme", "status": "AVAILABLE"}
        )

        assert res.status_code == 201
        assert res.data["status"] == "INTAKE"


@pytest.mark.django_db
class TestToyTransition:
    def test_staff_can_transition_toy(self, staff_client):
        toy = ToyFactory(status=Toy.Status.INTAKE)

        res = staff_client.post(
            f"/api/toys/{toy.id}/transition/", {"new_status": "AVAILABLE", "reason": "Stocked"}
        )

        assert res.status_code == 200
        assert res.data["status"] == "AVAILABLE"

    def test_illegal_transition_returns_400(self, staff_client):
        toy = ToyFactory(status=Toy.Status.RETIRED)

        res = staff_client.post(f"/api/toys/{toy.id}/transition/", {"new_status": "AVAILABLE"})

        assert res.status_code == 400

    def test_member_cannot_transition_toy(self, member_client, toy):
        res = member_client.post(f"/api/toys/{toy.id}/transition/", {"new_status": "BROKEN"})
        assert res.status_code == 403

    def test_status_log_records_transition(self, staff_client):
        toy = ToyFactory(status=Toy.Status.INTAKE)
        staff_client.post(f"/api/toys/{toy.id}/transition/", {"new_status": "AVAILABLE", "reason": "x"})

        res = staff_client.get(f"/api/toys/{toy.id}/status-log/")

        assert res.status_code == 200
        assert len(res.data) == 1
        assert res.data[0]["from_status"] == "INTAKE"
        assert res.data[0]["to_status"] == "AVAILABLE"
