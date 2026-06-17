import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler


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
    )
    scheduler.start()

    print(f"Scheduler iniciado. Intervalo: {INTERVALO_MINUTOS} minuto(s).")
    print("Pressione Ctrl+C para parar.")

    await job()

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler encerrado.")
