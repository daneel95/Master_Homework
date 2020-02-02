import cv2
import numpy as np
from skimage.feature import hog
from sklearn.svm import LinearSVC
import pickle

SELECTION_MODEL_PATH = "trained_model/choice_classifier.pkl"
MNIST_DATA_PATH = "mnist/mnist_train.csv"


def split_image_and_save(image):
    height, width = image.shape[:2]

    start_row, start_col = int(0), int(0)
    end_row, end_col = int(height * .35), int(width * .5)
    cropped_top = image[start_row:end_row, start_col:end_col]
    # cv2.imwrite("TopSide.jpg", cropped_top)

    start_row, start_col = int(height * .52), int(width * 0.1)
    end_row, end_col = int(height * 0.87), int(width)
    end_col_left = int(width * .37)
    start_col_right = int(width * .63)
    end_col = int(width * 0.9)
    choice_start_row = int(height * 0.45)
    choice_end_row = start_row

    cropped_bot_left = image[start_row:end_row, start_col:end_col_left]
    cropped_bot_right = image[start_row:end_row, start_col_right:end_col]
    cropped_bot_right_choice = image[choice_start_row:choice_end_row, start_col_right:end_col]

    cv2.imwrite("BotSideLeft.jpg", cropped_bot_left)
    cv2.imwrite("BotSideRight.jpg", cropped_bot_right)
    cv2.imwrite("BotSideRightChoice.jpg", cropped_bot_right_choice)


def split_image(image):
    height, width = image.shape[:2]

    start_row, start_col = 0, 0
    middle_row = int(height * 0.5)
    row_for_right_side = int(height * 0.4)
    middle_column = int(width * 0.5)
    cropped_bot_left = image[middle_row:height, start_col:middle_column]
    cropped_bot_right = image[row_for_right_side:height, middle_column:width]
    cropped_top_left = image[start_row:middle_row, start_col:middle_column]

    return cropped_bot_left, cropped_bot_right, cropped_top_left


def split_image_less_custom(image):
    height, width = image.shape[:2]

    start_row, start_col = 0, 0
    middle_row = int(height * 0.5)
    row_for_right_side = int(height * 0.4)
    middle_collumn = int(width * 0.5)
    cropped_bot_left = image[middle_row:height, start_col:middle_collumn]
    cropped_bot_right = image[row_for_right_side:height, middle_collumn:width]
    cropped_top_left = image[start_row:middle_row, start_col:middle_collumn]

    cv2.imwrite("BotSideLeft.jpg", cropped_bot_left)
    cv2.imwrite("BotSideRight.jpg", cropped_bot_right)
    cv2.imwrite("TopSideLeft.jpg", cropped_top_left)


def remove_duplicates(lines):
    # remove duplicate lines (lines within 10 pixels of eachother)
    for line in lines:
        line = line[0]
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        for index, line in enumerate(lines):
            line = line[0]
            x3 = line[0]
            y3 = line[1]
            x4 = line[2]
            y4 = line[3]
            if y1 == y2 and y3 == y4:
                diff = abs(y1 - y3)
            elif x1 == x2 and x3 == x4:
                diff = abs(x1 - x3)
            else:
                diff = 0
            if diff < 10 and diff is not 0:
                del lines[index]
    return lines


def sort_line_list(lines):
    # sort lines into horizontal and vertical
    vertical = []
    horizontal = []
    for line in lines:
        line = line[0]
        if line[0] == line[2]:
            vertical.append(line)
        elif line[1] == line[3]:
            horizontal.append(line)
    vertical.sort()
    horizontal.sort(key=lambda x: x[1])
    return horizontal, vertical


