import asyncio
import logging
import os
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler


logger = logging.getLogger("promobot.scheduler")

INTERVALO_MINUTOS = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "10"))


async def iniciar_scheduler(job):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        job,
        trigger="interval",
        minutes=INTERVALO_MINUTOS,
        id="buscar_promocoes",
        max_instances=1,
        coalesce=True,
        
        next_run_time=datetime.now(timezone.utc),
    )
    scheduler.start()

    logger.info("Scheduler iniciado. Intervalo: %d minuto(s).", INTERVALO_MINUTOS)
    logger.info("Pressione Ctrl+C para parar.")

    try:
       
        await asyncio.Event().wait()
    finally:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler encerrado.")