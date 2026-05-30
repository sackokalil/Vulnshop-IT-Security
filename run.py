from src.app import create_app
from src.config.config import Config
from src.database.db import init_db
import os

app = create_app()

if not os.path.exists(Config.DATABASE):
    init_db()

if __name__=="__main__":
    app.run()
