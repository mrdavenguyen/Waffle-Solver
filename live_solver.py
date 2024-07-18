from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dictionary import dictionary
from copy import copy
import time

#puzzle # 5
puzzle_sample_5 = [
    {'letter': 'C', 'color': 'green', 'position': '{"x":0,"y":0}'},
    {'letter': 'R', 'color': 'green', 'position': '{"x":1,"y":0}'},
    {'letter': 'M', 'color': None, 'position': '{"x":2,"y":0}'},
    {'letter': 'V', 'color': None, 'position': '{"x":3,"y":0}'},
    {'letter': 'P', 'color': 'green', 'position': '{"x":4,"y":0}'},
    {'letter': 'E', 'color': None, 'position': '{"x":0,"y":1}'},
    {'letter': 'R', 'color': None, 'position': '{"x":2,"y":1}'},
    {'letter': 'G', 'color': 'yellow', 'position': '{"x":4,"y":1}'},
    {'letter': 'L', 'color': 'yellow', 'position': '{"x":0,"y":2}'},
    {'letter': 'A', 'color': None, 'position': '{"x":1,"y":2}'},
    {'letter': 'I', 'color': 'green', 'position': '{"x":2,"y":2}'},
    {'letter': 'V', 'color': None, 'position': '{"x":3,"y":2}'},
    {'letter': 'Y', 'color': 'yellow', 'position': '{"x":4,"y":2}'},
    {'letter': 'E', 'color': None, 'position': '{"x":0,"y":3}'},
    {'letter': 'N', 'color': None, 'position': '{"x":2,"y":3}'},
    {'letter': 'B', 'color': None, 'position': '{"x":4,"y":3}'},
    {'letter': 'E', 'color': 'green', 'position': '{"x":0,"y":4}'},
    {'letter': 'L', 'color': None, 'position': '{"x":1,"y":4}'},
    {'letter': 'O', 'color': 'yellow', 'position': '{"x":2,"y":4}'},
    {'letter': 'U', 'color': None, 'position': '{"x":3,"y":4}'},
    {'letter': 'Y', 'color': 'green', 'position': '{"x":4,"y":4}'}
]

#puzzle #3
puzzle_sample_3 = [
    {'letter': 'S', 'color': 'green', 'position': '{"x":0,"y":0}'},
    {'letter': 'P', 'color': 'green', 'position': '{"x":1,"y":0}'},
    {'letter': 'E', 'color': 'green', 'position': '{"x":2,"y":0}'},
    {'letter': 'E', 'color': None, 'position': '{"x":3,"y":0}'},
    {'letter': 'D', 'color': 'green', 'position': '{"x":4,"y":0}'},
    {'letter': 'A', 'color': None, 'position': '{"x":0,"y":1}'},
    {'letter': 'T', 'color': None, 'position': '{"x":2,"y":1}'},
    {'letter': 'P', 'color': 'yellow', 'position': '{"x":4,"y":1}'},
    {'letter': 'T', 'color': 'yellow', 'position': '{"x":0,"y":2}'},
    {'letter': 'O', 'color': None, 'position': '{"x":1,"y":2}'},
    {'letter': 'C', 'color': 'green', 'position': '{"x":2,"y":2}'},
    {'letter': 'I', 'color': None, 'position': '{"x":3,"y":2}'},
    {'letter': 'R', 'color': 'yellow', 'position': '{"x":4,"y":2}'},
    {'letter': 'N', 'color': None, 'position': '{"x":0,"y":3}'},
    {'letter': 'E', 'color': 'green', 'position': '{"x":2,"y":3}'},
    {'letter': 'M', 'color': None, 'position': '{"x":4,"y":3}'},
    {'letter': 'P', 'color': 'green', 'position': '{"x":0,"y":4}'},
    {'letter': 'E', 'color': 'yellow', 'position': '{"x":1,"y":4}'},
    {'letter': 'I', 'color': 'yellow', 'position': '{"x":2,"y":4}'},
    {'letter': 'E', 'color': None, 'position': '{"x":3,"y":4}'},
    {'letter': 'Y', 'color': 'green', 'position': '{"x":4,"y":4}'}
]

