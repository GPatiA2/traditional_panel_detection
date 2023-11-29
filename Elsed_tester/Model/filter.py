
import cv2
import numpy as np 
from abc import ABC, abstractmethod
from numbers import Number

class Filter(ABC):

    @abstractmethod
    def apply(self, image : np.array) -> np.array: ...

class ParamsFilter(Filter):

    def __init__(self, allowed_params : dict[str, dict[str, Number]]):
        self.allowed_params = allowed_params

    @abstractmethod
    def apply(self, image : np.array) -> np.array: ...

    def check_params(self, params : dict[str, str]) -> bool:
        for key in params.keys():
            if key not in self.allowed_params:
                return False
        return True
    
    def get_params(self) -> dict[str, dict[str, dict[str, Number]]]:
        return self.allowed_params

class NoParamsFilter(Filter):

    @abstractmethod
    def apply(self, image : np.array) -> np.array: ...

