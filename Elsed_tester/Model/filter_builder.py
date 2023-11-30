import filters as f
import inspect
from numbers import Number

class FilterBuilder():

    def __init__(self):
        self.names = []
        for name, obj in inspect.getmembers(f):
            if inspect.isclass(obj) and obj.__module__ == 'filters':
                self.names.append(name)

        self.filters = {name : getattr(f, name) for name in self.names}

    def build(self, filter_name : str, params : dict[str, Number]) -> f.Filter:
        return self.filters[filter_name](**params)
    
    def get_available_filters(self) -> list[str]:
        return list(self.filters.keys()) 
    

if __name__ == '__main__':

    from filter_management import ParamGetter, ParamSetter
    import numpy as np
    import cv2

    fb = FilterBuilder()
    print("FILTERS = ", fb.filters)

    test = fb.build('Elsed', {'minLineLen' : 10, 'sigma' : 0.33, 'pxToSegmentDistTh' : 0.05, 'minArea' : 100, 'closing_kernel' : 5})
    print("BUILT GAUSSIAN BLUR = ", test)

    print("LIST OF NAMES OF AVAILABLE FILTERS = ", fb.get_available_filters())

    pg = ParamGetter()
    print("PARAMS OF A ELSED FILTER = ", pg.get_params(f.Elsed()))
    input()
    print("PARAMS OF GAUSSIAN BLUR FILTER ", pg.get_params(test))

    ps = ParamSetter()
    ps.set_params(test, {'ksize' : 7})
    print("NEW PARAMS OF GAUSSIAN BLUR FILTER ", pg.get_params(test))

    sample_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    cv2.imshow("sample", sample_img)
    print("SAMPLE IMAGE = ", sample_img.shape)
    applied = test.apply(sample_img)
    cv2.imshow("applied", applied)
    cv2.waitKey(0)