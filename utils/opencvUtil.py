

import cv2

class OpenCVUtil:

    def match(image, template, method = cv2.TM_CCOEFF_NORMED):
        result = cv2.matchTemplate(image, template, method)
        #cv2.imshow('', result)
        #cv2.waitKey(0)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return {'min_val':min_val, 'max_val':max_val, 'min_loc':min_loc, 'max_loc':max_loc}

    def isMatch(result):
        return result['max_val'] > 0.9

    def calculated(result, shape):
        mat_top, mat_left = result['max_loc']
        prepared_height, prepared_width, prepared_channels = shape

        x = {
            'left': int(mat_top),
            'center': int((mat_top + mat_top + prepared_width) / 2),
            'right': int(mat_top + prepared_width),
        }

        y = {
            'top': int(mat_left),
            'center': int((mat_left + mat_left + prepared_height) / 2),
            'bottom': int(mat_left + prepared_height),
        }

        return {
            'x': x,
            'y': y,
        }