#puzzle #4
puzzle_sample_4 = [
    {'letter': 'N', 'color': 'green', 'position': '{"x":0,"y":0}'},
    {'letter': 'D', 'color': 'yellow', 'position': '{"x":1,"y":0}'},
    {'letter': 'E', 'color': 'green', 'position': '{"x":2,"y":0}'},
    {'letter': 'E', 'color': 'yellow', 'position': '{"x":3,"y":0}'},
    {'letter': 'Y', 'color': 'green', 'position': '{"x":4,"y":0}'},
    {'letter': 'E', 'color': 'yellow', 'position': '{"x":0,"y":1}'},
    {'letter': 'E', 'color': 'yellow', 'position': '{"x":2,"y":1}'},
    {'letter': 'L', 'color': None, 'position': '{"x":4,"y":1}'},
    {'letter': 'T', 'color': None, 'position': '{"x":0,"y":2}'},
    {'letter': 'R', 'color': None, 'position': '{"x":1,"y":2}'},
    {'letter': 'A', 'color': 'green', 'position': '{"x":2,"y":2}'},
    {'letter': 'E', 'color': None, 'position': '{"x":3,"y":2}'},
    {'letter': 'C', 'color': 'yellow', 'position': '{"x":4,"y":2}'},
    {'letter': 'K', 'color': 'yellow', 'position': '{"x":0,"y":3}'},
    {'letter': 'A', 'color': None, 'position': '{"x":2,"y":3}'},
    {'letter': 'I', 'color': 'yellow', 'position': '{"x":4,"y":3}'},
    {'letter': 'D', 'color': 'green', 'position': '{"x":0,"y":4}'},
    {'letter': 'N', 'color': None, 'position': '{"x":1,"y":4}'},
    {'letter': 'S', 'color': 'yellow', 'position': '{"x":2,"y":4}'},
    {'letter': 'K', 'color': None, 'position': '{"x":3,"y":4}'},
    {'letter': 'S', 'color': 'green', 'position': '{"x":4,"y":4}'},
]

puzzle_sample_906 = [
    {'letter': 'I', 'color': 'green', 'position': '{"x":0,"y":0}'},
    {'letter': 'N', 'color': None, 'position': '{"x":1,"y":0}'},
    {'letter': 'R', 'color': 'yellow', 'position': '{"x":2,"y":0}'},
    {'letter': 'R', 'color': None, 'position': '{"x":3,"y":0}'},
    {'letter': 'E', 'color': 'green', 'position': '{"x":4,"y":0}'},
    {'letter': 'O', 'color': None, 'position': '{"x":0,"y":1}'},
    {'letter': 'U', 'color': None, 'position': '{"x":2,"y":1}'},
    {'letter': 'T', 'color': None, 'position': '{"x":4,"y":1}'},
    {'letter': 'R', 'color': 'yellow', 'position': '{"x":0,"y":2}'},
    {'letter': 'N', 'color': None, 'position': '{"x":1,"y":2}'},
    {'letter': 'I', 'color': 'green', 'position': '{"x":2,"y":2}'},
    {'letter': 'E', 'color': None, 'position': '{"x":3,"y":2}'},
    {'letter': 'O', 'color': 'yellow', 'position': '{"x":4,"y":2}'},
    {'letter': 'L', 'color': None, 'position': '{"x":0,"y":3}'},
    {'letter': 'R', 'color': None, 'position': '{"x":2,"y":3}'},
    {'letter': 'P', 'color': None, 'position': '{"x":4,"y":3}'},
    {'letter': 'T', 'color': 'green', 'position': '{"x":0,"y":4}'},
    {'letter': 'O', 'color': 'yellow', 'position': '{"x":1,"y":4}'},
    {'letter': 'A', 'color': 'yellow', 'position': '{"x":2,"y":4}'},
    {'letter': 'E', 'color': 'yellow', 'position': '{"x":3,"y":4}'},
    {'letter': 'R', 'color': 'green', 'position': '{"x":4,"y":4}'},
]