def get_results_from_table(horizontal, vertical, thresh_image):
    rows = []
    for i, h in enumerate(horizontal):
        if i < len(horizontal) - 1:
            row = []
            for j, v in enumerate(vertical):
                if i < len(horizontal) - 1 and j < len(vertical) - 1:
                    # every cell before last cell
                    # get width & height
                    width = horizontal[i + 1][1] - h[1]
                    height = vertical[j + 1][0] - v[0]
                else:
                    # last cell, width = cell start to end of image
                    # get width & height
                    width = tW
                    height = tH
                tW = width
                tH = height
                # get roi (region of interest)
                roi = thresh_image[h[1]:h[1] + width, v[0]:v[0] + height]
                roi = roi[10:roi.shape[0] - 10, 10:roi.shape[1] - 10]
                # roi = cv2.erode(roi, (3, 3), iterations=2)
                row.append(roi)
            row.pop()
            rows.append(row)

    # results = dict()
    # for i, row in enumerate(rows):
    #     cell_a = row[0]
    #     cell_b = row[1]
    #     cell_c = row[2]
    #     cell_d = row[3]
    #
    #     cell_a_black = np.sum(cell_a == 0)
    #     cell_b_black = np.sum(cell_b == 0)
    #     cell_c_black = np.sum(cell_c == 0)
    #     cell_d_black = np.sum(cell_d == 0)
    #
    #     max_black_pixels = max(cell_a_black, max(cell_b_black, max(cell_c_black, cell_d_black)))
    #
    #     if max_black_pixels == cell_a_black:
    #         results[i + 1] = "A"
    #     if max_black_pixels == cell_b_black:
    #         results[i + 1] = "B"
    #     if max_black_pixels == cell_c_black:
    #         results[i + 1] = "C"
    #     if max_black_pixels == cell_d_black:
    #         results[i + 1] = "D"

    results = []
    for i, row in enumerate(rows):
        cell_a = row[0]
        cell_b = row[1]
        cell_c = row[2]
        cell_d = row[3]

        # print("I = " + str(i + 1))
        # cv2.imshow("cell", cell_a)
        # cv2.waitKey(0)
        # cv2.imshow("cell", cell_b)
        # cv2.waitKey(0)
        # cv2.imshow("cell", cell_c)
        # cv2.waitKey(0)
        # cv2.imshow("cell", cell_d)
        # cv2.waitKey(0)

        cell_a_black = np.sum(cell_a == 0)
        cell_b_black = np.sum(cell_b == 0)
        cell_c_black = np.sum(cell_c == 0)
        cell_d_black = np.sum(cell_d == 0)

        max_black_pixels = max(cell_a_black, max(cell_b_black, max(cell_c_black, cell_d_black)))

        if max_black_pixels == cell_a_black:
            results.append("A")
        if max_black_pixels == cell_b_black:
            results.append("B")
        if max_black_pixels == cell_c_black:
            results.append("C")
        if max_black_pixels == cell_d_black:
            results.append("D")

    return results
    # for key, value in results.items():
    #     print("Result for question " + str(key) + " is " + value)


# returns 0 for Informatica and 1 for Fizica
def get_results_from_selection(horizontal, vertical, thresh_image):
    # Can be hardcoded as less line will give bad results (should not even work) and more lines is not a good answer.
    # Expectation is only for those lines
    horizontal_1 = horizontal[0]
    horizontal_2 = horizontal[1]
    horizontal_3 = horizontal[2]
    horizontal_4 = horizontal[3]
    vertical_1 = vertical[0]
    vertical_2 = vertical[1]

    width_1 = horizontal_2[1] - horizontal_1[1]
    height = vertical_2[0] - vertical_1[0]
    width_2 = horizontal_4[1] - horizontal_3[1]

    roi1 = thresh_image[horizontal_1[1]:horizontal_1[1] + width_1, vertical_1[0]:vertical_1[0] + height]
    roi2 = thresh_image[horizontal_3[1]:horizontal_3[1] + width_2, vertical_1[0]:vertical_1[0] + height]

    if np.sum(roi1 == 0) > np.sum(roi2 == 0):
        return 0
        # print("Informatica")
    else:
        return 1
        # print("Fizica")


def remove_reduntant_horizontal_lines(horizontal, threshold):
    # remove redundant horizontal lines
    to_remove = []

    for i in range(1, len(horizontal)):
        y1 = horizontal[i - 1][1]
        y2 = horizontal[i][1]
        if abs(y2 - y1) < threshold:
            to_remove.append(i - 1)

    new_horizontals = []
    for i, el in enumerate(horizontal):
        if i not in to_remove:
            new_horizontals.append(el)

    return new_horizontals


