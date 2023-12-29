import pandas as pd
import numpy as np
from etl.extract import ProjectZero


class Utilities:
    '''
    DataFrames containing all features related to Utilities
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Utilities
        self.data = ProjectZero().get_data()
