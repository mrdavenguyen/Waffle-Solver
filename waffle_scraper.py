from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


def main():
    #options for headless mode
    options = ChromeOptions()
    # options.add_argument("--headless=new")
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
        for tile_data in tile_data_list:
            print_debug(f"{tile_data},")
        print_debug(f"Puzzle {i} complete.")
        #clicks the back button to return to the archive menu
        driver.find_element(By.CSS_SELECTOR, "button.button--back.icon-button").click()

def print_debug(text):
    print(f"{text}")
    with open("puzzle_data.txt", "a") as myfile:
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

if __name__ == '__main__':
    main()
