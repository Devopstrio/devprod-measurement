import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("devprod-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="DevProd Measurement Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics/dora")
def get_dora_metrics():
    return {
        "deployment_frequency": "12.4 / week",
        "lead_time_for_changes": "1.2 days",
        "change_failure_rate": "4.2%",
        "time_to_restore_service": "45 mins",
        "rating": "Elite"
    }

@app.get("/metrics/flow")
def get_flow_metrics():
    return {
        "flow_efficiency": "64%",
        "active_wip_per_dev": 2.4,
        "avg_pr_cycle_time": "14h",
        "bottleneck_alerts": 2
    }

@app.get("/metrics/productivity")
def get_productivity_summary():
    return {
        "global_effectiveness_score": 0.882,
        "productivity_trend": "UP",
        "primary_bottleneck": "PR Review Latency (Team A)",
        "onboarding_velocity": "4.2 days to first PR"
    }

@app.get("/surveys/results")
def get_survey_results():
    return {
        "overall_satisfaction": 4.2,
        "participation_rate": "84%",
        "top_sentiment_driver": "Golden Path Templates"
    }

@app.get("/benchmarks")
def get_benchmarks():
    return [
        {"team": "Team Alpha", "score": 0.92, "rating": "Elite"},
        {"team": "Team Beta", "score": 0.84, "rating": "High"},
        {"team": "Platform Core", "score": 0.88, "rating": "High"}
    ]

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_active_engineers": 450,
        "active_pipelines": 124,
        "platform_roi_est": "$4.2M / year",
        "engineering_health": "OPTIMAL"
    }
