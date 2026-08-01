from aiohttp.web import Application, AppRunner, TCPSite, Response
import logging

logger = logging.getLogger(__name__)

PORT:int = 8080

async def checkHealth(request):
    return Response(text="Server Running...", content_type="text/plain")

async def startServer() -> None:
    app = Application()
    app.router.add_get("/", checkHealth)
    app.router.add_get("/healthz", checkHealth)
    runner = AppRunner(app, access_log=None)
    await runner.setup()
    site = TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"HTTP server listening on port {PORT}")