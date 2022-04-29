import numpy as np
import cv2
import os


def extractVideoFrames(VIDEO_PATH, OUTPUT_PATH=None, OUTPUT_COUNT=10):
    vidcap = cv2.VideoCapture(VIDEO_PATH)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(vidcap.get(cv2.CAP_PROP_FPS))
    total_time_ms = (frame_count//frame_rate) * 1000
    frames = [round(i) for i in np.linspace(0, total_time_ms, OUTPUT_COUNT)]

    for i in frames:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, i)
        success, image = vidcap.read()
        if success:
            if OUTPUT_PATH is None:
                cv2.imwrite("frame%d.jpg" % i, image)
            else:
                cv2.imwrite(os.path.join(
                    OUTPUT_PATH, "frame%d.jpg" % i), image)


def Stitcher(IMAGES_DIR):
    IMAGES_PATH = os.listdir(IMAGES_DIR)
    IMAGES = []

    for path in IMAGES_PATH:
        image_path = os.path.join(IMAGES_DIR, path)
        if os.path.isfile(image_path) and not image_path.endswith('Output.jpg'):
            image = cv2.imread(image_path)
            IMAGES.append(image)

    stitcher = cv2.Stitcher.create()
    (status, stitched) = stitcher.stitch(IMAGES)
    if (status == cv2.STITCHER_OK):
        return stitched
    else:
        return None


# IMAGES_DIR = <image_path>
# stitched = Stitcher(IMAGES_DIR)
# if (stitched is not None):
#     cv2.imwrite(os.path.join(IMAGES_DIR, 'stitchedOutput.jpg'), stitched)
#     stitched = cv2.resize(stitched, (0, 0), None, 0.2, 0.2)
#     cv2.imshow('Stitched Image', stitched)
#     cv2.waitKey()
#     cv2.destroyAllWindows()


VIDEO_PATH = <video_path>
OUTPUT_PATH = <output_path>
print('Extracting frames from video...')
extractVideoFrames(VIDEO_PATH, OUTPUT_PATH, 30)

print('Stitching frames...')
stitched = Stitcher(OUTPUT_PATH)
if (stitched is not None):
    cv2.imwrite(os.path.join(OUTPUT_PATH, 'stitchedOutput.jpg'), stitched)
