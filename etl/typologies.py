import pandas as pd
import numpy as np
from etl.extract import ProjectZero


class Typologies:
    '''
    DataFrames containing all features related to Typologies
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Typologies
        self.data = ProjectZero().get_data()
