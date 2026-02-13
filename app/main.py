import asyncio

from app.infrastructure.telegram.bot import main
import threading
from app.healthcheck import run_server
threading.Thread(target=run_server, daemon=True).start()
if __name__ == "__main__":
    asyncio.run(main())