puzzle_sample_905 = [
    {'letter': 'T', 'color': 'green', 'position': '{"x":0,"y":0}'},
    {'letter': 'V', 'color': None, 'position': '{"x":1,"y":0}'},
    {'letter': 'O', 'color': 'green', 'position': '{"x":2,"y":0}'},
    {'letter': 'P', 'color': None, 'position': '{"x":3,"y":0}'},
    {'letter': 'L', 'color': 'green', 'position': '{"x":4,"y":0}'},
    {'letter': 'S', 'color': None, 'position': '{"x":0,"y":1}'},
    {'letter': 'R', 'color': 'yellow', 'position': '{"x":2,"y":1}'},
    {'letter': 'M', 'color': 'yellow', 'position': '{"x":4,"y":1}'},
    {'letter': 'I', 'color': None, 'position': '{"x":0,"y":2}'},
    {'letter': 'L', 'color': 'yellow', 'position': '{"x":1,"y":2}'},
    {'letter': 'A', 'color': 'green', 'position': '{"x":2,"y":2}'},
    {'letter': 'P', 'color': 'yellow', 'position': '{"x":3,"y":2}'},
    {'letter': 'R', 'color': None, 'position': '{"x":4,"y":2}'},
    {'letter': 'I', 'color': 'green', 'position': '{"x":0,"y":3}'},
    {'letter': 'O', 'color': None, 'position': '{"x":2,"y":3}'},
    {'letter': 'Y', 'color': None, 'position': '{"x":4,"y":3}'},
    {'letter': 'C', 'color': 'green', 'position': '{"x":0,"y":4}'},
    {'letter': 'L', 'color': None, 'position': '{"x":1,"y":4}'},
    {'letter': 'I', 'color': None, 'position': '{"x":2,"y":4}'},
    {'letter': 'R', 'color': 'yellow', 'position': '{"x":3,"y":4}'},
    {'letter': 'T', 'color': 'green', 'position': '{"x":4,"y":4}'},
]

puzzle_sample_904 = [
{'letter': 'C', 'color': 'green', 'position': '{"x":0,"y":0}'},
{'letter': 'N', 'color': None, 'position': '{"x":1,"y":0}'},
{'letter': 'S', 'color': None, 'position': '{"x":2,"y":0}'},
{'letter': 'U', 'color': None, 'position': '{"x":3,"y":0}'},
{'letter': 'N', 'color': 'green', 'position': '{"x":4,"y":0}'},
{'letter': 'O', 'color': None, 'position': '{"x":0,"y":1}'},
{'letter': 'E', 'color': 'green', 'position': '{"x":2,"y":1}'},
{'letter': 'O', 'color': None, 'position': '{"x":4,"y":1}'},
{'letter': 'L', 'color': 'yellow', 'position': '{"x":0,"y":2}'},
{'letter': 'I', 'color': 'yellow', 'position': '{"x":1,"y":2}'},
{'letter': 'M', 'color': 'green', 'position': '{"x":2,"y":2}'},
{'letter': 'A', 'color': 'yellow', 'position': '{"x":3,"y":2}'},
{'letter': 'U', 'color': 'yellow', 'position': '{"x":4,"y":2}'},
{'letter': 'T', 'color': None, 'position': '{"x":0,"y":3}'},
{'letter': 'O', 'color': 'green', 'position': '{"x":2,"y":3}'},
{'letter': 'L', 'color': None, 'position': '{"x":4,"y":3}'},
{'letter': 'H', 'color': 'green', 'position': '{"x":0,"y":4}'},
{'letter': 'T', 'color': None, 'position': '{"x":1,"y":4}'},
{'letter': 'K', 'color': 'yellow', 'position': '{"x":2,"y":4}'},
{'letter': 'D', 'color': None, 'position': '{"x":3,"y":4}'},
{'letter': 'Y', 'color': 'green', 'position': '{"x":4,"y":4}'},
]

def build_tile_data(puzzle_data) -> dict:
    """
    [ 0,  1,  2,  3,  4],
    [ 5,  6,  7,  8,  9],
    [10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24]
    """

    tile_data = {}
    offset = 0
    
    for i in range(25):
        if i in [6, 8 , 16 , 18]:
            offset -=1
            continue
        else:
            tile_data[i] = {
                "letter" : puzzle_data[i + offset]["letter"],
                "color" : puzzle_data[i + offset]["color"],
                "position" : None,
                "row" : None,
                "col" : None,
                "swap_options" : [],
                "evaluated" : False
            }
            postition_data = puzzle_data[i + offset]["position"]
            positions = postition_data.strip('{}').split(',')
            tile_data[i]["position"] = {key_value.split(':')[0].strip('"'): int(key_value.split(':')[1]) for key_value in positions}
            
            if tile_data[i]["position"]["y"] % 2 == 0:
                tile_data[i]["row"] = f"row_{tile_data[i]["position"]["y"] // 2}"
            if tile_data[i]["position"]["x"] % 2 == 0:
                tile_data[i]["col"] = f"col_{tile_data[i]["position"]["x"] // 2}"

    return tile_data

