from dictionary import dictionary
import copy

NUM_BOXES = 21

def main():
    

    # create a data structure to store all letter "boxes":
    boxes = {}
    for i in range(NUM_BOXES):
        boxes[i] = {}
        boxes[i]['letter'] = None
        boxes[i]['prev_letter'] = None
        boxes[i]['color'] = None
        boxes[i]['prev_color'] = None
        boxes[i]['row'] = None
        boxes[i]['column'] = None

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
   
    # create a data structure to store the lists of yellow and white letters in each row and column
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
    # create list of all white letters in puzzle
    white_letters = []
    for i in range(len(boxes)):
        if boxes[i]['color'] == 'white':
            white_letters.append(copy.deepcopy(boxes[i]))

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


    solutions = []
    solve_waffle(boxes, rows, columns, white_letters, word_list, solutions)
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

def solve_waffle(boxes, rows, columns, white_letters, word_list, solutions, line_index = 0, letter_index = 0):
    if line_index == 6:
        solutions.append([])
        for i in range(len(boxes)):
            solutions[-1].append(boxes[i]['letter'])
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
        # try and swap with yellow letters from the same line and check if it makes valid word
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
                if line_ornts_1[line_index % 3]['yellow'][box][line_ornt_2] != None:
                    line_3 = line_ornts_1[line_index % 3]['yellow'][box][line_ornt_2]
                    yellow_keys = list(line_ornts_2[line_3]['yellow'].keys())
                    for box_2 in yellow_keys:
                        # if the box that's in the perpendicular line is the same as the yellow box in this line, remove it
                        if line_ornts_2[line_3]['yellow'][box_2] == line_ornts_1[line_index % 3]['yellow'][box]:
                            pos_3 = box_2
                            temp_3 = line_ornts_2[line_3]['yellow'].pop(pos_3)
                            break
                # remove the box from the yellow letter list
                temp = line_ornts_1[line_index % 3]['yellow'].pop(box)
                # waffle puzzle archive #138 exception
                # if current letter is intersectional, and the perpendicular line's yellow letter list contains this letter, remove the letter from that list as well
                temp_2 = None
                pos_2 = None
                line_2 = None
                if line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2] != None:
                    line_2 = line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2]
                    yellow_keys = list(line_ornts_2[line_2]['yellow'].keys())
                    for box_2 in yellow_keys:
                        if line_ornts_2[line_2]['yellow'][box_2]['letter'] == line_ornts_1[line_index % 3]['boxes'][letter_index]['letter']:
                            pos_2 = box_2
                            temp_2 = line_ornts_2[line_2]['yellow'].pop(pos_2)
                            break
                # check if valid word can be made with this letter
                if makes_valid_word(boxes, rows, columns, line_index, word_list):
                    next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
                    solve_waffle(boxes, rows, columns, white_letters, word_list, solutions, next_line_index, next_letter_index)
                # return box to yellow letter list
                line_ornts_1[line_index % 3]['yellow'][box] = temp
                # return other box to perpendicular yellow list if it was removed
                if temp_2 != None:
                    line_ornts_2[line_2]['yellow'][pos_2] = temp_2
                if temp_3 != None:
                    line_ornts_2[line_3]['yellow'][pos_3] = temp_3
                line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = None
                line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color']
                line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = None
        # try and swap with yellow letters from a perpendicular line and check if it makes valid word
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
                    # remove the box from the yellow letter list
                    temp = line_ornts_2[line]['yellow'].pop(box)
                    if makes_valid_word(boxes, rows, columns, line_index, word_list):
                        next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
                        solve_waffle(boxes, rows, columns, white_letters, word_list, solutions, next_line_index, next_letter_index)
                    line_ornts_2[line]['yellow'][box] = temp
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter']
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = None
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color']
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = None
        # try and swap with white letters from other lines and check if it makes valid word
        for box in range(len(white_letters)):
            # white letter isn't in the same row as current letter
            if white_letters[box][line_ornt_1] != line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_1]:
                # white letter isn't in an intersecting column CHECK THE LOGIC OF THIS!!! (not the case that current box is in a column and column number is same as white letter's column number)
                if not (line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2] != None and white_letters[box][line_ornt_2] == line_ornts_1[line_index % 3]['boxes'][letter_index][line_ornt_2]):
                    # save what the current letter and color are and change current box to the white letter
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['letter']
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['color']
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = white_letters[box]['letter']
                    # assume that the letter is correct and make it green
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = 'green'
                    # remove the box from the white letter list
                    temp = white_letters.pop(box)
                    if makes_valid_word(boxes, rows, columns, line_index, word_list):
                        next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
                        solve_waffle(boxes, rows, columns, white_letters, word_list, solutions, next_line_index, next_letter_index)
                    white_letters.insert(box, temp)
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['letter'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter']
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_letter'] = None
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['color'] = line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color']
                    line_ornts_1[line_index % 3]['boxes'][letter_index]['prev_color'] = None
    else:
        next_line_index, next_letter_index = increment_indexes(line_index, letter_index)
        solve_waffle(boxes, rows, columns, white_letters, word_list, solutions, next_line_index, next_letter_index)
    return

def increment_indexes(line_index, letter_index):
    letter_index += 1
    if letter_index == 5:
        line_index += 1
        letter_index = 0
    return line_index, letter_index

def makes_valid_word(boxes, rows, columns, line_index, word_list):
    green_letters = {}
    yellow_letters = {}
    line_white_letters = {}
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

    for word in word_list:
        current_word = word
        valid = True
        for pos, letter in green_letters.items():
            if current_word[pos] != letter:
                valid = False
                break
            else:
                temp_word = list(current_word)
                temp_word[pos] = temp_word[pos].upper()
                current_word = "".join(temp_word)
        if valid:
            for pos in yellow_letters:
                letter = yellow_letters[pos]['letter']
                if line_index < 3:
                    if yellow_letters[pos]['column'] == None:
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
                else:
                    if yellow_letters[pos]['row'] == None:
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
            if valid:
                for pos, letter in line_white_letters.items():
                    if letter in current_word:
                        valid = False
                        break
                if valid:
                    print("line:", line_index, "word:", current_word)
                    return True
    return False

if __name__ == "__main__":
    main()
