import copy
import time

def main():
    tiles = []
    for i in range(25):
        tiles.append({
            'letter': None,
            'color': None,
            'row': None,
            'column': None,
            'position': None            
        })
        for j in range(3):
            if (j * 10) + 0 <= i <= (j * 10) + 4:
                tiles[i]['row'] = j

            if (i - (2 * j)) % 5 == 0:
                tiles[i]['column'] = j

    for i in range(5):
        for j in range(5):
            tiles[(i * 5) + j]['position'] = f'{{"x":{j},"y":{i}}}'

    # collect indexes to remove
    indexes_to_remove = [i for i in range(25) if tiles[i]['row'] == None and tiles[i]['column'] == None]

    # remove indexes in reverse order to prevent index errors
    for index in indexes_to_remove[::-1]:
        tiles.pop(index)

    get_user_input(tiles)

    lines = {}
    for i in range(6):
        lines[i] = {}
    for i in range(3):
        for j in range(len(tiles)):
            if tiles[j]['row'] == i:
                lines[i][len(lines[i])] = tiles[j]
    for i in range(3):
        for j in range(len(tiles)):
            if tiles[j]['column'] == i:
                lines[i + 3][len(lines[i + 3])] = tiles[j]
    

    solution = ['sneer', 'aping', 'eagle', 'share', 'eking', 'rogue']
    swaps = []
    swaps_remaining = 15 #scrape the current swaps remaining instead of hard code
    print("Finding best swaps...")
    optimal_swaps = find_optimal_swaps(tiles, solution, lines)
    print(optimal_swaps)
    
def get_user_input(tiles) -> None:
    for i in range(len(tiles)):
        while True:
            letter = input(f"Enter letter (a-z) for tile {i}: ")
            if letter.lower() in 'abcdefghijklmnopqrstuvwxyz' and len(letter) == 1:
                letter = letter.lower()
                break
            else:
                print("Invalid letter, please try again.")

        tiles[i]['letter'] = letter

def find_optimal_swaps(tiles, solution, lines, swaps = None, optimal_swaps = None, swaps_remaining = 15, prev_green_count = None):
    if swaps is None:
        swaps = []
    if optimal_swaps is None:
        optimal_swaps = []
    # update the tile colors
    update_tile_colors(tiles, solution, lines)
    # if all of the tiles are green and this branch of swaps has the least number of swaps, save the list of swaps and return it
    if all_green_tiles(tiles):
        optimal_swaps = save_optimal_swaps(swaps, optimal_swaps)
        return optimal_swaps
    for tile_1_idx in range(1, len(tiles) - 2):
        # if the first tile is green, skip to the first tile's next index
        if tiles[tile_1_idx]['color'] == 'green':
            continue
        for tile_2_idx in range(tile_1_idx + 1, len(tiles) - 1):
            # if the second tile is green, skip to the second tile's next index
            if tiles[tile_2_idx]['color'] == 'green':
                continue
            green_count_before_swap = get_green_count(tiles)
            # swap the letters of both tiles
            swap_pair(tiles, tile_1_idx, tile_2_idx)
            # update the tile colors after the swap and append the swapped tiles color and positions to a list
            update_tile_colors(tiles, solution, lines)
            save_swap(swaps, tiles, tile_1_idx, tile_2_idx)
            green_count_after_swap = get_green_count(tiles)
            # if the current and previous swaps yielded less than two new green tiles in total, flag good_swaps as False
            current_green_count = green_count_after_swap - green_count_before_swap
            good_swaps = True
            # only check if good swaps have been made if it isn't currently the first swap, otherwise there is no previous swap to sum
            if prev_green_count != None:
                if prev_green_count + current_green_count < 2:
                    good_swaps = False
            swaps_remaining -= 1
            # if this branch of swaps is still optimal, continue to the next swap
            if current_branch_is_optimal(tiles, swaps_remaining) and good_swaps:
                # call the function again
                optimal_swaps = find_optimal_swaps(tiles, solution, lines, swaps, optimal_swaps, swaps_remaining, current_green_count)
                # if backtracking and all of the tiles are green already, return the optimal_swaps list
                if all_green_tiles(tiles):
                    return optimal_swaps
            # if backtracking, undo the swap
            swap_pair(tiles, tile_1_idx, tile_2_idx)
            remove_swaps(swaps)
            swaps_remaining += 1
    return optimal_swaps

def get_green_count(tiles):
    # counts the current number of tiles that are currently green and returns it
    green_count = 0
    for tile in tiles:
        if tile['color'] == 'green':
            green_count += 1
    return green_count

