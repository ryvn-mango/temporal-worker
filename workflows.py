from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import do_work


@workflow.defn
class PlaceholderWorkflow:
    """Backward-compat: drain any old queued PlaceholderWorkflow executions."""

    @workflow.run
    async def run(self, config: dict) -> str:
        return "drained"


@workflow.defn
class DoWorkWorkflow:
    @workflow.run
    async def run(self, duration_seconds: int) -> str:
        return await workflow.execute_activity(
            do_work,
            duration_seconds,
            start_to_close_timeout=timedelta(minutes=2),
        )
