import logging
from src.config import settings
import sys

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)

# Create a handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(settings.log_level)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
