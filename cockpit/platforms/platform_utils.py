from .aws_utils import *
from .serializers import *
from platform_state import *


def create_platform(platform_details):
    try:
        pass
    except Exception as e:
        print("Error creating platform \n{}".format(e))
