import json
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app


def test_f03_returned_job_id_retrieves_ticket_state():
    """
    F03 regression test:
    The job ID returned to the user should retrieve
    the corresponding ticket's stored state.
    """

    job_id = "job-123"
    ticket_id = "ticket-456"

    stored_states = {
        f"state:{ticket_id}": json.dumps({
            "ticket_id": ticket_id,
            "status": "PAUSED_FOR_REVIEW"
        })
    }

    def fake_redis_get(key):
        return stored_states.get(key)

    with patch("main.redis_client") as mock_redis:
        mock_redis.get.side_effect = fake_redis_get

        client = TestClient(app)

        response = client.get(f"/api/v1/state/{job_id}")

    assert response.status_code == 200, (
        f"F03: Expected 200, but received {response.status_code}. "
        "The status endpoint could not retrieve the ticket using its job ID."
    )

    assert response.json()["ticket_id"] == ticket_id
