import click
import pyautogui
import cv2
import os
from time import sleep

WINDOW_NAME = 'fish'
MAX_COORDINATES = pyautogui.size()

UNDERSAMPLING_FACTOR = 4
FPS = 48
REWIND_FRAME_COUNT = 120

@click.command()
@click.argument('file', type=click.File('rb'))
def main(file):
    filename = file.name

    filename_prefix = filename.split('.')[0]
    data_filename = filename_prefix + '_data' + '.csv'

    if not os.path.isfile(filename):
        print(f'ERROR: file not found {filename}')
        return

    data_file = open(data_filename, 'w+')

    if os.path.getsize(data_filename) > 0:
        print(f'WARN: data file for input video is already written to, will be overwritten ({data_filename})')

    vid = cv2.VideoCapture(filename)
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    coordinates = []

    i = 0
    while True:
        frame_success, frame = vid.read()

        if not frame_success:
            break

        sleep(1/FPS)
        cv2.imshow(WINDOW_NAME, frame)
        wait_key = cv2.waitKey(1)

        if wait_key & 0xFF == ord('q'):  # press q to quit
            break

        if wait_key == ord('p') or i == 0: # press p to pause
            cv2.waitKey(-1)

        if wait_key == ord('b'): # press b to rewind vid and data
            i = max(0, i - REWIND_FRAME_COUNT)

            vid.set(cv2.CAP_PROP_POS_FRAMES, i)
            coordinates = coordinates[:i]

            frame_success, frame = vid.read()

            if not frame_success:
                break
            
            cv2.imshow(WINDOW_NAME, frame)
            cv2.waitKey(-1)

        x = pyautogui.position().x / MAX_COORDINATES.width
        y = pyautogui.position().y / MAX_COORDINATES.height
        coordinates.append({'x': x, 'y': y})

        i += 1

    write_data(data_file, coordinates, UNDERSAMPLING_FACTOR)


def write_data(data_file, data_array, undersampling_factor):
    for i, data_point in enumerate(data_array):
        if i % undersampling_factor == 0:
            data_file.write(str(data_point.get('x')) + ', ' + str(data_point.get('y')) + '\n')

    data_file.close()


if __name__ == '__main__':
    main()
