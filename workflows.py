import asyncio
import logging
from datetime import timedelta

from temporalio import activity, workflow

logger = logging.getLogger("temporal-worker")


@activity.defn
async def complete_after_delay() -> str:
    logger.info("Activity started, waiting 15 seconds before completing")
    await asyncio.sleep(15)
    logger.info("15 second delay elapsed, completing")
    return "completed"


@workflow.defn
class PlaceholderWorkflow:
    @workflow.run
    async def run(self) -> str:
        result = await workflow.execute_activity(
            complete_after_delay,
            start_to_close_timeout=timedelta(minutes=2),
        )
        return result
