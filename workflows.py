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
    async def run(self, config: dict[str, int]) -> str:
        rounds = int(config["rounds"])
        work_units = int(config["work_units"])
        pause_seconds = int(config["pause_seconds"])

        logger.info(
            "Workflow started with %d rounds, %d work units per round, %d second pause",
            rounds,
            work_units,
            pause_seconds,
        )

        checksum = 0
        for round_index in range(rounds):
            # Keep each workflow task short enough to avoid Temporal's
            # deadlock detector while still creating meaningful queue work.
            checksum = _burn_cpu(work_units)

            if round_index + 1 < rounds:
                await workflow.sleep(pause_seconds)

        logger.info("Workflow finished %d rounds with checksum %d", rounds, checksum)
        return f"completed:{checksum}"
