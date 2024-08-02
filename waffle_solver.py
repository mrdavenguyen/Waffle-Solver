import copy
from typing import Tuple

NUM_BOXES = 21

def main():
    # create a data structure to store all letter "boxes":
    boxes = create_box_dict()
    # prompt user to enter the letter and color of each tile in puzzle
    get_user_input(boxes)
    # create a data structure to store the lists of yellow and white letters in each row and column
    rows, columns = create_rows_and_columns(boxes)
    # create list of all white letters in puzzle
    white_letters, og_white_letters = create_white_letter_list(boxes, rows, columns)
    word_list = get_word_list()
    solutions = []
    solve_waffle(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions)
    if len(solutions) == 0:
        print("No solutions found.")
    else:
        no_dupes = []
        for item in solutions:
            if item not in no_dupes:
                no_dupes.append(item)
        if len(no_dupes) > 1:
            print("Multiple solutions found")
        for item in no_dupes:
            print(item)

def create_box_dict() -> dict[int, dict]:
    boxes = {}
    for i in range(NUM_BOXES):
        boxes[i] = {}
        boxes[i]['letter'] = None
        boxes[i]['prev_letter'] = None
        boxes[i]['color'] = None
        boxes[i]['prev_color'] = None
        boxes[i]['row'] = None
        boxes[i]['column'] = None
    return boxes

def get_user_input(boxes: dict[int, dict]) -> None:
    for i in range(NUM_BOXES):
        while True:
            while True:
                letter = input(f"Enter letter (a-z) for tile {i}: ")
                if letter.lower() in 'abcdefghijklmnopqrstuvwxyz' and len(letter) == 1:
                    letter = letter.lower()
                    break
                else:
                    print("Invalid letter, please try again.")
            color = input(f"Enter color (g = 'green', y = 'yellow', w = 'white') for tile {i}: ")
            if color.lower() in 'gyw' and len(color) == 1:
                color = color.lower()
                break
            else:
                print("Invalid color, please try again.")

        boxes[i]['letter'] = letter
        if color == 'g':
            boxes[i]['color'] = 'green'
        elif color == 'y':
            boxes[i]['color'] = 'yellow'
        else:
            boxes[i]['color'] = 'white'

def create_rows_and_columns(boxes: dict[int, dict]) -> Tuple[dict[int, dict], dict[int, dict]]:
    rows = {}
    for i in range(3):
        rows[i] = {}
        rows[i]['yellow'] = {}
        rows[i]['white'] = {}
        rows[i]['boxes'] = {}
        for j in range(5):
            rows[i]['boxes'][j] = boxes[j + i * 8]
            # add row membership to boxes
            rows[i]['boxes'][j]['row'] = i

    columns = {
        0: {
            'boxes': {
                0: boxes[0],
                1: boxes[5],
                2: boxes[8],
                3: boxes[13],
                4: boxes[16]
            },
            'yellow': {},
            'white': {}
        },
        1: {
            'boxes': {
                0: boxes[2],
                1: boxes[6],
                2: boxes[10],
                3: boxes[14],
                4: boxes[18]
            },
            'yellow': {},
            'white': {}
        },
        2: {
            'boxes': {
                0: boxes[4],
                1: boxes[7],
                2: boxes[12],
                3: boxes[15],
                4: boxes[20]
            },
            'yellow': {},
            'white': {}
        }
    }

    for i in range(3):
        for j in range(5):
            # add column membership to boxes
            columns[i]['boxes'][j]['column'] = i

    # create list of white and yellow letters in each line
    for i in range(len(rows)):
        for j in range(len(rows[i]['boxes'])):
            if rows[i]['boxes'][j]['color'] == 'white':
                # array of white letters just store the letter
                rows[i]['white'][j] = rows[i]['boxes'][j]['letter']
            elif rows[i]['boxes'][j]['color'] == 'yellow':
                # array of yellow letters store the box, because position matters
                rows[i]['yellow'][j] = copy.deepcopy(rows[i]['boxes'][j])
            if columns[i]['boxes'][j]['color'] == 'white':
                columns[i]['white'][j] = columns[i]['boxes'][j]['letter']
            elif columns[i]['boxes'][j]['color'] == 'yellow':
                columns[i]['yellow'][j] = copy.deepcopy(columns[i]['boxes'][j])
    return rows, columns

def create_white_letter_list(boxes: dict[int, dict], rows: dict[int, dict], columns: dict[int, dict]) -> list[dict]:
    white_letters = []
    for i in range(len(boxes)):
        if boxes[i]['color'] == 'white':
            white_letters.append(copy.deepcopy(boxes[i]))
    # create an original copy of the white letters in order to check that all letters have been used at the end
    og_white_letters = copy.deepcopy(white_letters)
    # waffle puzzle archive #138 exception: a non-green intersectional letter has matching yellow letters in perpendicular lines (row and column)
    for box in boxes:
        added_letter = False
        if boxes[box]['row'] != None and boxes[box]['column'] != None:
            row = boxes[box]['row']
            column = boxes[box]['column']
            if boxes[box]['color'] != 'green':
                for row_yellow in rows[row]['yellow']:
                    for col_yellow in columns[column]['yellow']:
                        if rows[row]['yellow'][row_yellow]['letter'] == columns[column]['yellow'][col_yellow]['letter']:
                            if rows[row]['yellow'][row_yellow]['letter'] != boxes[box]['letter']:
                                white_letters.append(copy.deepcopy(rows[row]['yellow'][row_yellow])) # does this yellow letter need to change to white?
                                added_letter = True
                                break
                    if added_letter:
                        break
    return white_letters, og_white_letters

