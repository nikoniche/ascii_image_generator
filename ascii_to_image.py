import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
from PIL import Image

URL = "https://onlineasciitools.com/convert-ascii-to-image"

with open("config.json", "r") as r:
    config = json.load(r)
    DOWNLOAD_DIR = config["download_path"]
    CHROMEDRIVER = config["chromedriver_path"]

DOWNLOAD_NAME = "output-onlineasciitools.png"

DOWNLOAD = f"{DOWNLOAD_DIR}\{DOWNLOAD_NAME}"


def get_element(driver, by, path):
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, path)))
    except Exception as e:
        raise e
    else:
        return element


def generate_image(font_size: int) -> Image:
    """Using a selenium webdriver pastes a txt file representation of an image to a set website that converts
    it to an image and downloads to a designated folder."""

    print("Creating webdriver")
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_experimental_option("prefs",
                                   {
                                       "download.default_directory": "D:\Downloads",
                                       "download.prompt_for_download": False
                                   }
                                   )

    driver = webdriver.Chrome(CHROMEDRIVER, options=option)

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow', 'downloadPath': "D:\Downloads"}}
    driver.execute("send_command", params)
    driver.get(URL)

    print("Setting background color.")
    bg_color = get_element(driver, By.XPATH,
                           "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[4]/div[2]/div/div[1]/div[1]/input")
    bg_color.clear()
    bg_color.send_keys("#000000")

    print("Setting text color.")
    text_color = get_element(driver, By.XPATH,
                             "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[4]/div[2]/div/div[2]/div[1]/input")
    text_color.clear()
    text_color.send_keys("white")

    print("Selecting font size.")
    font_size_el = get_element(driver, By.XPATH,
                            "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[4]/div[2]/div/div[2]/div[2]/input")
    font_size_el.clear()
    font_size_el.send_keys(f"{font_size}px")

    print("Selecting font.")
    font = Select(get_element(driver, By.XPATH,
                              "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[4]/div[2]/div/div[2]/div[3]/div/select"))
    font.select_by_visible_text("Monospace")

    print("Importing the ASCII text file.")
    file_input = get_element(driver, By.XPATH,
                             "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[4]/div[1]/div[1]/div/div[2]/div[1]/div[1]/input")
    abs_path = os.path.abspath("ascii_image.txt")
    file_input.send_keys(abs_path)

    time.sleep(1)

    print("Downloading the image.")
    save_as = get_element(driver, By.XPATH,
                          "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[4]/div[1]/div[2]/div/div[2]/div[1]/div[3]")
    save_as.click()

    time.sleep(1)

    download = get_element(driver, By.XPATH,
                           "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[4]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]")
    download.click()

    print("Download completed, quitting driver.")
    time.sleep(1)
    driver.quit()

    # print("Renaming and moving final result")
    # if os.path.exists("converted_image.png"):
    #     os.remove("converted_image.png")
    os.remove("ascii_image.txt")
    # shutil.move(DOWNLOAD, "converted_image.png")
    # Image.open("converted_image.png").show()

    print("Finished.")

    return Image.open(DOWNLOAD)
