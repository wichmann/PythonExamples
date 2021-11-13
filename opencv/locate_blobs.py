#
# Locate blobs in an overhead shoot of a room
# 
# Requirements:
#  * opencv
#     - Ubuntu Linux: sudo apt install python3-opencv
#  * 
#  

import sys
import math

import cv2 as cv
import numpy as np


default_font = cv.FONT_HERSHEY_PLAIN


def detect_blobs(img):
    params = cv.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 215.0
    params.maxArea = 400.0
    params.filterByInertia = False
    params.filterByConvexity = False
    params.filterByColor = False
    #params.blobColor = 128
    params.filterByCircularity = False
    #params.minCircularity = 0.8
    detector = cv.SimpleBlobDetector_create(params)
    keypoints = detector.detect(img)
    return keypoints


def ident_keypoints(keypoints, img):
    axis_keypoints = []
    blob_keypoints = []
    for k in keypoints:
        x = int(k.pt[0])
        y = int(k.pt[1])
        b, g, r = img[y, x] # color = (b,g,r)
        print(f'Blob an Punkt {k.pt} mit Farbe ({r},{g},{b})')
        # filter blobs by their color (red is origin and axis, blue are roboter)
        color_threshold = 120
        if r > color_threshold and g < color_threshold and b < color_threshold:
            print('    -> ist Teil der Achse')
            cv.rectangle(img, (x-3, y-3), (x+3, y+3), (0, 0, 255), 3)
            axis_keypoints.append((x, y))
        elif r < color_threshold and g < color_threshold and b > color_threshold:
            print('    -> ist gesuchter Blob')
            cv.rectangle(img, (x-3, y-3), (x+3, y+3), (255, 0, 0), 3)
            blob_keypoints.append((x, y))
    return axis_keypoints, blob_keypoints


def find_axis(axis_keypoints):
    epsilon = 7.5
    if len(axis_keypoints) == 3:
        if abs(abs(calc_angle_between_lines((axis_keypoints[0], axis_keypoints[1]), (axis_keypoints[1], axis_keypoints[2]))) - 90) < epsilon:
            return axis_keypoints[1]
        if abs(abs(calc_angle_between_lines((axis_keypoints[0], axis_keypoints[1]), (axis_keypoints[0], axis_keypoints[2]))) - 90) < epsilon:
            return axis_keypoints[0]
        if abs(abs(calc_angle_between_lines((axis_keypoints[0], axis_keypoints[2]), (axis_keypoints[1], axis_keypoints[2]))) - 90) < epsilon:
            return axis_keypoints[2]
    else: 
        print('Anzahl der Achspunkte passt nicht!')
    return None


def calc_angle(line):
    return math.atan2(line[0][1] - line[1][1], line[0][0] - line[1][0])


def calc_angle_between_lines(lineA, lineB):
    """
    Calculates the angle between two lines.

    Source: https://stackoverflow.com/q/28260962
    """
    angle1 = calc_angle(lineA)
    angle2 = calc_angle(lineB)
    angle_degrees = (angle1 - angle2) * 360 / (2 * math.pi)
    print(f'Berechneter Winkel: {angle_degrees}')
    return angle_degrees


def calc_length(pointA, pointB):
    return math.sqrt( pow( abs(pointA[0] - pointB[0]), 2) + pow( abs(pointA[1] - pointB[1]), 2) )


def process_image(image_file):
    img = cv.imread(image_file)
    if img is None:
        sys.exit("Could not read the image.")
    cv.imshow('Geladenes Bild', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    ### find all blobs in image and sort them by color
    keypoints = detect_blobs(img)
    axis_keypoints, blob_keypoints = ident_keypoints(keypoints, img)
    img_with_keypoints = cv.drawKeypoints(img, keypoints, outImage=np.array([]), color=(0, 0, 255), flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imshow('Bild mit gefundenen Punkte', img_with_keypoints)
    cv.waitKey(0)
    cv.destroyAllWindows()

    ### find the origin and axis for scaling between image coordinates and real world coordinates
    axis_center = find_axis(axis_keypoints)
    if axis_center == None:
        print('Ursprung und Koordinatensystem konnten nicht ermittelt werden.')
        return
    # TODO: Process which point is x and which point is y
    axis_keypoints.remove(axis_center)
    # find orientation of two axis
    angle1 = calc_angle((axis_keypoints[0], axis_center)) + 2 * math.pi
    angle2 = calc_angle((axis_keypoints[1], axis_center)) + 2 * math.pi
    if angle1 < angle2:
        axis_x = axis_keypoints[1]
        axis_y = axis_keypoints[0]
    else:
        axis_x = axis_keypoints[0]
        axis_y = axis_keypoints[1]
    # draw axis and show image
    image_with_origin = img.copy()
    cv.line(image_with_origin, axis_center, axis_x, (255, 255, 255), thickness=3, lineType=cv.LINE_AA)
    cv.line(image_with_origin, axis_center, axis_y, (255, 255, 255), thickness=3, lineType=cv.LINE_AA)
    cv.putText(image_with_origin, 'x-Achse', (axis_y[0]+25, axis_y[1]), fontFace=default_font, fontScale=1.0, thickness=2, color=(0,0,0))
    cv.putText(image_with_origin, 'y-Achse', (axis_x[0], axis_x[1]+25), fontFace=default_font, fontScale=1.0, thickness=2, color=(0,0,0))
    cv.imshow('Bild mit erkanntem Ursprung', image_with_origin)
    cv.waitKey(0)
    cv.destroyAllWindows()

    ### transform image according to the origin and axis
    # source: https://theailearner.com/tag/cv2-warpaffine/
    rows, cols = img.shape[:2]
    input_pts = np.float32([axis_center, axis_x, axis_y])
    output_pts = np.float32([[0,0], [0,200], [200,0]])
    transform_matrix_image = cv.getAffineTransform(input_pts , output_pts)
    img_transformed = cv.warpAffine(img, transform_matrix_image, (cols,rows))
    cv.imshow('Transformiertes Bild gemäß Ursprung-Marker', img_transformed)
    cv.waitKey(0)
    cv.destroyAllWindows()

    ### scale all blobs that are not part of the axis to real world coordinates
    # length between two red markers
    axis_length = 250
    # calculate transformation matrix to scale to real world coordinates
    input_pts = np.float32([axis_center, axis_x, axis_y])
    output_pts = np.float32([[0,0], [0,axis_length], [axis_length,0]])
    transform_matrix_coordinates = cv.getAffineTransform(input_pts , output_pts)
    # scale each blob and show text label
    for k in blob_keypoints:
        k_as_array = np.array([[[k[0], k[1], 1]]])
        point_on_image = cv.transform(k_as_array, transform_matrix_image)
        point_in_real_life = cv.transform(k_as_array, transform_matrix_coordinates)
        blob_label = '({}mm, {}mm)'.format(*point_in_real_life[0][0])
        print(f'Blob befindet sich am Punkt: {blob_label}')
        cv.putText(img_transformed, blob_label, (point_on_image[0][0][0], point_on_image[0][0][1]),
                   fontFace=default_font, fontScale=1.0, thickness=2, color=(0,0,0))
    cv.imshow('Transformiertes Bild mit umgerechneten Koordinaten', img_transformed)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    process_image('image1.jpg')
    process_image('image2.jpg')
    process_image('image3.jpg')