def build_board(tile_data: dict) -> list:
    """
    ------------
    This function will take a the list "tile_data" that contains dictionaries for each tile.
    The index of each dictionary corresponds to the order the tile appears on the board.
    Current line could be either a row or column. Each dict contains the letter, color, and position of the tile.
    It will return a dictionary of lists containing "tile_data" for each line.
        c0  c1  c2      
         |   |   |
    r0 - F U G U E          
         O   L   N
    r1 - L O O S E
         I   B   M
    r2 - O M E G A 
    """
    lines = {
        "row_0" : [0, 1, 2, 3, 4],
        "row_1" : [10, 11, 12, 13, 14],
        "row_2" : [20, 21, 22, 23, 24],
        "col_0" : [0, 5, 10, 15, 20],
        "col_1" : [2, 7, 12, 17, 22],
        "col_2" : [4, 9, 14, 19, 24]
    }
    
    return lines

def build_line_intersections() -> dict:
    """
    ------------
    This function will build and return a dictionary that contains intersection data for
    a row and a col. This can be used to determine which line shares letter pools for
    intersections at the given index
    """
    intersections = {
        "row" : {
            0 : "col_0",
            2 : "col_1",
            4 : "col_2"
        },
        "col" : {
            0 : "row_0",
            2 : "row_1",
            4 : "row_2"
        }
    }
    
    return intersections

def build_letter_pools(tile_data: dict, intersections: dict, board_layout: dict) -> dict:
    """
    This fucntion will take a dictionary of the lines and build a letter pool for each line.
    This is achieved by taking each line, evaluating it's current color and then populating the lines
    appropriately if it's yellow or white, dependent upon the index of that letter. It's then stored in the dictionary and returned.
    """
        
    for tile in tile_data:
        tiles_to_populate = []
        tile_position = tile
        current_tile = tile_data[tile]
        
        tiles_to_remove = []
              
        if current_tile["color"] == "yellow" or current_tile["color"] == None:
            tiles_to_populate = determine_letter_pool_allocation(tile_position, current_tile, intersections, board_layout)
            
            # print_debug(f"Tile {tile_position}: has a letter {current_tile["letter"]}: can be place {tiles_to_populate}")
        
            for possible_tile in tiles_to_populate:
                if tile_data[possible_tile]["color"] == "green":
                    tiles_to_remove.append(possible_tile)
                    
                if tile_data[possible_tile]["color"] == None or tile_data[possible_tile]["color"] == "yellow":
                    if tile_data[possible_tile]["letter"] == current_tile["letter"]:
                        tiles_to_remove.append(possible_tile)
                        
        # print_debug(f"Tile {tile_position}: has a letter {current_tile["letter"]}: will be removed from {tiles_to_remove}")
        
        for tile_ in tiles_to_remove:
            tiles_to_populate.remove(tile_)

        for tile_ in tiles_to_populate:
            if tile_data[tile_position]["letter"] not in tile_data[tile_]["swap_options"]:
                tile_data[tile_]["swap_options"].append(tile_data[tile_position]["letter"])
                # print_debug(f"Adding {tile_data[tile_position]["letter"]} to {tile_} - {tile_data[tile_]}'s swap_options")
            
        # for tile_ in tiles_to_populate:
        #     if tile_data[tile_]["letter"] not in tile_data[tile_position]["swap_options"]:
        #         tile_data[tile_position]["swap_options"].append(tile_data[tile_]["letter"])
        #         print_debug(f"Adding {tile_data[tile_]["letter"]} to {tile_position} - {tile_data[tile_position]}'s swap_options")
                
                
        # print_debug(f"Tile {tile_position}: has a letter {current_tile["letter"]}: final destinations should be {tiles_to_populate}")
        # print_debug("")
    
def build_word_pools():
    """
    This function will take all the lines and thier letter pools and loop through them.
    It will add from the dictionary of words, any word that could be a starting word based on
    the starting status of the line during the first scrape.
    """
    
    word_pools = {
        "row_0" : [],
        "row_1" : [],
        "row_2" : [],
        "col_0" : [],
        "col_1" : [],
        "col_2" : []
    } 
        
    return word_pools 
        