def solve_waffle(boxes: dict[int, dict], rows: dict[int, dict], columns: dict[int, dict], white_letters: list[dict], og_white_letters: list[dict], word_list: list[str], solutions: list[list], line_index: int = 0, letter_index: int = 0) -> list[list]:
    # when all tiles have been filled with green letters, evaluate the solution
    if line_index == 6:
        # check if there are remaining yellow letters in any lines. if so the solution isn't valid, and the solution shouldn't be added
        for i in range(len(rows)):
            if rows[i]['yellow'] or columns[i]['yellow']:
                print(rows[i]['yellow'])
                # return without adding solution
                return
        # if all of the letters in the white letter list have been removed, save the solution
        if not og_white_letters:
            solutions.append([])
            for row in rows:
                solutions[-1].append([])
                word = ""
                for box in rows[row]['boxes']:
                    word += rows[row]['boxes'][box]['letter']
                solutions[-1][row] = word
            for column in columns:
                solutions[-1].append([])
                word = ""
                for box in columns[column]['boxes']:
                    word += columns[column]['boxes'][box]['letter']
                solutions[-1][column + 3] = word                
            return
        else:
            return
            
    if line_index < 3:
        line_ornts_1 = rows
        line_ornts_2 = columns
        line_ornt_1 = 'row'
        line_ornt_2 = 'column'
    else:
        line_ornts_1 = columns
        line_ornts_2 = rows
        line_ornt_1 = 'column'
        line_ornt_2 = 'row'

    # if current letter isn't already green
    if line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] != 'green':
        # try and swap with yellow letters from the same line and check if it makes a valid word
        try_yellow_letters(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions, line_index, letter_index, line_ornts_1, line_ornts_2, line_ornt_1, line_ornt_2)
        if solutions:
            return
        # try and swap with yellow letters from a perpendicular line and check if it makes a valid word
        try_yellow_perpendicular(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions, line_index, letter_index, line_ornts_1, line_ornts_2, line_ornt_1, line_ornt_2)
        if solutions:
            return
        # try and swap with white letters from other lines and check if it makes a valid word
        try_white_letters(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions, line_index, letter_index, line_ornts_1, line_ornt_1, line_ornt_2)
        if solutions:
            return
    else:
        # increase index to move to the next letter or line
        next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
        # call the function again with the new index
        solve_waffle(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions, next_line_index, next_letter_index)
    return

def try_yellow_letters(boxes: dict[int, dict], rows: dict[int, dict], columns: dict[int, dict], white_letters: list[dict], og_white_letters: list[dict], word_list: list[str], solutions: list[list], line_index: int, letter_index: int, line_ornts_1: dict[int, dict], line_ornts_2: dict[int, dict], line_ornt_1: str, line_ornt_2: str) -> None:
    yellow_keys = list(line_ornts_1[line_index % 3]['yellow'].keys()) # Has to be a list of indexes otherwise it freaks out when it pops something from dictionary
    for box in yellow_keys:
        # if the letter from the yellow pool isn't the same as the current letter, or (is the same but comes before the current letter and current letter is white)
        if line_ornts_1[line_index % 3]['yellow'][box]['letter'] != line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] or (line_ornts_1[line_index % 3]['yellow'][box]['letter'] == line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] and box < line_index and line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] == 'white'):
            # save what the current letter and color are and change current box to the yellow letter
            line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['letter']
            line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['color']
            line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_1[line_index % 3]['yellow'][box]['letter']
            # assume that the letter is correct and make it green
            line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = 'green'
            # waffle #891 exception
            # if yellow letter to be removed is on an intersection, remove it from the perpendicular line's yellow letters as well
            temp_3 = None
            pos_3 = None
            line_3 = None
            temp_4 = None
            pos_4 = None
            removed_yellow = False
            # if the yellow box is a member of a perpendicular line (on an intersection)
            if line_ornts_1[line_index % 3]['yellow'][box][line_ornt_2] != None:
                # iterate through the perpendicular line's yellow letters
                line_3 = line_ornts_1[line_index % 3]['yellow'][box][line_ornt_2]
                yellow_keys2 = list(line_ornts_2[line_3]['yellow'].keys())
                for box_2 in yellow_keys2:
                    # if the tile in the perpendicular line is the same as the first yellow tile, remove it
                    if line_ornts_2[line_3]['yellow'][box_2] == line_ornts_1[line_index % 3]['yellow'][box]:
                        # remove the tile and save the position in case backtracking is needed
                        pos_3 = box_2
                        temp_3 = line_ornts_2[line_3]['yellow'].pop(pos_3)
                        # flag that a yellow tile has been removed
                        removed_yellow = True
                        break
                if removed_yellow:
                    # if the perpendicular line contains a white tile that is the same letter as the removed yellow, remove the letter from white list
                    # (this step should also add the letter to the yellow list, but would require a restructuring of white line lists to hold boxes instead of letters) *
                    white_keys = list(line_ornts_2[line_3]['white'].keys())
                    for box_2 in white_keys:
                        if line_ornts_2[line_3]['white'][box_2] == line_ornts_1[line_index % 3]['yellow'][box]['letter']:
                            # remove the tile and save the position in case backtracking is needed
                            pos_4 = box_2
                            temp_4 = line_ornts_2[line_3]['white'].pop(pos_4)
                            break  
            # remove the box from the yellow letter list and save for backtracking
            temp = line_ornts_1[line_index % 3]['yellow'].pop(box)
            # waffle puzzle archive #138 exception
            # if current letter is intersectional, and the perpendicular line's yellow letter list contains this letter, remove the letter from that list as well
            temp_2 = None
            pos_2 = None
            line_2 = None
            # initialise variables for handling backtracking if a third yellow letter is to be removed
            temp_5 = None
            pos_5 = None
            line_5 = None
            if line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2] != None:
                line_2 = line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2]
                yellow_keys2 = list(line_ornts_2[line_2]['yellow'].keys())
                for box_2 in yellow_keys2:
                    if line_ornts_2[line_2]['yellow'][box_2]['letter'] == line_ornts_1[line_index % 3]['boxes'][letter_index]['letter']:
                        pos_2 = box_2
                        # if the additional yellow letter to be removed is on an intersection, remove the yellow letter from another perpendicular line as well
                        if line_ornts_2[line_2]['yellow'][box_2][line_ornt_1] != None:
                            line_5 = line_ornts_2[line_2]['yellow'][box_2][line_ornt_1]
                            yellow_keys3 = list(line_ornts_1[line_5]['yellow'].keys())
                            for box_3 in yellow_keys3:
                                if line_ornts_1[line_5]['yellow'][box_3] == line_ornts_2[line_2]['yellow'][box_2]:
                                    pos_5 = box_3
                                    temp_5 = line_ornts_1[line_5]['yellow'].pop(pos_5)
                        temp_2 = line_ornts_2[line_2]['yellow'].pop(pos_2)
                        break
                
            # check if valid word can be made with this letter
            if makes_valid_word(rows, columns, line_index, word_list):
                next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
                solve_waffle(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions, next_line_index, next_letter_index)
                if solutions:
                    return
            # return box to yellow letter list
            line_ornts_1[line_index % 3]['yellow'][box] = temp
            # return other box to perpendicular yellow list if it was removed
            if temp_2 != None:
                line_ornts_2[line_2]['yellow'][pos_2] = temp_2
            if temp_3 != None:
                line_ornts_2[line_3]['yellow'][pos_3] = temp_3
            # return removed white letter to perpendicular line if removed
            if temp_4 != None:
                line_ornts_2[line_3]['white'][pos_4] = temp_4
            # return extra intersectional box to 2nd perpendicular line's yellow list if removed
            if temp_5 != None:
                line_ornts_1[line_5]['yellow'][pos_5] = temp_5
            line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter']
            line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = None
            line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color']
            line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = None

