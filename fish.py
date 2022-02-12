import pyautogui, cv2, os
from time import sleep

FILE_DIRECTORY = 'C:\\Users\\ryanh\\Downloads'
FILE_NAME = '4_by_3.mp4'

FILE_PATH = FILE_DIRECTORY + '\\' + FILE_NAME
FILE_NAME_PREFIX = FILE_NAME.split('.')[0]
DATA_FILE_NAME = FILE_NAME_PREFIX + '_data' + '.csv'
WINDOW_NAME = 'fish'
MAX_COORDINATES = pyautogui.size()

UNDERSAMPLING_FACTOR = 4
FPS = 48
REWIND_FRAME_COUNT = 120


def main():
    if not os.path.isfile(FILE_PATH):
        print('ERROR: file not found ' + FILE_PATH)
        return

    data_file = open(DATA_FILE_NAME, 'w+')

    if os.path.getsize(DATA_FILE_NAME) > 0:
        print('WARN: data file for ' + FILE_NAME + ' is already written to, will be overwritten')

    vid = cv2.VideoCapture(FILE_PATH)
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    coordinates = []
    frames = get_frames(vid)

    i = 0
    while i < len(frames):
        sleep(1/FPS)
        cv2.imshow(WINDOW_NAME, frames[i])
        wait_key = cv2.waitKey(1)

        if wait_key & 0xFF == ord('q'):  # press q to quit
            break

        if wait_key == ord('p') or i == 0: # press p to pause
            cv2.waitKey(-1)

        if wait_key == ord('b'): # press b to rewind vid and data
            i = max(0, i - REWIND_FRAME_COUNT)
            vid.set(cv2.CAP_PROP_POS_FRAMES, i)
            coordinates = coordinates[:i]
            cv2.imshow(WINDOW_NAME, frames[i])

        x = pyautogui.position().x / MAX_COORDINATES.width
        y = pyautogui.position().y / MAX_COORDINATES.height
        coordinates.append({'x': x, 'y': y})

        i = i+1

    write_data(data_file, coordinates, UNDERSAMPLING_FACTOR)


def write_data(data_file, data_array, undersampling_factor):
    for i, data_point in enumerate(data_array):
        if i % undersampling_factor == 0:
            data_file.write(str(data_point.get('x')) + ', ' + str(data_point.get('y')) + '\n')

    data_file.close


def get_frames(video):
    frames = []

    while True:
        frame_success, frame = video.read()
        if frame_success:
            frames.append(frame)
        else:
            break

    return frames


if __name__ == '__main__':
    main()