def determine_letter_pool_allocation(tile_position, current_tile, intersections, board_layout) -> list:
    """
    This function will take a tile and based off index in current line, color, and intersections, return
    a list of lines that this tile's letter can be added to it's pool of letter options.
    
    Index 0, 2, 4:
    --------------
    Yellow = Letter poshsible in eiter current line or line intersection only. 
    Grey = Letter not in current line or line intersection at index. All other lines possible
    
    
    Index 1, 3:
    -------------
    Yellow = Letter in current line only.
    Grey = Letter not in current line, or start or ending intersection
    
    """
    positions = [i for i in range(25) if i not in [6, 8, 16, 18]]
    
    tile_position = tile_position
    color = current_tile["color"]
    
    relational_positions = []
    
    for row_or_col in board_layout: #loops through the lines of the board
        current_line = board_layout[row_or_col]
        
        if tile_position in current_line: #if this tile in in the line (row or col)
            for position in current_line: #loops through every tile in lineSoo
                if color == "yellow":
                    if position != tile_position: #if not the current tile, then add it to related positions
                        relational_positions.append(position)
                else: #white
                    if position in positions: #removes any related tile in current line or intersections
                        positions.remove(position)
                        
    if color != "yellow":
        relational_positions = positions        
    
    return relational_positions           
            
def tile_swap(actions: ActionChains, driver: webdriver, source_pos: str, target_pos: str) -> None:
    """
    Pre-Condition: Known tiles to be swapped will be provided, order is irrelevant
    Post-Condition: Tiles will be swapped on screen
    ---------------
    This function is provided the "data-pos" value of two tiles (as well as the WebDriver and ActionChain objects)
    and simply swaps their locations on screen. 
    """
    source_tile_pos = driver.find_element(By.CSS_SELECTOR, f"[data-pos='{source_pos}']")
    target_tile_pos = driver.find_element(By.CSS_SELECTOR, f"[data-pos='{target_pos}']")
    actions.drag_and_drop(source_tile_pos, target_tile_pos).perform()
    
def find_possible_words(lines: dict, letter_pools: list) -> None:
    """
    This function will use some sub-functions to build a starting word list
    """
    
    find_words_with_yellows(lines, word_pools)
    
    remove_words_with_bad_letters(lines, letter_pools, word_pools)                
    
    #check every line
     #check index in line
      #if letter is green at index,
       #remove all words that don't have letter at index
      #else
    
    
    return word_pools

def words_with_greens(word_pools: dict, line_mapping: dict, tile_data: dict) -> None:
    """
    This function will run through the possible word pool for each line and update it to only contain
    words that match the expected green positions for each line.
    """
    
    for line in line_mapping:
        temp_word_list = []
        tile_positions = line_mapping[line]
        
        for word in word_pools[line]:
            valid_word = False
            for index, letter in enumerate(word):
                current_tile = tile_data[tile_positions[index]]
                
                if current_tile["color"] == "green":
                    if letter != current_tile["letter"]:
                        valid_word = False
                        break #move to next word
                    else:
                        valid_word = True
                        continue          
                        
                if letter not in current_tile["swap_options"]:
                    valid_word = False
                    break #move to next word
                else:
                    valid_word = True
                    continue  
            
            if valid_word and word not in temp_word_list:
                temp_word_list.append(word)
                                          
        word_pools[line] = temp_word_list
        
    return word_pools                    
                
def word_contains_swap_options(tile: dict, word: str):
    for letter in word:
        if letter not in tile["swap_options"]:
            return False
    return True
                
def find_words_with_required_yellows(lines: dict, word_pools: dict) -> None:
    """
    This function will take the word pool and reduce it to only words that:
    contain known good yellows in the current line (yellows in index 1 or 3 HAVE to be in word)
    don't contain the yellows in the current bad position (words with yellow letters in matching position CANNOT be valid)
    """
    required_indexes = [1, 3]
    
    for line in lines.keys(): #will loops through all row and col
        
        known_greens = [] #will hold tuples of (index, letter) for each known green
        required_yellows = [] #will hold tuples of (index, letter) for each known yellow
        
        for index, tile in enumerate(lines[line]): #will loops through all the tiles for the current line
            if tile["color"] == "green": 
                known_greens.append((index, tile["letter"].lower())) #adds green indexes to the indexes to verify
            if tile["color"] == "yellow" and index in required_indexes: #if tile is yellow and required to be in the word 
                required_yellows.append((index, tile["letter"].lower())) #adds yellow indexes to the indexes to verify
                             
        if len(required_yellows) == 0:
            continue
        
        words_with_required_yellows = []
        
        for word in word_pools[line]: #will loop through word pool for the current line
            for yellow in required_yellows:
                required_letter = yellow[1]
                wrong_position = yellow[0]
                if required_letter not in word or word[wrong_position] == required_letter: #word contain the yellow letter in the known wrong place (because it's yellow) or is not present
                    valid_word = False
                    break
                else:
                    valid_word = True
                    
            if valid_word:
                words_with_required_yellows.append(word)
        
        word_pools[line] = words_with_required_yellows

