
"""Load the property, rooms, and housekeepers from CSV files exactly once."""

import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from roomready.models import Property, Room, Housekeeper


def seed(session: Session, seed_dir: str = "seed") -> None:
    """Seed one property without duplicating records on restart."""
    property_obj = session.scalar(
        select(Property).where(Property.slug == "harbour-view")
    )

    if property_obj is None:
        property_obj = Property(
            slug="harbour-view",
            name="Harbour View",
        )
        session.add(property_obj)
        session.flush()

    property_id = property_obj.id
    directory = Path(seed_dir)

    rooms_file = directory / "rooms.csv"
    housekeepers_file = directory / "housekeepers.csv"

    existing_rooms = set(
        session.scalars(
            select(Room.no).where(Room.property_id == property_id)
        ).all()
    )

    with rooms_file.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["no"] in existing_rooms:
                continue

            session.add(
                Room(
                    property_id=property_id,
                    no=row["no"],
                    floor=int(row["floor"]),
                    type=row["type"],
                    out_of_order=False,
                )
            )

    existing_codes = set(
        session.scalars(
            select(Housekeeper.code).where(
                Housekeeper.property_id == property_id
            )
        ).all()
    )

    with housekeepers_file.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["id"] in existing_codes:
                continue

            session.add(
                Housekeeper(
                    property_id=property_id,
                    code=row["id"],
                    name=row["name"],
                )
            )

    session.commit()
