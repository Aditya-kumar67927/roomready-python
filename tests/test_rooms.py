
"""Tests for RoomReady startup and room board."""

from pathlib import Path

from fastapi.testclient import TestClient

from roomready.app import create_app


def test_app_starts_twice_without_duplicate_rooms(tmp_path, monkeypatch):
    database_file = tmp_path / "roomready-test.db"
    seed_directory = Path(__file__).resolve().parents[1] / "seed"

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_file}")
    monkeypatch.setenv("SEED_DIR", str(seed_directory))

    # First application start.
    with TestClient(create_app()) as client:
        response = client.get("/properties/harbour-view/rooms")
        assert response.status_code == 200
        assert len(response.json()["rooms"]) == 60

    # Second application start, using the same database.
    with TestClient(create_app()) as client:
        response = client.get("/properties/harbour-view/rooms")
        assert response.status_code == 200
        assert len(response.json()["rooms"]) == 60

        board = response.json()
        assert board["property"] == "harbour-view"