def remove_words_with_wrong_yellows(lines: dict, word_pools: dict) -> None:
    """
    This code will run through the yellow letters in the indexes that are't required
    and remove any words that have letters matching these indexes
    """
    
    optional_indexes = [2, 4]
    
    for line in lines.keys(): #will loops through all row and col
    
        potential_yellows = [] #will hold tuples of (index, letter) for each known yellow
        
        for index, tile in enumerate(lines[line]): #will loops through all the tiles for the current line
            if tile["color"] == "yellow" and index in optional_indexes: #if tile is yellow and required to be in the word 
                potential_yellows.append((index, tile["letter"].lower())) #adds yellow indexes to the indexes to verify

        if len(potential_yellows) == 0:
            continue
        
        words_without_wrong_index_yellows = []
        
        for word in word_pools[line]: #will loop through word pool for the current line
            valid_word = False
            
            for yellow in potential_yellows:
                potnetial_letter = yellow[1]
                wrong_postion = yellow[0]
                
                if word[wrong_postion] == potnetial_letter: #word contain the yellow letter in the known wrong place (because it's yellow)
                    valid_word = False
                    break #breaks the index searching and moves to next word
                else:
                    valid_word = True

            if valid_word:
                words_without_wrong_index_yellows.append(word)
        
        word_pools[line] = words_without_wrong_index_yellows
 
def remove_words_containing_invalid_letters(lines: dict, word_pools, letter_pools)-> None:
    """
    This will remove all words from the word pool that contain letters not available to swap in
    """
    for line in lines.keys():
        valid_letters = []
        valid_letters = copy(letter_pools[line])
        for tile in lines[line]:
            if tile["color"] == "green":
                valid_letters.append(tile["letter"])
        

        words_without_bad_letters = []    
            
        for word in word_pools[line]:
            valid_word = False
            for letter in word:
                if letter.upper() in valid_letters:
                    valid_word = True
                else:
                    print_debug(f"removing {word} - {letter} not in {valid_letters}")
                    valid_word = False
                    break
                
            if valid_word:
                words_without_bad_letters.append(word)
        
        word_pools[line] = words_without_bad_letters
                
def fill_starting_word_pool(word_pools: dict, line_mapping: dict, tile_data: dict) -> None:
    """
    This function will take all the lines and thier letter pools and loop through them.
    It will add from the dictionary of words, any word that could be a starting word based on
    the starting status of the line during the first scrape.
    """
    first_position = 0
    
    for line in line_mapping: #lines row or col
        current_position = line_mapping[line][first_position]
        current_tile = tile_data[current_position]
        
        if current_tile["color"] == "green":
            word_pools[line] = dictionary[current_tile["letter"]]
        else:
            for letter in current_tile["swap_options"]:
                for word in dictionary[letter]:
                    word_pools[line].append(word)
        
    return word_pools        
    
def remove_impossible_words(word_pools: dict, line_mapping: dict, tile_data: dict):

    pass

def determine_swappable_tiles():
    pass    
 
def print_debug(text):
    print(f"DEBUG: {text}")
    with open("errorlog.txt", "a") as myfile:
        myfile.write(f"DEBUG: {text}\n")
    myfile.close()
    
def swap_options_debug(tile_data):
    for tile in tile_data:
        print_debug(f"{tile} - {tile_data[tile]["swap_options"]}")
#sample code to test results   

def main():

    open('errorlog.txt', 'w').close()

    puzzle_data = puzzle_sample_904

    tile_data = build_tile_data(puzzle_data)

    board_layout = build_board(tile_data)
        
    intersections = build_line_intersections()

    build_letter_pools(tile_data, intersections, board_layout)

    word_pools = build_word_pools()

    word_pools = fill_starting_word_pool(word_pools, board_layout, tile_data)

    word_pools = words_with_greens(word_pools, board_layout, tile_data)

    for line in word_pools:
        print_debug(f"{line} - {word_pools[line]}")
        print_debug(f"")

if __name__ == "__main__":
    main() 
    