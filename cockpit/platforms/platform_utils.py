from .aws_utils import *
from .serializers import *
from platform_state import *
import logging

logger=logging.getLogger("platforms")

def create_platform(platform_details):
    try:
        pass
    except Exception as e:
        logger.error("Error creating platform \n{}".format(e))