def remove_redundant_vertical_lines(vertical, threshold):
    # remove redundant vertical lines
    to_remove = []

    for i in range(1, len(vertical)):
        x1 = vertical[i - 1][0]
        x2 = vertical[i][0]

        if abs(x2 - x1) < threshold:
            to_remove.append(i - 1)

    new_verticals = []
    for i, el in enumerate(vertical):
        if i not in to_remove:
            new_verticals.append(el)

    return new_verticals


def normalize_lines(horizontal, vertical):
    # stretch horizontals
    for i, line in enumerate(horizontal):
        x1 = vertical[0][0]
        y1 = line[1]
        x2 = vertical[-1][0]
        y2 = line[3]

        horizontal[i] = [x1, y1, x2, y2]

    # stretch verticals
    for i, line in enumerate(vertical):
        x1 = line[0]
        y1 = horizontal[0][1]
        x2 = line[2]
        y2 = horizontal[-1][1]

        vertical[i] = [x1, y1, x2, y2]

    return horizontal, vertical


def handle_left_table(img):
    # gray scale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply adaptive threshold
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 55, 8)
    thresh_for_results = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    # apply Canny algorithm to get the edges
    edges = cv2.Canny(thresh, 10, 50, apertureSize=7)
    # Use HoughtLines to get the lines from the Canny result
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 200, minLineLength=20, maxLineGap=999).tolist()
    # Remove duplicate lines
    lines = remove_duplicates(lines)
    # break lines into horizontal and vertical lines
    horizontal, vertical = sort_line_list(lines)

    horizontal = remove_reduntant_horizontal_lines(horizontal, 75)
    # get rid of last horizontal line
    horizontal = horizontal[:-1]
    # take only the 16 needed lines (starting to count from last to the 1st line)
    horizontal = horizontal[len(horizontal) - 16:]

    vertical = remove_redundant_vertical_lines(vertical, 75)
    # get rid of the first vertical lines so that we get only the last 5 lines (needed for the table). We don't need that part of the table
    vertical = vertical[len(vertical) - 5:]

    horizontal, vertical = normalize_lines(horizontal, vertical)

    # TESTING STUFF

    # for line in horizontal:
    #     x1 = line[0]
    #     y1 = line[1]
    #     x2 = line[2]
    #     y2 = line[3]
    #     # print("(" + str(x1) + "," + str(y1) + ") -- (" + str(x2) + "," + str(y2) + ")")
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    #
    # # show verticals
    # for line in vertical:
    #     x1 = line[0]
    #     y1 = line[1]
    #     x2 = line[2]
    #     y2 = line[3]
    #     # print("(" + str(x1) + "," + str(y1) + ") -- (" + str(x2) + "," + str(y2) + ")")
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    #
    # cv2.imwrite("left_table.jpg", img)
    # # cv2.imshow("aa", img)
    # # cv2.waitKey(0)

    # END OF TESTING STUFF

    results = get_results_from_table(horizontal, vertical, thresh_for_results)

    return results

    # for key, value in results.items():
    #     print("Result for question " + str(key) + " is " + value)


