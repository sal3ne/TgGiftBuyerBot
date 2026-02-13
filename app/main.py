import asyncio
import threading
from app.healthcheck import run_server
from app.infrastructure.telegram.bot import main

# Запускаем healthcheck в отдельном потоке
threading.Thread(target=run_server, daemon=True).start()

if __name__ == "__main__":
    asyncio.run(main())
