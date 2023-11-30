
import cv2
import numpy as np
from Elsed_tester.Model.filter_management import Filter, ParamGetter, ParamSetter
from typing import TypeAlias
from filter_builder import FilterBuilder
from numbers import Number
from image_loader import ImageLoader
from observers import ImageObserver, FilterListObserver

Filter_id : TypeAlias = str

class Model():

    def __init__(self, fb : FilterBuilder, pg : ParamGetter, ps : ParamSetter, il : ImageLoader) -> None:

        self.image           : np.array = None
        self.filters         : dict[Filter_id, Filter] = []
        self.order           : list[Filter_id] = []
        self.image_observers : list[ImageObserver] = []
        self.order_observers : list[FilterListObserver] = []

        self.filter_builder : FilterBuilder = fb
        self.param_getter   : ParamGetter = pg
        self.param_setter   : ParamSetter = ps
        self.image_loader   : ImageLoader = il

    ####

    def load_image(self, image_path : str) -> None:
            
        self.image = self.image_loader.load_image(image_path)

    def save_image(self, image_path : str) -> None:

        self.image_loader.save_image(image_path, self.display_image())

    #### 

    def update_image_observers(self):

        display = self.display_image()
        for observer in self.image_observers:
            observer.update(display)

    def update_order_observers(self):

        for observer in self.order_observers:
            observer.update(self.order)

    ####

    def get_order(self) -> list[Filter_id]:

        return self.order
    
    def set_order(self, order : list[Filter_id]) -> None:

        self.order = order
        self.update_order_observers()
        self.update_image_observers()


    ####

    def clear_filters(self) -> None:
            
        self.filters = {}
        self.order = []
    
    def add_filter(self, id : str, filter : Filter) -> None:

        self.filters[id] = filter
        self.order.append(id)

    def build_filter(self, filter_name : str, params : dict[str, Number]) -> Filter:

        return self.filter_builder.build(filter_name, params)
    
    def get_available_filters(self) -> list[str]:

        filters      = self.filter_builder.get_available_filters()
        dict_filters = {filter_name : self.get_default_filter_params(filter_name) for filter_name in filters}

        return dict_filters 

    def get_default_filter_params(self, filter_name : str) -> dict[str, Number]:

        sample_filter = self.filter_builder.build(filter_name)
        return self.param_getter.get_params(sample_filter)
    
    def get_using_filter_params(self, filter_id : Filter_id) -> dict[str, Number]:
            
        return self.param_getter.get_params(self.filters[filter_id])
    
    ### 

    def refresh(self) -> None:

        self.update_image_observers()
        self.update_order_observers()

    def display_image(self) -> np.array:

        img = self.image.copy()
        
        for id in self.order:
            img = self.filters[id].apply(img)
        
        return img
    

    
