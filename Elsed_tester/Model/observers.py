from abc import ABC, abstractmethod
from filter_management import Filter
import numpy as np

class FilterListObserver(ABC):

    @abstractmethod
    def update(self, filter_list : list[Filter]) -> None: ...

class ImageObserver(ABC):

    @abstractmethod
    def update(self, image : np.array) -> None: ...