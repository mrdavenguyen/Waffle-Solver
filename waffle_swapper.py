def main():
    swaps = []
    least_swaps = []
    swaps_remaining = 15
    find_optimal_swaps()

def find_optimal_swaps():
    assign_colors()
    loop_through_all_letters:
    if all_green:
        save_least_swaps()
        return
    if (swaps_remaining - 5) * 2 < non_green_remaining:
        return
    loop_through_all_index_pairs:
        if not green:
            swap_pair()
            save_swap()
            increment_indexes()
            find_optimal_swaps()
            swaps[-1].pop()
        else:
            increment_indexes()
            find_optimal_swaps()
            return

def assign_colors():
    loop_through_all_boxes:
        reset_colors()
    loop_through_all_lines:
        solution_word = []
        loop_through_all_letters:
            solution_word.append(solution[line_index][letter_index]['letter'])
        solution_word = assign_greens(solution_word)
        assign_yellows_and_whites()
    
def assign_greens():
    loop_through_all_letters:
        if current_letter == solution_word[i]:
            lines[line_index][letter_index]['color'] = 'green'
            solution_word[i] = solution_word[i].upper()
    return solution_word
            
def assign_yellows_and_whites():
    loop_through_all_letters:
        if lines[line_index][letter_index]['color'] != 'green' and lines[line_index][letter_index]['color'] != 'yellow':
            if current_letter in solution_word:
                lines[line_index][letter_index]['color'] = 'yellow'
                solution_word[i] = solution_word[i].upper()
            else:
                lines[line_index][letter_index]['color'] = 'white'

if __name__ == "__main__":
    main()

    
