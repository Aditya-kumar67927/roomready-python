
"""HTTP endpoints for the RoomReady board."""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from roomready.schemas import (
    BoardOut,
    HousekeepersOut,
    RoomOut,
    RoomState,
    RoomType,
)

router = APIRouter()


def get_session(request: Request):
    session_factory = request.app.state.sessionmaker
    with session_factory() as session:
        yield session


@router.get(
    "/properties/{property}/rooms",
    response_model=BoardOut,
)
def list_rooms(
    property: str,
    floor: int | None = Query(default=None, ge=1, le=4),
    state: RoomState | None = None,
    type: RoomType | None = None,
    session: Session = Depends(get_session),
):
    from roomready.services.rooms import get_board

    return get_board(
        session,
        property_slug=property,
        floor=floor,
        state=state,
        room_type=type,
    )


@router.get(
    "/properties/{property}/rooms/{no}",
    response_model=RoomOut,
)
def room_detail(
    property: str,
    no: str,
    session: Session = Depends(get_session),
):
    from roomready.services.rooms import get_room

    return get_room(session, property, no)


@router.get(
    "/properties/{property}/housekeepers",
    response_model=HousekeepersOut,
)
def list_housekeepers(
    property: str,
    session: Session = Depends(get_session),
):
    from roomready.services.rooms import get_housekeepers

    return get_housekeepers(session, property)
