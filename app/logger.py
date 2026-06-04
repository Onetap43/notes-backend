import logging
import json
from datetime import datetime,timezone
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "time": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage()
        }
        if hasattr(record, "event"):
            log_data["event"] = record.event

        if hasattr(record, "username"):
            log_data["username"] = record.username

        return json.dumps(log_data)
logger = logging.getLogger("notes_backend")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())

logger.handlers.clear()
logger.addHandler(console_handler)
logger.propagate = False