def handle_right_table_and_choice(img):
    # gray scale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply adaptive threshold
    # thresh_for_results = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 55, 8)
    thresh_for_results = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    # apply Canny algorithm to get the edges
    edges = cv2.Canny(thresh, 10, 50, apertureSize=7)
    # Use HoughtLines to get the lines from the Canny result
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 200, minLineLength=20, maxLineGap=999).tolist()
    # Remove duplicate lines
    lines = remove_duplicates(lines)
    # break lines into horizontal and vertical lines
    horizontal, vertical = sort_line_list(lines)

    horizontal = remove_reduntant_horizontal_lines(horizontal, 75)
    # get rid of last horizontal line
    horizontal = horizontal[:-1]
    # take only the 16 needed lines (starting to count from last to the 1st line)
    horizontal = horizontal[len(horizontal) - 16:]

    vertical = remove_redundant_vertical_lines(vertical, 75)
    # get rid of the first vertical lines so that we get only the last 5 lines (needed for the table). We don't need that part of the table
    vertical = vertical[len(vertical) - 5:]

    horizontal, vertical = normalize_lines(horizontal, vertical)

    # TESTING STUFF

    # for line in horizontal:
    #     x1 = line[0]
    #     y1 = line[1]
    #     x2 = line[2]
    #     y2 = line[3]
    #     # print("(" + str(x1) + "," + str(y1) + ") -- (" + str(x2) + "," + str(y2) + ")")
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    #
    # # show verticals
    # for line in vertical:
    #     x1 = line[0]
    #     y1 = line[1]
    #     x2 = line[2]
    #     y2 = line[3]
    #     # print("(" + str(x1) + "," + str(y1) + ") -- (" + str(x2) + "," + str(y2) + ")")
    #
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    #
    # cv2.imwrite("right_table.jpg", img)
    # # cv2.imshow("aa", img)
    # # cv2.waitKey(0)

    # END OF TESTING STUFF

    results = get_results_from_table(horizontal, vertical, thresh_for_results)

    # for key, value in results.items():
    #     print("Result for question " + str(key) + " is " + value)

    # create selection region
    # The selection region will be the region starting from TOP to the first horizontal from where we move upwards
    # with a threshold (this time 250).
    # The vertical lines will be the last 2 (the column for D) which we strtch a bit to be sure to get
    # the 2 selection boxes
    region_y = horizontal[0][1] - 250
    region_x1 = vertical[-2][0] - 50
    region_x2 = vertical[-1][2] + 50
    selection_region_color = img[0:region_y, region_x1:region_x2]
    selection_result, choice_result = get_selection(selection_region_color)

    print("Candidate chose {} with subject {}".format(selection_result, choice_result))

    return results, "barem/{}_varianta{}.txt".format(selection_result, choice_result)


# returns 0 for Informatioca and 1 for Fizica
def get_selection(selection_region_color):
    # gray scale image
    gray = cv2.cvtColor(selection_region_color, cv2.COLOR_BGR2GRAY)
    # apply threshold
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

    edges = cv2.Canny(gray, 30, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    rect_bottom = cv2.boundingRect(contours[0])
    x, y, w, h = rect_bottom
    bottom_box = thresh[y: y + h, x: x + w]
    bottom_box_color = selection_region_color[y: y + h, x: x + w]

    rect_top = cv2.boundingRect(contours[1])
    x, y, w, h = rect_top
    top_box = thresh[y: y + h, x: x + w]
    top_box_color = selection_region_color[y: y + h, x: x + w]

    if np.sum(top_box == 0) > np.sum(bottom_box == 0):
        no_border_image = apply_mask_on_border(top_box_color)
        no_border_image = apply_black_on_margin(no_border_image)
        choice = predict_choice(no_border_image)

        # global_warming.append("I")
        # cv2.imwrite("only_so_called_digits/digit_" + str(len(global_warming)) + ".jpg", ~no_border)
        # cv2.imwrite("only_so_called_digits/digit_original_" + str(len(global_warming)) + ".jpg",  top_box_color)
        return "Informatica", choice
        # print("Informatica")
    else:
        no_border_image = apply_mask_on_border(bottom_box_color)
        no_border_image = apply_black_on_margin(no_border_image)
        choice = predict_choice(no_border_image)

        # global_warming.append("F")
        # cv2.imwrite("only_so_called_digits/digit_" + str(len(global_warming)) + ".jpg", ~no_border)
        # cv2.imwrite("only_so_called_digits/digit_original_" + str(len(global_warming)) + ".jpg", bottom_box_color)
        return "Fizica", choice
        # print("Fizica")


def apply_mask_on_border(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
    inv = 255 - thresh
    horizontal_img = inv.copy()
    vertical_img = inv.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 10))
    horizontal_img = cv2.erode(horizontal_img, kernel, iterations=1)
    horizontal_img = cv2.dilate(horizontal_img, kernel, iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 100))
    vertical_img = cv2.erode(vertical_img, kernel, iterations=1)
    vertical_img = cv2.dilate(vertical_img, kernel, iterations=3)
    mask_img = horizontal_img + vertical_img
    no_border = np.bitwise_or(thresh, mask_img)

    return no_border


