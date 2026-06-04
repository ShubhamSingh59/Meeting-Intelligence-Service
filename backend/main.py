from fastapi import FastAPI, Request, HTTPException, Depends
from database.session import engine, Base
import uuid
from routers import meetings, action_items, auth
from services.webhook_service import notification_service
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.session import get_db
from datetime import datetime, timezone
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting background scheduler...")
    scheduler = AsyncIOScheduler()

    scheduler.add_job(notification_service.send_webhook, "interval", minutes=1)
    scheduler.start()

    yield  # This is where the application runs
    print("Shutting down background scheduler...")
    scheduler.shutdown()


app = FastAPI(
    title="Meeting Management API",
    description="Hintro Assignment",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    trace_id = getattr(request.state, "trace_id", "unknown")

    error_messages = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]

    return JSONResponse(
        status_code=400,
        content={
            "traceId": trace_id,
            "success": False,
            "error": {"code": "VALIDATION_ERROR", "message": "; ".join(error_messages)},
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    trace_id = getattr(request.state, "trace_id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "traceId": trace_id,
            "success": False,
            "error": {"code": "HTTP_ERROR", "message": exc.detail},
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    trace_id = getattr(request.state, "trace_id", "unknown")
    print(f"CRITICAL ERROR: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "traceId": trace_id,
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred.",
            },
        },
    )


## Middleware to add trace_id to each
@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id

    response = await call_next(request)

    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "trace_id": trace_id,
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
    }

    print(f"API_LOG: {log_data}")

    return response


@app.get("/")
def read_root():
    return {"message": "Welcome to the Meeting Management API!"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Ping the database to ensure the connection is alive
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "version": "1.0.0"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/api/evaluation")
def get_evaluation_details():
    return {
        "candidateName": "Shubham Singh",
        "email": "shubhams@alumni.iitgn.ac.in",
        "repositoryUrl": "https://github.com/ShubhamSingh59/Meeting-Intelligence-Service",
        "deployedUrl": "https://meeting-intelligence-service-zj75.onrender.com",
        "externalIntegration": "Discord Webhook API",
        "features": ["AI Analysis", "Reminder Scheduler", "Database Integration"],
    }


app.include_router(auth.router)
app.include_router(meetings.router)
app.include_router(action_items.router)
