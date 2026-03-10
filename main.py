import asyncio
import logging
import os
import time

from fastapi import FastAPI, Request
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import PlaceholderWorkflow, complete_after_delay

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("temporal-worker")

TEMPORAL_ENDPOINT = os.environ["TEMPORAL_ENDPOINT"]
TEMPORAL_NAMESPACE = os.environ["TEMPORAL_NAMESPACE"]
TEMPORAL_API_KEY = os.environ["TEMPORAL_API_KEY"]
TASK_QUEUE = "temporal-worker-queue"

app = FastAPI(title="temporal-worker")


async def start_temporal_worker():
    logger.info("Connecting to Temporal at %s", TEMPORAL_ENDPOINT)
    client = await Client.connect(
        TEMPORAL_ENDPOINT,
        namespace=TEMPORAL_NAMESPACE,
        rpc_metadata={"temporal-namespace": TEMPORAL_NAMESPACE},
        api_key=TEMPORAL_API_KEY,
        tls=True,
    )
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[PlaceholderWorkflow],
        activities=[complete_after_delay],
        max_concurrent_workflow_tasks=10,
        max_concurrent_activities=10,
    )
    logger.info("Starting Temporal worker on queue '%s'", TASK_QUEUE)
    await worker.run()


@app.on_event("startup")
async def startup():
    asyncio.create_task(start_temporal_worker())


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("%s %s %d %.1fms", request.method, request.url.path, response.status_code, elapsed_ms)
    return response


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