def try_yellow_perpendicular(boxes: dict[int, dict], rows: dict[int, dict], columns: dict[int, dict], white_letters: list[dict], og_white_letters: list[dict], word_list: list[str], solutions: list[list], line_index: int, letter_index: int, line_ornts_1: dict[int, dict], line_ornts_2: dict[int, dict], line_ornt_1: str, line_ornt_2: str) -> None:
    if line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2] != None:
        line = line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2]
        yellow_keys = list(line_ornts_2[line]['yellow'].keys())
        for box in yellow_keys:
            if line_ornts_2[line]['yellow'][box]['letter'] != line_ornts_1[line_index % 3]['boxes'][letter_index]['letter']:
                # save what the current letter and color are and change current box to the yellow letter
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['letter']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['color']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_2[line]['yellow'][box]['letter']
                # assume that the letter is correct and make it green
                line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = 'green'
                temp_2 = None
                pos_2 = None
                line_2 = None
                # archive #2 exception:
                # if a yellow letter in a perpendicular line is on an intersection with another perpendicular line, remove the yellow letter from that line
                if line_ornts_2[line]['yellow'][box][line_ornt_1] != None:
                    line_2 = line_ornts_2[line]['yellow'][box][line_ornt_1]
                    yellow_keys2 = list(line_ornts_1[line_2]['yellow'].keys())
                    for box_2 in yellow_keys2:
                        # if the box in the second perpendicular line is the same as the one in the first perpendicular line, remove it from the second perpendicular's yellow list
                        if line_ornts_1[line_2]['yellow'][box_2] == line_ornts_2[line]['yellow'][box]:
                            pos_2 = box_2
                            temp_2 = line_ornts_1[line_2]['yellow'].pop(pos_2)
                            break
                # remove the box from the yellow letter list
                temp = line_ornts_2[line]['yellow'].pop(box)
                if makes_valid_word(rows, columns, line_index, word_list):
                    next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
                    solve_waffle(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions, next_line_index, next_letter_index)
                    if solutions:
                        return
                line_ornts_2[line]['yellow'][box] = temp
                if temp_2 != None:
                    line_ornts_1[line_2]['yellow'][pos_2] = temp_2
                line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = None
                line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = None

def try_white_letters(boxes: dict[int, dict], rows: dict[int, dict], columns: dict[int, dict], white_letters: list[dict], og_white_letters: list[dict], word_list: list[str], solutions: list[list], line_index: int, letter_index: int, line_ornts_1: dict[int, dict], line_ornt_1: str, line_ornt_2: str) -> None:
    for box in range(len(white_letters)):
        valid_white = True
        for box_2 in line_ornts_1[line_index % 3]['white']:
            if white_letters[box]['letter'] == line_ornts_1[line_index % 3]['white'][box_2]:
                valid_white = False
        if valid_white:

        # # white letter isn't in the same line as current letter # #
        # if white_letters[box][line_ornt_1] != line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_1]:

            # white letter isn't in a perpendicular line
            if not (line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2] != None and white_letters[box][line_ornt_2] == line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2]):
                # save what the current letter and color are and change current box to the white letter
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['letter']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['color']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = white_letters[box]['letter']
                # assume that the letter is correct and make it green
                line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = 'green'
                # remove the box from the white letter list
                temp = white_letters.pop(box)
                # remove the box from the original white letter list if the index is within range
                temp_2 = None
                if box < len(og_white_letters):
                    temp_2 = og_white_letters.pop(box)
                if makes_valid_word(rows, columns, line_index, word_list):
                    next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
                    solve_waffle(boxes, rows, columns, white_letters, og_white_letters, word_list, solutions, next_line_index, next_letter_index)
                    if solutions:
                        return
                white_letters.insert(box, temp)
                # return the box to the original white letter list
                if temp_2 != None:
                    og_white_letters.insert(box, temp_2)
                line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = None
                line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = None

def increment_indexes(line_index: int, letter_index: int) -> Tuple[int, int]:
    letter_index += 1
    if letter_index == 5:
        line_index += 1
        letter_index = 0
    return line_index, letter_index

def makes_valid_word(rows: dict[int, dict], columns: dict[int, dict], line_index: str, word_list: list[str]) -> bool:
    green_letters, yellow_letters, line_white_letters = get_colored_letters(rows, columns, line_index)
    for word in word_list:
        current_word = word
        valid = True
        # check whether any words match the current green letter positions
        valid, current_word = compare_with_greens(green_letters, current_word, valid)
        if valid:
            # check that current word contains all of the letters that are currently yellow
            valid, current_word, line_white_letters = compare_with_yellows(line_index, yellow_letters, line_white_letters, current_word, valid)
            if valid:
                # check that current word doesn't contain any of this line's initial white letters
                valid, current_word = compare_with_whites(line_white_letters, current_word, valid)
                if valid:
                    print("line:", line_index, "word:", current_word)
                    return True
    return False

def get_colored_letters(rows: dict[int, dict], columns: dict[int, dict], line_index: str) -> Tuple[dict[int, str], dict[int, dict], dict[int, str]]:
    green_letters = {}
    # check rows for green letters
    if line_index < 3:
        for i in range(len(rows[line_index]['boxes'])):
            if rows[line_index]['boxes'][i]['color'] == 'green':
                green_letters[i] = rows[line_index]['boxes'][i]['letter']
        yellow_letters = rows[line_index]['yellow']
        line_white_letters = rows[line_index]['white']
    else:
        for i in range(len(columns[line_index % 3]['boxes'])):
            if columns[line_index % 3]['boxes'][i]['color'] == 'green':
                green_letters[i] = columns[line_index % 3]['boxes'][i]['letter']
        yellow_letters = columns[line_index % 3]['yellow']
        line_white_letters = columns[line_index % 3]['white']
    return green_letters, yellow_letters, line_white_letters

def compare_with_greens(green_letters: dict[int, str], current_word: str, valid: bool) -> Tuple[bool, str]:
    for pos, letter in green_letters.items():
        if current_word[pos] != letter:
            valid = False
            break
        else:
            temp_word = list(current_word)
            temp_word[pos] = temp_word[pos].upper()
            current_word = "".join(temp_word)
    return valid, current_word

