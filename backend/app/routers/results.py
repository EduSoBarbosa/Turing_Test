from fastapi import APIRouter, Depends, Request, Response

from app.routers.admin import authenticate
from app.services import analytics_service


router = APIRouter(prefix="/admin/results", tags=["Administration"], dependencies=[Depends(authenticate)])


@router.get("")
def results(request: Request):
    with request.app.state.experiments.sessions() as db:
        return analytics_service.results(db)


@router.get("/export", response_class=Response)
def export(request: Request):
    with request.app.state.experiments.sessions() as db:
        return Response(
            analytics_service.export_csv(db), media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="turing-test-results.csv"'},
        )
