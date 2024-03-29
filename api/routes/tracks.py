from fastapi import APIRouter
from api.models.requests.track import Track
from api.controllers.tracks_controller import TracksController
from api.models.responses.track import Track as TrackResponse

router = APIRouter(tags=["Tracks"])


@router.post("/tracks", status_code=201, response_model=TrackResponse)
async def create_user(track: Track):
    return TracksController.create(track)