def compare_with_yellows(line_index: int, yellow_letters: dict[int, dict], line_white_letters: dict[int, str], current_word: str, valid: bool) -> Tuple[bool, str, dict[int, str]]:
    if line_index < 3:
        line_ornt = 'column'
    else:
        line_ornt = 'row'

    for pos in yellow_letters:
        letter = yellow_letters[pos]['letter']
        # check whether yellow letter is on an intersection
        if yellow_letters[pos][line_ornt] == None:
            if letter not in current_word:
                valid = False
                break
            else:
                positions_to_remove = []
                for pos_2, letter_2 in line_white_letters.items():
                    # if a white letter is the same letter as a yellow letter, and the white letter comes after it
                    # sequentially, then then that letter is in the word, so remove the white letter
                    if letter_2 == letter and pos_2 > pos:
                        # save positions to list
                        positions_to_remove.append(pos_2)
                # remove the marked positions after the iteration
                for pos_2 in positions_to_remove:
                    line_white_letters.pop(pos_2)
        else:
            positions_to_remove = []
            for pos_2, letter_2 in line_white_letters.items():
                # if a white letter is the same letter as an intersectional yellow letter, and the white letter comes after it
                # sequentially, then we can't say for sure that that letter isn't in the word, so remove the white letter
                if letter_2 == letter and pos_2 > pos:
                    # save positions to list
                    positions_to_remove.append(pos_2)
            # remove the marked positions after the iteration
            for pos_2 in positions_to_remove:
                line_white_letters.pop(pos_2)
    return valid, current_word, line_white_letters

def compare_with_whites(line_white_letters: dict[int, str], current_word: str, valid: bool) -> Tuple[bool, str]:
    for pos, letter in line_white_letters.items():
        if letter in current_word:
            valid = False
            break
    return valid, current_word

