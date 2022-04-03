import os
import sys

import pandas as pd
from openpyxl import *
from CommonOs import OsServices as os_services


class BackupLogReview(os_services):
    """
    This class contains the methods to create a report of the existing backup files

    Args
        Required: none
        Optional: none

    Logging: WARN | ERROR

    """

    __author__ = "Barry Onizak"
    __version__ = "20220330.1"
    # # # # # End of header # # # #

    resource_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resource")
