import logging

from temporalio import workflow

logger = logging.getLogger("temporal-worker")


def _burn_cpu(work_units: int) -> int:
    total = 0
    for i in range(work_units):
        total = (total + ((i * 17) % 13)) % 1_000_000_007
    return total


@workflow.defn
class PlaceholderWorkflow:
    @workflow.run
    async def run(self, work_units: int) -> str:
        logger.info("Workflow started with %d work units", work_units)

        # Demo-only: spend CPU in the workflow task itself so backlog appears
        # on the workflow queue instead of the activity queue.
        checksum = _burn_cpu(work_units)

        logger.info("Workflow finished CPU burn with checksum %d", checksum)
        return f"completed:{checksum}"
