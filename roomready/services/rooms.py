
"""Room board service: derive room state from database records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from roomready.models import Property, Room, Housekeeper
from roomready.schemas import RoomOut, BoardOut, HousekeeperOut, HousekeepersOut
from roomready.errors import NoSuchProperty, NoSuchRoom


def get_board(
    session: Session,
    property_slug: str,
    floor: int | None = None,
    state: str | None = None,
    room_type: str | None = None,
) -> BoardOut:
    prop = session.scalar(select(Property).where(Property.slug == property_slug))
    if prop is None:
        raise NoSuchProperty("Property not found")

    query = select(Room).where(Room.property_id == prop.id)
    if floor is not None:
        query = query.where(Room.floor == floor)
    if room_type is not None:
        query = query.where(Room.type == room_type)

    rows = session.scalars(query.order_by(Room.no)).all()
    rooms = [
        RoomOut(
            no=r.no,
            floor=r.floor,
            type=r.type,
            state="out_of_order" if r.out_of_order else "occupied",
        )
        for r in rows
        if state is None or state == ("out_of_order" if r.out_of_order else "occupied")
    ]

    return BoardOut(
        property=prop.slug,
        ready=sum(r.state == "ready" for r in rooms),
        dirty=sum(r.state == "dirty" for r in rooms),
        rooms=rooms,
    )


def get_room(session: Session, property_slug: str, room_no: str) -> RoomOut:
    prop = session.scalar(select(Property).where(Property.slug == property_slug))
    if prop is None:
        raise NoSuchProperty("Property not found")

    room = session.scalar(
        select(Room).where(Room.property_id == prop.id, Room.no == room_no)
    )
    if room is None:
        raise NoSuchRoom("No such room in this property")

    return RoomOut(
        no=room.no,
        floor=room.floor,
        type=room.type,
        state="out_of_order" if room.out_of_order else "occupied",
    )


def get_housekeepers(session: Session, property_slug: str) -> HousekeepersOut:
    prop = session.scalar(select(Property).where(Property.slug == property_slug))
    if prop is None:
        raise NoSuchProperty("Property not found")

    staff = session.scalars(
        select(Housekeeper)
        .where(Housekeeper.property_id == prop.id)
        .order_by(Housekeeper.code)
    ).all()

    return HousekeepersOut(
        housekeepers=[
            HousekeeperOut(id=h.code, name=h.name, open_assignment=None)
            for h in staff
        ]
    )
