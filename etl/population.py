import pandas as pd
import numpy as np
from etl.extract import ProjectZero


class Population:
    '''
    DataFrames containing all features related to Population
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Population
        self.data = ProjectZero().get_data()
