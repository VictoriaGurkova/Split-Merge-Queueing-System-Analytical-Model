import logging
from collections import defaultdict

import numpy as np
from scipy.linalg import expm

from data_store import PerformanceMeasures
from network_params import Params
from states_utils import *
from utils import *

logger = logging.getLogger()


# TODO: make the main calculation class
class QueueingSystem:

    def __init__(self, params: Params):
        self.params = params
        self.data = PerformanceMeasures()

        self.x = params.devices_amount // params.fragments_amounts[0]
        self.y = params.devices_amount // params.fragments_amounts[1]
