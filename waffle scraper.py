from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# #options for headless mode
# options = ChromeOptions()
# options.add_argument("--headless=new")
# driver = webdriver.Chrome(options=options)

#option for regular web browser
driver = webdriver.Chrome()

driver.get("https://wafflegame.net/archive")

#waits until the data is displayed and visible on the screen
WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'stat-row__val')))
items = driver.find_elements(By.CLASS_NAME, 'stat-row__val')
for item in items:
    #there are a few blanks here, data that isn't actually visible in the current vew and thus empty
    #so I just am looking to grab the first non-blank element and strip out just the max puzzle count and stores it
    if item.text != "":
        #strips the txt from a value of '0 / 899 (0%)' ->  '899'
        num_puzzles = int(item.text.rsplit("/ ")[1].rsplit(" (")[0])
        break

for i in range(1, num_puzzles + 1):
    # driver.get("https://wafflegame.net/archive")
    # wait for the item with the specific data-id to be present
    item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[@data-id='{i}']")))
    # scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView();", item)
    
    # wait until the element is clickable and then click it
    # time.sleep(.1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[@data-id='{i}']"))).click()

    # time.sleep(.1)
    # Find all tile elements
    wait = WebDriverWait(driver, 20)
    
    # find elements with class names starting with "tile draggable tile" - notated by the ^ 
    tiles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class^='tile draggable tile']")))

    tile_data = []
    count = 0
    for tile in tiles:
        letter = tile.text

        #DEBUG
        if letter == "":
            quit()
        
        classes = tile.get_attribute('class').split()
        color = None
        if 'green' in classes:
            color = 'green'
        elif 'yellow' in classes:
            color = 'yellow'
        # elif 'gray' in classes:
        #     color = 'gray'
        # elif 'fixed' in classes:
        #     color = 'fixed'
        
        tile_data.append({
            'letter': letter,
            'color': color
        })
        count += 1
        if count == 21:
            break

    for data in tile_data:
        print(data)
    print(f"Puzzle {i} complete.")

    driver.find_element(By.CSS_SELECTOR, "button.button--back.icon-button").click()



# <button tabindex="-1" class="button--back icon-button" style=""> </button>
