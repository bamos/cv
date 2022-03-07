#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import shutil
import os

width = 1024
height = 768

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1024x768')

urls = [
    ["https://ceyani.io/", "https://github.com/emirceyani/cv"],
    # ["https://www.natolambert.com/cv", "https://github.com/natolambert/cv"],
    ["https://chahuja.com/", "https://github.com/chahuja/cv"],
    ["http://www.cbclement.com/cv/", "https://github.com/colinclement/cv"],
    ["https://davidlindell.com/", "https://github.com/davelindell/cv"],
    # ["http://georei.com/", "https://github.com/skachuck/cv"],
    ["https://jmloyola.github.io/cv/", "https://github.com/jmloyola/cv"],
    ["https://lizonly.github.io/cv/", "https://github.com/lizOnly/cv"],
    # ["https://m-oikonomou.github.io/", "https://github.com/m-oikonomou/cv"],
    [" https://nplawrence.com/cv/", "https://github.com/NPLawrence/CV"],
    ["https://renansouza.org/", "https://github.com/renan-souza/cv"],
    ["http://cogscikid.com/files/wilka_carvalho_CV.pdf", "https://github.com/wcarvalho/cv"],
    "https://pinardemetci.github.io/",
    "https://stevetkjan.github.io/",
    "https://vinayakumarr.github.io/",
    "https://fmeier.github.io/",
    "https://hubert0527.github.io/",
    "https://dekura.github.io/",
    "https://joancano.github.io/",
    "https://jwy-leo.github.io/",
    "https://lilyo.github.io/",
    "https://nurpeiis.github.io/",
    "https://dineshresearch.github.io/",
    "https://yannael.github.io/",
    "https://murali-koppula.github.io/",
    "https://swami1995.github.io/",
    "https://boyochen.github.io/",
    "https://alexsludds.github.io/",
    "https://laminjuwara.github.io",
    "https://krishnakancharla.github.io/about",
    "https://chaibapchya.github.io/about",
    "https://conan7882.github.io/",
    "https://suredream.github.io/",
    "https://pinardemetci.github.io/",
    "https://prachisudrik.github.io/about",
    "https://mpicci.github.io/",
    "https://scriptedonachip.com/",
    "https://alessandrochecco.github.io/",
]

tmpdir = tempfile.mkdtemp()
print(tmpdir)

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(20)
for i, url in enumerate(urls):
    # TODO: Quick hack for now, could clean up
    if isinstance(url, list):
        web_url, code_url = url
    else:
        web_url = url
    try:
        driver.get(web_url)
    except:
        # print(f'timeout for {web_url}')
        print(f"+ {url}")
        continue

    if isinstance(url, list):
        print(f"+ [{driver.title}]({web_url}) ([code]({code_url}))")
    else:
        print(f"+ [{driver.title}]({web_url})")
    driver.save_screenshot(f"{tmpdir}/{i}.png")

os.system(f'montage {tmpdir}/*.png -resize 700x -geometry +0-0 -tile 3x forks.png')
# shutil.rmtree(tmpdir)
