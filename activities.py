import asyncio

from temporalio import activity


@activity.defn
async def do_work(duration_seconds: int) -> str:
    activity.logger.info("Starting work for %d seconds", duration_seconds)
    await asyncio.sleep(duration_seconds)
    return f"Completed {duration_seconds}s of work"
