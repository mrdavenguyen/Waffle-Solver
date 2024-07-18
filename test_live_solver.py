from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dictionary import dictionary
import time


def main():
    #options for headless mode
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    
    actions = ActionChains(driver)
    
    driver.get("https://wafflegame.net/archive")
    driver.implicitly_wait(3)
    #waits until the data is displayed and visible on the screen
    items = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'stat-row__val')))

    for item in items:
        #there are a few blanks here, data that isn't actually visible in the current vew and thus empty
        #so I just am looking to grab the first non-blank element and strip out just the max puzzle count and stores it
        if item.text != "":
            #strips the txt from a value of '0 / 899 (0%)' ->  '899'
            num_puzzles = int(item.text.rsplit("/ ")[1].rsplit(" (")[0])
            break

    for i in range(1, num_puzzles + 1):
        scroll_to_puzzle(driver, i)
        tile_data_list = scrape_tiles(driver)
        # for tile_data in tile_data_list:
        #     print_debug(f"{tile_data},")
            
            
        puzzle_data = tile_data_list

        tile_data = build_tile_data(puzzle_data)

        board_layout = build_board(tile_data)
            
        intersections = build_line_intersections()

        build_letter_pools(tile_data, intersections, board_layout)

        word_pools = build_word_pools()

        word_pools = fill_starting_word_pool(word_pools, board_layout, tile_data)

        word_pools = words_with_greens(word_pools, board_layout, tile_data)

        complete = True
        
        for line in word_pools:
            if len(word_pools[line]) == 0:
                complete = False
                break
        
        for line in word_pools:
            print_debug(f"{line} - {word_pools[line]}")
            print_debug(f"")
        
        for tile in tile_data:
            print_debug(f"{tile} - {tile_data[tile]["swap_options"]}")
            print_debug(f"")
        
        if complete:
    
            print_debug(f"Puzzle {i} complete.")
        else:
            print_debug(f"Puzzle {i} failed. ")
                
        
        #clicks the back button to return to the archive menu
        driver.find_element(By.CSS_SELECTOR, "button.button--back.icon-button").click()

def print_debug(text):
    with open("puzzle_troubleshooting.txt", "a") as myfile:
        myfile.write(f"{text}\n")
    myfile.close()

def scrape_tiles(driver: webdriver) -> list:
    """
    Pre-Condition: Puzzle to be scraped will be loaded on screen
    Post-Condition: Data for all the current letter tiles will be returned
    ---------------
    This function will grab all the elements on screen that correlate with the letter tiles that are present on the current board.
    It will grab some data from each tile: the letter in plain text between the <div></div>, the color from the class name, and
    the position as notated by an attribute called "data-pos". Then the data for the board is returned as a list of dictionaries. 
    """
    tiles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class^='tile draggable tile']")))
    count = 0
    tile_data = []

    for tile in tiles:
        letter = tile.text
        position = tile.get_attribute('data-pos')
        classes = tile.get_attribute('class').split()
        color = None

        if 'green' in classes:
            color = 'green'
        elif 'yellow' in classes:
            color = 'yellow'
        
        tile_data.append({
            'letter': letter,
            'color': color,
            'position': position
        })

        count += 1
        if count == 21:
            break

    return tile_data

def scroll_to_puzzle(driver: webdriver, puzzle_number: int) -> None:
    """
    Pre-Condition: The web page will be in the archive menu and a puzzle to be selected is known and provided
    Post-Contition: The puzzle board for the current puzzle will have been loaded to the screen.
    ---------------
    This function is going to move the menu archive to the next puzzle in the list and open it for interaction with other functions
    """
    item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[@data-id='{puzzle_number}']")))
    driver.execute_script("arguments[0].scrollIntoView();", item)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[@data-id='{puzzle_number}']"))).click()

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
            
            print_debug(f"Tile {tile_position}: has a letter {current_tile["letter"]}: can be place {tiles_to_populate}")
        
            for possible_tile in tiles_to_populate:
                if tile_data[possible_tile]["color"] == "green":
                    tiles_to_remove.append(possible_tile)
                    
                if tile_data[possible_tile]["color"] == None or tile_data[possible_tile]["color"] == "yellow":
                    if tile_data[possible_tile]["letter"] == current_tile["letter"]:
                        tiles_to_remove.append(possible_tile)
                        
        print_debug(f"Tile {tile_position}: has a letter {current_tile["letter"]}: will be removed from {tiles_to_remove}")
        
        for tile_ in tiles_to_remove:
            tiles_to_populate.remove(tile_)

        for tile_ in tiles_to_populate:
            if tile_data[tile_position]["letter"] not in tile_data[tile_]["swap_options"]:
                tile_data[tile_]["swap_options"].append(tile_data[tile_position]["letter"])
                print_debug(f"Adding {tile_data[tile_position]["letter"]} to {tile_} - {tile_data[tile_]}'s swap_options")
            
        # for tile_ in tiles_to_populate:
        #     if tile_data[tile_]["letter"] not in tile_data[tile_position]["swap_options"]:
        #         tile_data[tile_position]["swap_options"].append(tile_data[tile_]["letter"])
        #         print_debug(f"Adding {tile_data[tile_]["letter"]} to {tile_position} - {tile_data[tile_position]}'s swap_options")
                
                
        print_debug(f"Tile {tile_position}: has a letter {current_tile["letter"]}: final destinations should be {tiles_to_populate}")
        print_debug("")
    
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

def already_white_in_line(line: list, current_tile: dict) -> bool:
    """
    This function takes a line list that contains all tiles in the line and checks if the letter already exists as a white tile in that line
    """
    for tile in line:
        if tile["letter"] == current_tile["letter"] and tile["color"] == None:
            return True
    return False
            
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
                                    
                # print(f"{index_in_word} - letter in position {word[index_in_word]} from word {word} - current tile word pool {current_tile["swap_options"]}")
                
                
                
                
                # # print_debug(f"Checking if {word[index_in_word]} in {current_tile["swap_options"]}")
                # if word[index_in_word] not in current_tile["swap_options"]:
                #     if word in temp_word_list:
                #         temp_word_list.remove(word)
                #     continue
                # temp_word_list.append(word)
            
        
        # print(f"For line {line}, temp_word_list = {temp_word_list}")
                
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
    
    # for line, tile_data in lines.items():

    #     if tile_data[0]["color"] == "green": #first letter of word is known
    #         word_pools[line] = dictionary[tile_data[0]["letter"]] #load only the word list for the known letter
    #     else:
    #         word_starting_letters = []
    #         for letter in letter_pools[line]: #loops through all the possible letters for this line
    #             if letter not in word_starting_letters: #ensures there is no duplicate letters, which would result in 
    #                 word_starting_letters.append(letter)
                    
    #         if tile_data[0]["color"] == "yellow": #first letter is possible in the current line's word, but NOT in the first position (word can't start with this letter)
    #             word_starting_letters.remove(tile_data[0]["letter"]) #removes this yellow letter
                
    #         for letter in word_starting_letters:
    #             for word in dictionary[letter]:
    #                 word_pools[line].append(word)
                    
    # return word_pools
    
def remove_impossible_words(word_pools: dict, line_mapping: dict, tile_data: dict):

    pass

def determine_swappable_tiles():
    pass    
    
def swap_options_debug(tile_data):
    for tile in tile_data:
        print_debug(f"{tile} - {tile_data[tile]["swap_options"]}")
#sample code to test results   
    open('errorlog.txt', 'w').close()



if __name__ == '__main__':
    main()