def get_word_list() -> list[str]:
    word_list = [
    'aback',     'abase',     'abate',     'abbey',     'abbot',     'abhor',     'abide',
    'abled',     'abode',     'abort',     'about',     'above',     'abuse',     'abyss',     'acorn',
    'acrid',     'actor',     'acute',     'adage',     'adapt',     'adept',     'admin',     'admit',
    'adobe',     'adopt',     'adore',     'adorn',     'adult',     'affix',     'afire',     'afoot',
    'afoul',     'after',     'again',     'agape',     'agate',     'agent',     'agile',     'aging',
    'aglow',     'agony',     'agree',     'ahead',     'aider',     'aisle',     'alarm',     'album',
    'alert',     'algae',     'alibi',     'alien',     'align',     'alike',     'alive',     'allay',
    'alley',     'allot',     'allow',     'alloy',     'aloft',     'alone',     'along',     'aloof',
    'aloud',     'alpha',     'altar',     'alter',     'amass',     'amaze',     'amber',     'amble',
    'amend',     'amiss',     'amity',     'among',     'ample',     'amply',     'amuse',     'angel',
    'anger',     'angle',     'angry',     'angst',     'anime',     'ankle',     'annex',     'annoy',
    'annul',     'anode',     'antic',     'anvil',     'aorta',     'apart',     'aphid',     'aping',
    'apnea',     'apple',     'apply',     'apron',     'aptly',     'arbor',     'ardor',     'arena',
    'argue',     'arise',     'armor',     'aroma',     'arose',     'array',     'arrow',     'arson',
    'artsy',     'ascot',     'ashen',     'aside',     'askew',     'assay',     'asset',     'atoll',
    'atone',     'attic',     'audio',     'audit',     'augur',     'aunty',     'avail',     'avert',
    'avian',     'avoid',     'await',     'awake',     'award',     'aware',     'awash',     'awful',
    'awoke',     'axial',     'axiom',     'axion',     'azure',     'bacon',     'badge',     'badly',
    'bagel',     'baggy',     'baker',     'baler',     'balmy',     'banal',     'banjo',     'barge',
    'baron',     'basal',     'basic',     'basil',     'basin',     'basis',     'baste',     'batch',
    'bathe',     'baton',     'batty',     'bawdy',     'bayou',     'beach',     'beady',     'beard',
    'beast',     'beech',     'beefy',     'befit',     'began',     'begat',     'beget',     'begin',
    'begun',     'being',     'belch',     'belie',     'belle',     'belly',     'below',     'bench',
    'beret',     'berry',     'berth',     'beset',     'betel',     'bevel',     'bezel',     'bible',
    'bicep',     'biddy',     'bigot',     'bilge',     'billy',     'binge',     'bingo',     'biome',
    'birch',     'birth',     'bison',     'bitty',     'black',     'blade',     'blame',     'bland',
    'blank',     'blare',     'blast',     'blaze',     'bleak',     'bleat',     'bleed',     'bleep',
    'blend',     'bless',     'blimp',     'blind',     'blink',     'bliss',     'blitz',     'bloat',
    'block',     'bloke',     'blond',     'blood',     'bloom',     'blown',     'bluer',     'bluff',
    'blunt',     'blurb',     'blurt',     'blush',     'board',     'boast',     'bobby',     'boney',
    'bongo',     'bonus',     'booby',     'boost',     'booth',     'booty',     'booze',     'boozy',
    'borax',     'borne',     'bosom',     'bossy',     'botch',     'bough',     'boule',     'bound',
    'bowel',     'boxer',     'brace',     'braid',     'brain',     'brake',     'brand',     'brash',
    'brass',     'brave',     'bravo',     'brawl',     'brawn',     'bread',     'break',     'breed',
    'briar',     'bribe',     'brick',     'bride',     'brief',     'brine',     'bring',     'brink',
    'briny',     'brisk',     'broad',     'broil',     'broke',     'brood',     'brook',     'broom',
    'broth',     'brown',     'brunt',     'brush',     'brute',     'buddy',     'budge',     'buggy',
    'bugle',     'build',     'built',     'bulge',     'bulky',     'bully',     'bunch',     'bunny',
    'burly',     'burnt',     'burst',     'bused',     'bushy',     'butch',     'butte',     'buxom',
    'buyer',     'bylaw',     'cabal',     'cabby',     'cabin',     'cable',     'cacao',     'cache',
    'cacti',     'caddy',     'cadet',     'cagey',     'cairn',     'camel',     'cameo',     'canal',
    'candy',     'canny',     'canoe',     'canon',     'caper',     'caput',     'carat',     'carer',
    'cargo',     'carol',     'carry',     'carve',     'caste',     'catch',     'cater',     'catty',
    'caulk',     'cause',     'cavil',     'cease',     'cedar',     'cello',     'chafe',     'chaff',
    'chain',     'chair',     'chalk',     'champ',     'chant',     'chaos',     'chard',     'charm',
    'chart',     'chase',     'chasm',     'cheap',     'cheat',     'check',     'cheek',     'cheer',
    'chess',     'chest',     'chewy',     'chick',     'chide',     'chief',     'child',     'chili',     'chill',
    'chime',     'china',     'chirp',     'chock',     'choir',     'choke',     'chord',     'chore',
    'chose',     'chuck',     'chump',     'chunk',     'churn',     'chute',     'cider',     'cigar',
    'cinch',     'circa',     'civic',     'civil',     'clack',     'claim',     'clamp',     'clang',
    'clank',     'clash',     'clasp',     'class',     'clean',     'clear',     'cleat',     'cleft',
    'clerk',     'click',     'cliff',     'climb',     'cling',     'clink',     'cloak',     'clock',
    'clone',     'close',     'cloth',     'cloud',     'clout',     'clove',     'clown',     'cluck',
    'clued',     'clump',     'clung',     'coach',     'coast',     'cobra',     'cocoa',     'colon',
    'color',     'comet',     'comfy',     'comic',     'comma',     'conch',     'condo',     'conic',
    'copse',     'coral',     'corer',     'corny',     'couch',     'cough',     'could',     'count',
    'coupe',     'court',     'coven',     'cover',     'covet',     'covey',     'cower',     'coyly',
    'crack',     'craft',     'cramp',     'crane',     'crank',     'crash',     'crass',     'crate',
    'crave',     'crawl',     'craze',     'crazy',     'creak',     'cream',     'credo',     'creed',
    'creek',     'creep',     'creme',     'crepe',     'crept',     'cress',     'crest',     'crick',
    'cried',     'crier',     'crime',     'crimp',     'crisp',     'croak',     'crock',     'crone',
    'crony',     'crook',     'cross',     'croup',     'crowd',     'crown',     'crude',     'cruel',
    'crumb',     'crump',     'crush',     'crust',     'crypt',     'cubic',     'cumin',     'curio',
    'curly',     'curry',     'curse',     'curve',     'curvy',     'cutie',     'cyber',     'cycle',
    'cynic',     'daddy',     'daily',     'dairy',     'daisy',     'dally',     'dance',     'dandy',
    'datum',     'daunt',     'dealt',     'death',     'debar',     'debit',     'debug',     'debut',
    'decal',     'decay',     'decor',     'decoy',     'decry',     'defer',     'deign',     'deity',
    'delay',     'delta',     'delve',     'demon',     'demur',     'denim',     'dense',     'depot',
    'depth',     'derby',     'deter',     'detox',     'deuce',     'devil',     'diary',     'dicey',
    'digit',     'dilly',     'dimly',     'diner',     'dingo',     'dingy',     'diode',     'dirge',
    'dirty',     'disco',     'ditch',     'ditto',     'ditty',     'diver',     'dizzy',     'dodge',
    'dodgy',     'dogma',     'doing',     'dolly',     'donor',     'donut',     'dopey',     'doubt',
    'dough',     'dowdy',     'dowel',     'downy',     'dowry',     'dozen',     'draft',     'drain',
    'drake',     'drama',     'drank',     'drape',     'drawl',     'drawn',     'dread',     'dream',
    'dress',     'dried',     'drier',     'drift',     'drill',     'drink',     'drive',     'droit',
    'droll',     'drone',     'drool',     'droop',     'dross',     'drove',     'drown',     'druid',
    'drunk',     'dryer',     'dryly',     'duchy',     'dully',     'dummy',     'dumpy',     'dunce',
    'dusky',     'dusty',     'dutch',     'duvet',     'dwarf',     'dwell',     'dwelt',     'dying',
    'eager',     'eagle',     'early',     'earth',     'easel',     'eaten',     'eater',     'ebony',
    'eclat',     'edict',     'edify',     'eerie',     'egret',     'eight',     'eject',     'eking',
    'elate',     'elbow',     'elder',     'elect',     'elegy',     'elfin',     'elide',     'elite',
    'elope',     'elude',     'email',     'embed',     'ember',     'emcee',     'empty',     'enact',
    'endow',     'enema',     'enemy',     'enjoy',     'ennui',     'ensue',     'enter',     'entry',
    'envoy',     'epoch',     'epoxy',     'equal',     'equip',     'erase',     'erect',     'erode',
    'error',     'erupt',     'essay',     'ester',     'ether',     'ethic',     'ethos',     'etude',
    'evade',     'event',     'every',     'evict',     'evoke',     'exact',     'exalt',     'excel',
    'exert',     'exile',     'exist',     'expel',     'extol',     'extra',     'exult',     'eying',
    'fable',     'facet',     'faint',     'fairy',     'faith',     'false',     'fancy',     'fanny',
    'farce',     'fatal',     'fatty',     'fault',     'fauna',     'favor',     'feast',     'fecal',
    'feign',     'fella',     'felon',     'femme',     'femur',     'fence',     'feral',     'ferry',
    'fetal',     'fetch',     'fetid',     'fetus',     'fever',     'fewer',     'fiber',     'ficus',
    'field',     'fiend',     'fiery',     'fifth',     'fifty',     'fight',     'filer',     'filet',
    'filly',     'filmy',     'filth',     'final',     'finch',     'finer',     'first',     'fishy',
    'fixer',     'fizzy',     'fjord',     'flack',     'flail',     'flair',     'flake',     'flaky',
    'flame',     'flank',     'flare',     'flash',     'flask',     'fleck',     'fleet',     'flesh',
    'flick',     'flier',     'fling',     'flint',     'flirt',     'float',     'flock',     'flood',
    'floor',     'flora',     'floss',     'flour',     'flout',     'flown',     'fluff',     'fluid',
    'fluke',     'flume',     'flung',     'flunk',     'flush',     'flute',     'flyer',     'foamy',
    'focal',     'focus',     'foggy',     'foist',     'folio',     'folly',     'foray',     'force',
    'forge',     'forgo',     'forte',     'forth',     'forty',     'forum',     'found',     'foyer',
    'frail',     'frame',     'frank',     'fraud',     'freak',     'freed',     'freer',     'fresh',
    'friar',     'fried',     'frill',     'frisk',     'fritz',     'frock',     'frond',     'front',
    'frost',     'froth',     'frown',     'froze',     'fruit',     'fudge',     'fugue',     'fully',
    'fungi',     'funky',     'funny',     'furor',     'furry',     'fussy',     'fuzzy',     'gaffe',
    'gaily',     'gamer',     'gamma',     'gamut',     'gassy',     'gaudy',     'gauge',     'gaunt',
    'gauze',     'gavel',     'gawky',     'gayer',     'gayly',     'gazer',     'gecko',     'geeky',
    'geese',     'genie',     'genre',     'ghost',     'ghoul',     'giant',     'giddy',     'gipsy',
    'girly',     'girth',     'given',     'giver',     'glade',     'gland',     'glare',     'glass',
    'glaze',     'gleam',     'glean',     'glide',     'glint',     'gloat',     'globe',     'gloom',
    'glory',     'gloss',     'glove',     'glyph',     'gnash',     'gnome',     'godly',     'going',
    'golem',     'golly',     'gonad',     'goner',     'goody',     'gooey',     'goofy',     'goose',
    'gorge',     'gouge',     'gourd',     'grace',     'grade',     'graft',     'grail',     'grain',
    'grand',     'grant',     'grape',     'graph',     'grasp',     'grass',     'grate',     'grave',
    'gravy',     'graze',     'great',     'greed',     'green',     'greet',     'grief',     'grill',
    'grime',     'grimy',     'grind',     'gripe',     'groan',     'groin',     'groom',     'grope',
    'gross',     'group',     'grout',     'grove',     'growl',     'grown',     'gruel',     'gruff',
    'grunt',     'guard',     'guava',     'guess',     'guest',     'guide',     'guild',     'guile',
    'guilt',     'guise',     'gulch',     'gully',     'gumbo',     'gummy',     'guppy',     'gusto',
    'gusty',     'gypsy',     'habit',     'hairy',     'halve',     'handy',     'happy',     'hardy',
    'harem',     'harpy',     'harry',     'harsh',     'haste',     'hasty',     'hatch',     'hater',
    'haunt',     'haute',     'haven',     'havoc',     'hazel',     'heady',     'heard',     'heart',
    'heath',     'heave',     'heavy',     'hedge',     'hefty',     'heist',     'helix',     'hello',
    'hence',     'heron',     'hilly',     'hinge',     'hippo',     'hippy',     'hitch',     'hoard',
    'hobby',     'hoist',     'holly',     'homer',     'honey',     'honor',     'hoped',     'horde',     'horny',
    'horse',     'hotel',     'hotly',     'hound',     'house',     'hovel',     'hover',     'howdy',
    'human',     'humid',     'humor',     'humph',     'humus',     'hunch',     'hunky',     'hurry',
    'husky',     'hussy',     'hutch',     'hydro',     'hyena',     'hymen',     'hyper',     'icily',
    'icing',     'ideal',     'idiom',     'idiot',     'idler',     'idyll',     'igloo',     'iliac',
    'image',     'imbue',     'impel',     'imply',     'inane',     'inbox',     'incur',     'index',
    'inept',     'inert',     'infer',     'ingot',     'inlay',     'inlet',     'inner',     'input',
    'inter',     'intro',     'ionic',     'irate',     'irony',     'islet',     'issue',     'itchy',
    'ivory',     'jaunt',     'jazzy',     'jelly',     'jerky',     'jetty',     'jewel',     'jiffy',
    'joint',     'joist',     'joker',     'jolly',     'joust',     'judge',     'juice',     'juicy',
    'jumbo',     'jumpy',     'junta',     'junto',     'juror',     'kappa',     'kaput',     'karma',     'kayak',
    'kebab',     'khaki',     'kinky',     'kiosk',     'kitty',     'knack',     'knave',     'knead',
    'kneed',     'kneel',     'knelt',     'knife',     'knock',     'knoll',     'known',     'koala',
    'krill',     'label',     'labor',     'laden',     'ladle',     'lager',     'lance',     'lanky',
    'lapel',     'lapse',     'large',     'larva',     'lasso',     'latch',     'later',     'lathe',
    'latte',     'laugh',     'layer',     'leach',     'leafy',     'leaky',     'leant',     'leapt',
    'learn',     'lease',     'leash',     'least',     'leave',     'ledge',     'leech',     'leery',
    'lefty',     'legal',     'leggy',     'lemon',     'lemur',     'leper',     'level',     'lever',
    'libel',     'liege',     'light',     'liken',     'lilac',     'limbo',     'limit',     'linen',
    'liner',     'lingo',     'lipid',     'lithe',     'liver',     'livid',     'llama',     'loamy',
    'loath',     'lobby',     'local',     'locus',     'lodge',     'lofty',     'logic',     'login',
    'loopy',     'loose',     'lorry',     'loser',     'louse',     'lousy',     'lover',     'lower',
    'lowly',     'loyal',     'lucid',     'lucky',     'lumen',     'lumpy',     'lunar',     'lunch',
    'lunge',     'lupus',     'lurch',     'lurid',     'lusty',     'lying',     'lymph',     'lyric',
    'macaw',     'macho',     'macro',     'madam',     'madly',     'mafia',     'magic',     'magma',
    'maize',     'major',     'maker',     'mambo',     'mamma',     'mammy',     'manga',     'mange',
    'mango',     'mangy',     'mania',     'manic',     'manly',     'manor',     'maple',     'march',
    'marry',     'marsh',     'mason',     'masse',     'match',     'matey',     'mauve',     'maxim',
    'maybe',     'mayor',     'mealy',     'meant',     'meaty',     'mecca',     'medal',     'media',
    'medic',     'melee',     'melon',     'mercy',     'merge',     'merit',     'merry',     'metal',
    'meter',     'metro',     'micro',     'midge',     'midst',     'might',     'milky',     'mimic',
    'mince',     'miner',     'minim',     'minor',     'minty',     'minus',     'mirth',     'miser',
    'missy',     'mocha',     'modal',     'model',     'modem',     'mogul',     'moist',     'molar',
    'moldy',     'money',     'month',     'moody',     'moose',     'moral',     'moron',     'morph',
    'mossy',     'motel',     'motif',     'motor',     'motto',     'moult',     'mound',     'mount',
    'mourn',     'mouse',     'mouth',     'mover',     'movie',     'mower',     'mucky',     'mucus',
    'muddy',     'mulch',     'mummy',     'munch',     'mural',     'murky',     'mushy',     'music',
    'musky',     'musty',     'myrrh',     'nadir',     'naive',     'naked',     'nanny',     'nasal',     'nasty',
    'natal',     'naval',     'navel',     'needy',     'neigh',     'nerdy',     'nerve',     'never',
    'newer',     'newly',     'nicer',     'niche',     'niece',     'night',     'ninja',     'ninny',
    'ninth',     'noble',     'nobly',     'noise',     'noisy',     'nomad',     'noose',     'north',
    'nosey',     'notch',     'novel',     'nudge',     'nurse',     'nutty',     'nylon',     'nymph',
    'oaken',     'obese',     'occur',     'ocean',     'octal',     'octet',     'odder',     'oddly',
    'offal',     'offer',     'often',     'olden',     'older',     'olive',     'ombre',     'omega',
    'onion',     'onset',     'opera',     'opine',     'opium',     'optic',     'orbit',     'order',
    'organ',     'other',     'otter',     'ought',     'ounce',     'outdo',     'outer',     'outgo',
    'ovary',     'ovate',     'overt',     'ovine',     'ovoid',     'owing',     'owner',     'oxide',
    'ozone',     'paddy',     'pagan',     'paint',     'paler',     'palsy',     'panel',     'panic',
    'pansy',     'papal',     'paper',     'parer',     'parka',     'parry',     'parse',     'party',
    'pasta',     'paste',     'pasty',     'patch',     'patio',     'patsy',     'patty',     'pause',
    'payee',     'payer',     'peace',     'peach',     'pearl',     'pecan',     'pedal',     'penal',
    'pence',     'penne',     'penny',     'perch',     'peril',     'perky',     'pesky',     'pesto',
    'petal',     'petty',     'phase',     'phone',     'phony',     'photo',     'piano',     'picky',
    'piece',     'piety',     'piggy',     'pilot',     'pinch',     'piney',     'pinky',     'pinto',
    'piper',     'pique',     'pitch',     'pithy',     'pivot',     'pixel',     'pixie',     'pizza',
    'place',     'plaid',     'plain',     'plait',     'plane',     'plank',     'plant',     'plate',
    'plaza',     'plead',     'pleat',     'plied',     'plier',     'pluck',     'plumb',     'plume',
    'plump',     'plunk',     'plush',     'poesy',     'point',     'poise',     'poker',     'polar',
    'polka',     'polyp',     'pooch',     'poppy',     'porch',     'poser',     'posit',     'posse',
    'pouch',     'pound',     'pouty',     'power',     'prank',     'prawn',     'preen',     'press',
    'price',     'prick',     'pride',     'pried',     'prime',     'primo',     'print',     'prior',
    'prism',     'privy',     'prize',     'probe',     'prone',     'prong',     'proof',     'prose',
    'proud',     'prove',     'prowl',     'proxy',     'prude',     'prune',     'psalm',     'pubic',
    'pudgy',     'puffy',     'pulpy',     'pulse',     'punch',     'pupil',     'puppy',     'puree',
    'purer',     'purge',     'purse',     'pushy',     'putty',     'pygmy',     'quack',     'quail',
    'quake',     'qualm',     'quark',     'quart',     'quash',     'quasi',     'queen',     'queer',
    'quell',     'query',     'quest',     'queue',     'quick',     'quiet',     'quill',     'quilt',
    'quirk',     'quite',     'quota',     'quote',     'quoth',     'rabbi',     'rabid',     'racer',
    'radar',     'radii',     'radio',     'rainy',     'raise',     'rajah',     'rally',     'ralph',
    'ramen',     'ranch',     'randy',     'range',     'rapid',     'rarer',     'raspy',     'ratio',
    'ratty',     'raven',     'rayon',     'razor',     'reach',     'react',     'ready',     'realm',
    'rearm',     'rebar',     'rebel',     'rebus',     'rebut',     'recap',     'recur',     'recut',
    'reedy',     'refer',     'refit',     'regal',     'rehab',     'reign',     'relax',     'relay',
    'relic',     'remit',     'renal',     'renew',     'repay',     'repel',     'reply',     'rerun',
    'reset',     'resin',     'retch',     'retro',     'retry',     'reuse',     'revel',     'revue',
    'rhino',     'rhyme',     'rider',     'ridge',     'rifle',     'right',     'rigid',     'rigor',
    'rinse',     'ripen',     'riper',     'risen',     'riser',     'risky',     'rival',     'river',
    'rivet',     'roach',     'roast',     'robin',     'robot',     'rocky',     'rodeo',     'roger',
    'rogue',     'roomy',     'roost',     'rotor',     'rouge',     'rough',     'round',     'rouse',
    'route',     'rover',     'rowdy',     'rower',     'royal',     'ruddy',     'ruder',     'rugby',
    'ruler',     'rumba',     'rumor',     'rupee',     'rural',     'rusty',     'sadly',     'safer',
    'saint',     'salad',     'sally',     'salon',     'salsa',     'salty',     'salve',     'salvo',
    'sandy',     'saner',     'sappy',     'sassy',     'satin',     'satyr',     'sauce',     'saucy',
    'sauna',     'saute',     'savor',     'savoy',     'savvy',     'scald',     'scale',     'scalp',
    'scaly',     'scamp',     'scant',     'scare',     'scarf',     'scary',     'scene',     'scent',
    'scion',     'scoff',     'scold',     'scone',     'scoop',     'scope',     'score',     'scorn',
    'scour',     'scout',     'scowl',     'scram',     'scrap',     'scree',     'screw',     'scrub',
    'scrum',     'scuba',     'sedan',     'seedy',     'segue',     'seize',     'semen',     'sense',
    'sepia',     'serif',     'serum',     'serve',     'setup',     'seven',     'sever',     'sewer',
    'shack',     'shade',     'shady',     'shaft',     'shake',     'shaky',     'shale',     'shall',
    'shalt',     'shame',     'shank',     'shape',     'shard',     'share',     'shark',     'sharp',
    'shave',     'shawl',     'shear',     'sheen',     'sheep',     'sheer',     'sheet',     'sheik',
    'shelf',     'shell',     'shied',     'shift',     'shine',     'shiny',     'shire',     'shirk',
    'shirt',     'shoal',     'shock',     'shone',     'shook',     'shoot',     'shore',     'shorn',
    'short',     'shout',     'shove',     'shown',     'showy',     'shrew',     'shrub',     'shrug',
    'shuck',     'shunt',     'shush',     'shyly',     'siege',     'sieve',     'sight',     'sigma',
    'silky',     'silly',     'since',     'sinew',     'singe',     'siren',     'sissy',     'sixth',
    'sixty',     'skate',     'skier',     'skiff',     'skill',     'skimp',     'skirt',     'skulk',
    'skull',     'skunk',     'slack',     'slain',     'slang',     'slant',     'slash',     'slate',
    'sleek',     'sleep',     'sleet',     'slept',     'slice',     'slick',     'slide',     'slime',
    'slimy',     'sling',     'slink',     'sloop',     'slope',     'slosh',     'sloth',     'slump',
    'slung',     'slunk',     'slurp',     'slush',     'slyly',     'smack',     'small',     'smart',
    'smash',     'smear',     'smell',     'smelt',     'smile',     'smirk',     'smite',     'smith',
    'smock',     'smoke',     'smoky',     'smote',     'snack',     'snail',     'snake',     'snaky',
    'snare',     'snarl',     'sneak',     'sneer',     'snide',     'sniff',     'snipe',     'snoop',
    'snore',     'snort',     'snout',     'snowy',     'snuck',     'snuff',     'soapy',     'sober',
    'soggy',     'solar',     'solid',     'solve',     'sonar',     'sonic',     'sooth',     'sooty',
    'sorry',     'sound',     'south',     'sower',     'space',     'spade',     'spank',     'spare',
    'spark',     'spasm',     'spawn',     'speak',     'spear',     'speck',     'speed',     'spell',
    'spelt',     'spend',     'spent',     'sperm',     'spice',     'spicy',     'spied',     'spiel',
    'spike',     'spiky',     'spill',     'spilt',     'spine',     'spiny',     'spire',     'spite',
    'splat',     'split',     'spoil',     'spoke',     'spoof',     'spook',     'spool',     'spoon',
    'spore',     'sport',     'spout',     'spray',     'spree',     'sprig',     'spunk',     'spurn',
    'spurt',     'squad',     'squat',     'squib',     'stack',     'staff',     'stage',     'staid',
    'stain',     'stair',     'stake',     'stale',     'stalk',     'stall',     'stamp',     'stand',
    'stank',     'stare',     'stark',     'start',     'stash',     'state',     'stave',     'stead',
    'steak',     'steal',     'steam',     'steed',     'steel',     'steep',     'steer',     'stein',
    'stern',     'stick',     'stiff',     'still',     'stilt',     'sting',     'stink',     'stint',
    'stock',     'stoic',     'stoke',     'stole',     'stomp',     'stone',     'stony',     'stood',
    'stool',     'stoop',     'store',     'stork',     'storm',     'story',     'stout',     'stove',
    'strap',     'straw',     'stray',     'strip',     'strut',     'stuck',     'study',     'stuff',
    'stump',     'stung',     'stunk',     'stunt',     'style',     'suave',     'sugar',     'suing',
    'suite',     'sulky',     'sully',     'sumac',     'sunny',     'super',     'surer',     'surge',
    'surly',     'sushi',     'swami',     'swamp',     'swarm',     'swash',     'swath',     'swear',
    'sweat',     'sweep',     'sweet',     'swell',     'swept',     'swift',     'swill',     'swine',
    'swing',     'swirl',     'swish',     'swoon',     'swoop',     'sword',     'swore',     'sworn',
    'swung',     'synod',     'syrup',     'tabby',     'table',     'taboo',     'tacit',     'tacky',
    'taffy',     'taint',     'taken',     'taker',     'tally',     'talon',     'tamer',     'tango',
    'tangy',     'taper',     'tapir',     'tardy',     'tarot',     'taste',     'tasty',     'tatty',
    'taunt',     'tawny',     'teach',     'teary',     'tease',     'teddy',     'teeth',     'tempo',
    'tenet',     'tenor',     'tense',     'tenth',     'tepee',     'tepid',     'terra',     'terse',
    'testy',     'thank',     'theft',     'their',     'theme',     'there',     'these',     'theta',
    'thick',     'thief',     'thigh',     'thing',     'think',     'third',     'thong',     'thorn',
    'those',     'three',     'threw',     'throb',     'throw',     'thrum',     'thumb',     'thump',
    'thyme',     'tiara',     'tibia',     'tidal',     'tiger',     'tight',     'tilde',     'timer',
    'timid',     'tipsy',     'titan',     'tithe',     'title',     'toast',     'today',     'toddy',
    'token',     'tonal',     'tonga',     'tonic',     'tooth',     'topaz',     'topic',     'torch',
    'torso',     'torus',     'total',     'totem',     'touch',     'tough',     'towel',     'tower',
    'toxic',     'toxin',     'trace',     'track',     'tract',     'trade',     'trail',     'train',
    'trait',     'tramp',     'trash',     'trawl',     'tread',     'treat',     'trend',     'triad',
    'trial',     'tribe',     'trice',     'trick',     'tried',     'tripe',     'trite',     'troll',
    'troop',     'trope',     'trout',     'trove',     'truce',     'truck',     'truer',     'truly',
    'trump',     'trunk',     'truss',     'trust',     'truth',     'tryst',     'tubal',     'tuber',
    'tulip',     'tulle',     'tumor',     'tuner',     'tunic',     'turbo',     'tutor',     'twang',     'tweak',
    'tweed',     'tweet',     'twice',     'twine',     'twirl',     'twist',     'twixt',     'tying',
    'udder',     'ulcer',     'ultra',     'umbra',     'uncle',     'uncut',     'under',     'undid',
    'undue',     'unfed',     'unfit',     'unify',     'union',     'unite',     'unity',     'unlit',
    'unmet',     'unset',     'untie',     'until',     'unwed',     'unzip',     'upper',     'upset',
    'urban',     'urine',     'usage',     'usher',     'using',     'usual',     'usurp',     'utile',
    'utter',     'vague',     'valet',     'valid',     'valor',     'value',     'valve',     'vapid',
    'vapor',     'vault',     'vaunt',     'vegan',     'venom',     'venue',     'verge',     'verse',
    'verso',     'verve',     'vicar',     'video',     'vigil',     'vigor',     'villa',     'vinyl',
    'viola',     'viper',     'viral',     'virus',     'visit',     'visor',     'vista',     'vital',
    'vivid',     'vixen',     'vocal',     'vodka',     'vogue',     'voice',     'voila',     'vomit',
    'voter',     'vouch',     'vowel',     'vying',     'wacky',     'wafer',     'wager',     'wagon',
    'waist',     'waive',     'waltz',     'warty',     'waste',     'watch',     'water',     'waver',
    'waxen',     'weary',     'weave',     'wedge',     'weedy',     'weigh',     'weird',     'welch',
    'welsh',     'whack',     'whale',     'wharf',     'wheat',     'wheel',     'whelp',     'where',
    'which',     'whiff',     'while',     'whine',     'whiny',     'whirl',     'whisk',     'white',
    'whole',     'whoop',     'whose',     'widen',     'wider',     'widow',     'width',     'wield',
    'wight',     'willy',     'wimpy',     'wince',     'winch',     'windy',     'wiser',     'wispy',
    'witch',     'witty',     'woken',     'woman',     'women',     'woody',     'wooer',     'wooly',
    'woozy',     'wordy',     'world',     'worry',     'worse',     'worst',     'worth',     'would',
    'wound',     'woven',     'wrack',     'wrath',     'wreak',     'wreck',     'wrest',     'wring',
    'wrist',     'write',     'wrong',     'wrote',     'wrung',     'wryly',     'yacht',     'yearn',
    'yeast',     'yield',     'yodel',     'young',     'youth',     'yucca',     'zebra',     'zesty',     'zonal']
    return word_list

if __name__ == "__main__":
    main()