def apply_black_on_margin(image, threshold=20):
    w, h = image.shape

    image[0:threshold, 0:h] = 255
    image[w - threshold:w, 0:h] = 255
    image[0:h, 0:threshold] = 255
    image[0:h, h - threshold:h] = 255

    return image


def train_and_save_model():
    print("Handling mnist data!")
    f = open(MNIST_DATA_PATH, "r")
    f.readline()
    size = 28
    labels = []
    features = []

    for line in f.readlines():
        img_mnist = []
        line = line[:-1]
        line = line.split(",")
        if line[0] not in ["1", "2", "3", "4"]:
            # want to pick only the needed digits - 1, 2, 3, 4
            continue
        labels.append(int(line[0]) - 1)
        line = line[1:]

        for i in range(size):
            ln = []
            for j in range(size):
                ln.append(int(line[i * size + j]))
            img_mnist.append(ln)

        img_mnist = np.array(img_mnist, dtype=np.float32)
        img_mnist = cv2.cvtColor(img_mnist, cv2.COLOR_GRAY2BGR)
        img_mnist = cv2.cvtColor(img_mnist, cv2.COLOR_BGR2GRAY)
        hog_value = hog(img_mnist, orientations=11, pixels_per_cell=(3, 3), cells_per_block=(1, 1))
        features.append(hog_value)
    f.close()
    print("Mnist data handling completed!")

    features = np.array(features, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)
    classifier = LinearSVC()
    print("Start training!")
    classifier.fit(features, labels)
    print("Training completed!")
    pickle.dump(classifier, open(SELECTION_MODEL_PATH, 'wb'))


def predict_choice(image):
    classifier = pickle.load(open(SELECTION_MODEL_PATH, 'rb'))
    digit = cv2.resize(image, (28, 28))
    hog_value = hog(digit, orientations=11, pixels_per_cell=(3, 3), cells_per_block=(1, 1))
    return int(classifier.predict([hog_value])[0] + 1)


def calculate_mark(path_to_image):
    image = cv2.imread(path_to_image)
    cropped_bot_left, cropped_bot_right, cropped_top_left = split_image(image)
    left_table_results = handle_left_table(cropped_bot_left)
    right_table_results, barem_file = handle_right_table_and_choice(cropped_bot_right)
    final_results = left_table_results + right_table_results

    # read barem
    correct_answers = 0
    f = open(barem_file, "r")
    f.readline()  # read the first line, don't need it
    for j in range(30):
        correct_answer = f.readline()[:-1].split(" ")[1]
        if correct_answer == final_results[j]:
            correct_answers += 1
    f.close()

    mark = correct_answers * 0.3 + 1

    return mark


