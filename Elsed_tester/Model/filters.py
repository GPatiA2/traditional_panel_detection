from filter_management import *
import cv2
import pyelsed as elsed

class toHSV(NoParamsFilter):
    
    def __init__(self) -> None:
        pass

    def apply(self, image : np.array) -> np.array:
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

class toBGR(NoParamsFilter):

    def __init__(self) -> None:
        pass

    def apply(self, image : np.array) -> np.array:
        return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    
class toGRAY(NoParamsFilter):

    def __init__(self) -> None:
        pass

    def apply(self, image : np.array) -> np.array:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
class ChannelFilter(ParamsFilter):

    def __init__(self, channel : int = 0, lwt : int = 0, hgt : int = 255) -> None:
        self.channel      : int = channel
        self.lw_threshold : int = lwt
        self.hi_threshold : int = hgt

    def apply(self, image : np.array) -> np.array:
        channel  = image[:,:,self.channel]
        
        mask           = np.zeros_like(channel)
        mask_idx       = np.where(np.logical_and(channel >= self.lw_threshold, channel <= self.hi_threshold), 255, 0)
        mask[mask_idx] = 255 

        channel[mask == 0] = 0

        image[:,:,self.channel] = channel

        return image
    
class MultiChannelFilter(ParamsFilter):

    def __init__(self, l_th1 : int = 0, h_th1 : int = 255, l_th2 : int = 0, h_th2 : int = 255, l_th3 : int = 0, h_th3 : int = 255) -> None:
        self.l_th1 : int = l_th1
        self.h_th1 : int = h_th1
        self.l_th2 : int = l_th2
        self.h_th2 : int = h_th2
        self.l_th3 : int = l_th3
        self.h_th3 : int = h_th3

    def apply(self, image : np.array) -> np.array:

        m1 = ChannelFilter(0, self.l_th1, self.h_th1).apply(image)
        m2 = ChannelFilter(1, self.l_th2, self.h_th2).apply(image)
        m3 = ChannelFilter(2, self.l_th3, self.h_th3).apply(image)
        return np.stack([m1, m2, m3], axis=2)

class GaussianBlur(ParamsFilter):

    def __init__(self, ksize : int = 5) -> None:

        self.ksize  : int = ksize

    def apply(self, image : np.array) -> np.array:

        return np.uint8(cv2.GaussianBlur(image, (self.ksize, self.ksize)))

class MeanBlur(ParamsFilter):

    def __init__(self, ksize : int = 5) -> None:

        self.ksize  : int = ksize

    def apply(self, image : np.array) -> np.array:
            
        return np.uint8(cv2.blur(image, (self.ksize, self.ksize)))

class MedianBlur(ParamsFilter):

    def __init__(self, ksize : int = 5) -> None:

        self.ksize  : int = ksize

    def apply(self, image : np.array) -> np.array:
            
        return np.uint8(cv2.medianBlur(image, self.ksize))
    
class SobelX(ParamsFilter):

    def __init__(self, ksize : int = 5) -> None:

        self.ksize  : int = ksize

    def apply(self, image : np.array) -> np.array:
            
        return np.uint8(cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=self.ksize))
    
class SobelY(ParamsFilter):

    def __init__(self, ksize : int = 5) -> None:

        self.ksize  : int = ksize

    def apply(self, image : np.array) -> np.array:
            
        return np.uint8(cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=self.ksize))
    
class Laplacian(ParamsFilter):

    def __init__(self, ksize : int = 5) -> None:

        self.ksize  : int = ksize

    def apply(self, image : np.array) -> np.array:
            
        return np.uint8(cv2.Laplacian(image, cv2.CV_64F, ksize=self.ksize))
    
class Canny(ParamsFilter):

    def __init__(self, threshold1 : int = 100, threshold2 : int = 200, apertureSize : int = 3) -> None:

        self.threshold1    : int = threshold1
        self.threshold2    : int = threshold2
        self.apertureSize  : int = apertureSize

    def apply(self, image : np.array) -> np.array:
            
        return np.uint8(cv2.Canny(image, self.threshold1, self.threshold2, apertureSize=self.apertureSize))
    
class Elsed(ParamsFilter):

    def __init__(self, minLineLen = 20, sigma = 3, pxToSegmentDistTh = 5, minArea = 150, closing_kernel = 27) -> None:
        
        self.minLineLen : int = minLineLen
        self.sigma : float = sigma
        self.pxToSegmentDistTh : float = pxToSegmentDistTh
        self.minArea : float = minArea
        self.closing_kernel : int = closing_kernel

    def apply(self, image : np.array) -> np.array:

        i_c = image.copy()

        i_c = cv2.cvtColor(i_c, cv2.COLOR_BGR2GRAY)
        
        segments, scores = elsed.detect(i_c, minLineLen = self.minLineLen, sigma = self.sigma, pxToSegmentDistTh = self.pxToSegmentDistTh)
        
        contour_imgs = np.zeros_like(i_c, dtype = np.uint8)
        for s in segments.astype(np.int32):
            cv2.line(contour_imgs, (s[0], s[1]), (s[2], s[3]), 255, 1, cv2.LINE_AA)

        contour_imgs = cv2.morphologyEx(contour_imgs, cv2.MORPH_CLOSE, np.ones((self.closing_kernel, self.closing_kernel), np.uint8))

        contours = cv2.findContours(contour_imgs, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        contours = list(filter(lambda x : cv2.contourArea(x) > self.minArea, contours))

        mean_area = np.mean([cv2.contourArea(c) for c in contours])
        std_area  = np.std([cv2.contourArea(c) for c in contours])

        contours = list(filter(lambda x : cv2.contourArea(x) > mean_area - std_area and cv2.contourArea(x) < mean_area + std_area, contours))

        contour_imgs = np.zeros_like(image, dtype=np.uint8)
        for c in contours:
            contour_imgs = cv2.drawContours(contour_imgs, [c], -1, (0,0,255), thickness=cv2.FILLED)

        blended = cv2.addWeighted(image, .5, contour_imgs, 0.5, 0)

        return blended
        