import asyncio
import logging
from datetime import timedelta

from temporalio import activity, workflow

logger = logging.getLogger("temporal-worker")


@activity.defn
async def complete_after_delay() -> str:
    logger.info("Activity started, waiting 10 minutes before completing")
    await asyncio.sleep(600)
    logger.info("10 minute delay elapsed, completing")
    return "completed"


@workflow.defn
class PlaceholderWorkflow:
    @workflow.run
    async def run(self) -> str:
        result = await workflow.execute_activity(
            complete_after_delay,
            start_to_close_timeout=timedelta(minutes=15),
        )
        return result
