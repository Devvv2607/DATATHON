from fastapi import APIRouter, HTTPException

from .reddit_service import fetch_reddit_graph
from .schema import RedditGraphRequest, SocialGraphResponse

router = APIRouter(prefix="/api/social-graph", tags=["Social Graph"])


@router.post("/reddit", response_model=SocialGraphResponse)
async def reddit_social_graph(
    payload: RedditGraphRequest
) -> SocialGraphResponse:
    """
    Build a Reddit social graph based on keyword search.
    
    Returns posts, comments, users, and their relationships as a network graph.
    """
    try:
        response = await fetch_reddit_graph(payload)
        return response
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Failed to build Reddit graph") from exc
