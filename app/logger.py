import logging
logger=logging.getLogger("notes_backend")
logger.setLevel(logging.INFO)
console_handler=logging.StreamHandler()
log_format=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)