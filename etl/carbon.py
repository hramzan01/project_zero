import pandas as pd
import numpy as np
from etl.extract import ProjectZero


class Carbon:
    '''
    DataFrames containing all features related to embodied carbon
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of carbon
        self.data = ProjectZero().get_data()
