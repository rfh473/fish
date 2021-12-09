import pyautogui, cv2, os, sys

def main():
    FILE_DIRECTORY = 'C:\\Users\\ryanh\\Downloads'
    FILE_NAME = '4_by_3.mp4'

    FILE_PATH = FILE_DIRECTORY + '\\' + FILE_NAME
    FILE_NAME_PREFIX = FILE_NAME.split('.')[0]
    DATA_FILE_NAME = FILE_NAME_PREFIX + '_data' + '.csv'
    SUMMARY_FILE_NAME = FILE_NAME_PREFIX + '_summary' + '.txt'
    WINDOW_NAME = 'fish'
    UNDERSAMPLING_FACTOR = 4
    MAX_COORDINATES = pyautogui.size()

    if not os.path.isfile(FILE_PATH):
        print('ERROR: file not found ' + FILE_PATH)
        return

    data = open(DATA_FILE_NAME, 'w+')
    summary = open(SUMMARY_FILE_NAME, 'w+')

    if os.path.getsize(DATA_FILE_NAME) > 0 or os.path.getsize(SUMMARY_FILE_NAME):
        print('WARN: data or summary files for ' + FILE_NAME + ' are already written to, will be overwritten')

    vid = cv2.VideoCapture(FILE_PATH)
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    x_coordinates = []
    y_coordinates = []
    frame_index = 0

    while True:
        ret, frame = vid.read()

        if not ret:
            break

        wait_key = cv2.waitKey(1)

        cv2.imshow(WINDOW_NAME, frame)

        if wait_key & 0xFF == ord('q'):  # press q to quit
            break
        if wait_key == ord('p') or frame_index == 0: # press p to pause
            cv2.waitKey(-1)

        if frame_index % UNDERSAMPLING_FACTOR == 0:
            x = pyautogui.position().x / MAX_COORDINATES.width
            y = pyautogui.position().y / MAX_COORDINATES.height
            x_coordinates.append(x)
            y_coordinates.append(y)
            if frame_index != 0:
                data.write('\n')
            data.write(str(x) + ', ' + str(y))

            print('x: ' + str(x), 'y: ' + str(y))

        frame_index += 1

    avg_x_coordinate = sum(x_coordinates) / len(x_coordinates)
    avg_y_coordinate = sum(y_coordinates) / len(y_coordinates)

    print('avg x: ' + str(avg_x_coordinate), 'avg y: ' + str(avg_y_coordinate))

    summary.write(FILE_NAME + '\n')
    summary.write('frames: ' + str(frame_index + 1) + '\n')
    summary.write('undersampling factor: ' + str(UNDERSAMPLING_FACTOR) + '\n')
    summary.write('avg_coordinates: ' + str(avg_x_coordinate) + ', ' + str(avg_y_coordinate))

    data.close()
    summary.close()

if __name__ == '__main__':
    main()