# just testing purposes
def test_on_example_tests_rotated():
    # for i in range(105, 106):
    for i in range(1, 2):
        print("Handling image " + str(i))
        if i == 92:  # skip 92, X instead of a number in selection
            continue
        file_path = "C:\\Users\\Daniel\\Desktop\\PrelucrareaSemnalelorsiAplicatii\\tema1\\exemple_corecte\\rotation_" + str(
            i) + ".jpg"
        image = cv2.imread(file_path)

        # TEST START

        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 175, 2)
        # edges = cv2.Canny(img, 200, 250)
        # contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #
        # cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
        cv2.imwrite("rotated_image_handled.jpg", image)

        cv2.imwrite("test.jpg", img)

        #
        # def resize(img, height=800):
        #     """ Resize image to given height """
        #
        #     rat = height / img.shape[0]
        #     return cv2.resize(img, (int(rat * img.shape[1]), height))
        #
        # img = cv2.cvtColor(resize(img), cv2.COLOR_BGR2GRAY)
        # img = cv2.bilateralFilter(img, 9, 75, 75)
        # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 75, -2)
        # # img = cv2.medianBlur(img, 11)
        # img = cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        # edges = cv2.Canny(img, 200, 250)
        # contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #
        # cv2.imwrite("test.jpg", edges)
        #
        # cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
        # cv2.imwrite("rotated_image_handled.jpg", image)

        # TEST END

        # cropped_bot_left, cropped_bot_right, cropped_top_left = split_image(image)
        # left_table_results = handle_left_table(cropped_bot_left)
        # right_table_results, barem = handle_right_table_and_choice(cropped_bot_right)
        # final_results = left_table_results + right_table_results
        # barem = barem.split("/")[1]
        # barem = barem.split("_")
        # test_choice = "F" if barem[0] == "Fizica" else "I"
        # barem = barem[1].split(".")[0]
        # test_number = int(barem[-1])
        # f = open("C:\\Users\\Daniel\\Desktop\\PrelucrareaSemnalelorsiAplicatii\\tema1\\exemple_corecte\\image_" + str(
        #     i) + ".txt", "r")
        # test_type = f.readline()[:-1].split(" ")
        # if test_type[0] != test_choice:
        #     print("Nu am ales bine materia!")
        #
        # if int(test_type[1]) != test_number:
        #     print("Nu am ales bine numarul variantei!")
        #
        # for j in range(30):
        #     answer = f.readline()[:-1].split(" ")[1]
        #     if answer != final_results[j]:
        #         if j < 15:
        #             print("Nu am ales bine X-ul in TABEL STANGA. Pe linia {} am gasit {} si expected {}".format(j + 1, final_results[j], answer))
        #         else:
        #             print("Nu am ales bine X-ul in TABEL DREAPTA. Pe linia {} am gasit {} si expected {}".format(j - 15 + 1, final_results[j], answer))
        # f.close()
        # print("=============================================")


# just testing purposes
def test_on_example_tests():
    # for i in range(105, 106):
    for i in range(1, 151):
        print("Handling image " + str(i))
        if i == 92:  # skip 92, X instead of a number in selection
            continue
        file_path = "C:\\Users\\Daniel\\Desktop\\PrelucrareaSemnalelorsiAplicatii\\tema1\\exemple_corecte\\image_" + str(
            i) + ".jpg"
        image = cv2.imread(file_path)
        cropped_bot_left, cropped_bot_right, cropped_top_left = split_image(image)
        left_table_results = handle_left_table(cropped_bot_left)
        right_table_results, barem = handle_right_table_and_choice(cropped_bot_right)
        final_results = left_table_results + right_table_results
        barem = barem.split("/")[1]
        barem = barem.split("_")
        test_choice = "F" if barem[0] == "Fizica" else "I"
        barem = barem[1].split(".")[0]
        test_number = int(barem[-1])
        f = open("C:\\Users\\Daniel\\Desktop\\PrelucrareaSemnalelorsiAplicatii\\tema1\\exemple_corecte\\image_" + str(
            i) + ".txt", "r")
        test_type = f.readline()[:-1].split(" ")
        if test_type[0] != test_choice:
            print("Nu am ales bine materia!")

        if int(test_type[1]) != test_number:
            print("Nu am ales bine numarul variantei!")

        for j in range(30):
            answer = f.readline()[:-1].split(" ")[1]
            if answer != final_results[j]:
                if j < 15:
                    print("Nu am ales bine X-ul in TABEL STANGA. Pe linia {} am gasit {} si expected {}".format(j + 1,
                                                                                                                final_results[
                                                                                                                    j],
                                                                                                                answer))
                else:
                    print("Nu am ales bine X-ul in TABEL DREAPTA. Pe linia {} am gasit {} si expected {}".format(
                        j - 15 + 1, final_results[j], answer))
        f.close()
        print("=============================================")


if __name__ == "__main__":
    # provide a path to the test
    file_path = input("Introduceti un path catre testul grila: \n")
    # calculate the mark of the test
    mark = calculate_mark(file_path)
    print("Nota finala este {}".format(mark))