def swap_pair(tiles, tile_1_idx, tile_2_idx):
    # takes the index of two tiles and swaps both tiles' "letter" value in the tiles dict
    temp = tiles[tile_1_idx]['letter']
    tiles[tile_1_idx]['letter'] = tiles[tile_2_idx]['letter']
    tiles[tile_2_idx]['letter'] = temp

def save_swap(swaps, tiles, tile_1_idx, tile_2_idx):
    # saves the indexes of the two tiles being swapped to a list and appends it to the swaps list
    tile_1_pos = tiles[tile_1_idx]['position']
    tile_2_pos = tiles[tile_2_idx]['position']
    tile_1_color = tiles[tile_1_idx]['color']
    tile_2_color = tiles[tile_2_idx]['color']
    swap = {
        'positions': [tile_1_pos, tile_2_pos],
        'expected_colors': [tile_1_color, tile_2_color]
    }
    swaps.append(swap)

def remove_swaps(swaps):
    # removes the most recent swaps from the swaps list
    swaps.pop()

def current_branch_is_optimal(tiles, swaps_remaining):
    """ 
    check if it's possible for the current branch of swaps to produce an optimal solution.
    an optimal solution is where five or more swaps are remaining, so we subtract five from the current remaining swaps to ascertain how many
    swaps remain if this is to be an optimal solution. as the greatest number of tiles that can be converted to green in one swap is two,
    we multiply the remaining swaps by two to get the maximum number of tiles that can be converted to green if
    the current branch of swaps continues. if this number is greater than or equal to the number of non-green tiles remaining in the puzzle, then an optimal
    solution is still possible, and the function will return true.
    """
    # get a count of how many non green tiles are remaining
    non_green_remaining = 0
    for tile in tiles:
        if tile['color'] != 'green':
            non_green_remaining += 1
    # calculate the maximum number of tiles that can become green with the current swaps remaining (minus five, for an optimal solution)
    maximum_green_swaps = (swaps_remaining - 5) * 2
    if maximum_green_swaps >= non_green_remaining:
        return True
    return False

def save_optimal_swaps(swaps, optimal_swaps):
    # checks whether the current list of swaps is shorter than the existing optimal solution, and if so makes it the new optimal solution.
    if optimal_swaps:
        if len(swaps) < len(optimal_swaps):
            optimal_swaps = copy.deepcopy(swaps)
    # if an optimal solution doesn't exist yet, then the current list is the optimal solution.
    else:
        optimal_swaps = copy.deepcopy(swaps)
    return optimal_swaps

def all_green_tiles(tiles):
    # iterates through all tiles and check if they are all green. returns true or false
    for tile in tiles:
        if tile['color'] != 'green':
            return False
    return True

def update_tile_colors(tiles, solution, lines):
    # resets all tile colors to default grey
    reset_colors(tiles)
    # iterates through the solution words for all lines (rows and columns), converting each to a list that is passed to functions that
    # assign green and yellow colors to tiles that fulfil specific conditions based on waffle game rules
    for i in range(len(solution)):
        solution_word = list(solution[i])
        assign_greens(solution_word, lines, i)
        assign_yellows(solution_word, lines, i)
    
def reset_colors(tiles):
    # resets the colour of all tiles to grey
    for tile in tiles:
        tile['color'] = 'grey'
    
def assign_greens(solution_word, lines, line_index):
    # iterates through letter positions in each line (row or column) and changes their color to green if the letter matches the letter
    # in the same position in the solution word. any letter in the solution word that is matched is changed to upper case so that it
    # isn't counted again as one of the letters in the solution word when assigning yellow to tiles in the "assign_yellows" function
    for i in range(len(lines[line_index])):
        current_letter = lines[line_index][i]['letter']
        if current_letter == solution_word[i]:
            lines[line_index][i]['color'] = 'green'
            solution_word[i] = solution_word[i].upper()
            
def assign_yellows(solution_word, lines, line_index):
    # checks whether each letter is in the current word (not counting letters that are already green, as these letters are capitalised in the
    # assign_greens function and can't match with these lower case letters). if the letter is in the word, that tile's color is changed
    # to yellow and the matching letter in the solution is changed to upper case so that repeated letters in the line don't match with the 
    # same solution letter more than once.
    for i in range(len(lines[line_index])):
        if lines[line_index][i]['color'] != 'green' and lines[line_index][i]['color'] != 'yellow':
            current_letter = lines[line_index][i]['letter']
            for j in range(len(solution_word)):
                if current_letter == solution_word[j]:
                    lines[line_index][i]['color'] = 'yellow'
                    solution_word[j] = solution_word[i].upper()
                    break

if __name__ == "__main__":
    main()