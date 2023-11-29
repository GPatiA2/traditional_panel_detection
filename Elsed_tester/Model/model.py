
import cv2
import numpy as np
from filter import Filter
from typing import TypeAlias

Filter_id : TypeAlias = str

class Model():

    def __init__(self):

        self.image        : np.array = None
        self.image_path   : str = None
        self.filters      : dict[Filter_id, Filter] = []

    def load_image(self, image_path : str) -> None:

        self.image_path = image_path
        self.image = cv2.imread(image_path)

    def add_filter(self, filter : Filter) -> None:

        self.filters_applied.append(filter)

    def display_image(self, order : list[Filter_id]) -> np.array:

        img = self.image.copy()
        
        for id in order:
            img = self.filters[id].apply(img)
        
        return img
    
    def save_image(self, image_path : str) -> None:

        img = self.display_image()
        cv2.imwrite(image_path, img)

    
