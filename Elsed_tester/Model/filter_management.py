import numpy as np 
from abc import ABC, abstractmethod
from numbers import Number
import cv2

class Filter(ABC):

    @abstractmethod
    def apply(self, image : np.array) -> np.array: ...

class ParamsFilter(Filter):

    @abstractmethod
    def apply(self, image : np.array) -> np.array: ...

class NoParamsFilter(Filter):

    @abstractmethod
    def apply(self, image : np.array) -> np.array: ...

class CompoundFilter(Filter):

    def __init__(self, filters : list[Filter]) -> None:

        self.filters : list[Filter] = filters

    def apply(self, image : np.array) -> np.array:

        img = image.copy()
        
        for filter in self.filters:
            img = np.uint8(filter.apply(img))
        
        return img
    
    def decompose(self) -> list[Filter]:

        return self.filters

class ParamSetter():

    def __init__(self) -> None:
        pass

    def set_params(self, filter : ParamsFilter, params : dict[str, Number]) -> None:
        for k in params.keys():
            if hasattr(filter, k):
                setattr(filter, k, params[k])

class ParamGetter():

    def __init__(self) -> None:
        pass

    def get_params(self, filter : ParamsFilter) -> dict[str, Number]:
        at_names = [attr for attr in dir(filter) if not callable(getattr(filter, attr)) and not attr.startswith("__") and not attr.startswith("_")]
        return {at_name : getattr(filter, at_name) for at_name in at_names}



    