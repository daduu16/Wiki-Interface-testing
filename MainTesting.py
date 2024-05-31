import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

@pytest.fixture(params=["chrome", "edge"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif request.param == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    driver.implicitly_wait(3)
    yield driver
    driver.quit()

def test_nasa_wikipedia_page_logo(driver):
    driver.get("https://en.wikipedia.org/wiki/NASA")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/header/div[1]/a/span/img[1]')))
    logo = driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/a/span/img[1]')
    assert logo.size['width'] == 160 and logo.size['height'] == 160

def test_nasa_wikipedia_page_table(driver):
    driver.get("https://en.wikipedia.org/wiki/NASA")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[3]')))
    table = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[3]')
    assert table.value_of_css_property("box-sizing") == "border-box"

def test_nasa_wikipedia_page_background(driver):
    driver.get("https://en.wikipedia.org/wiki/NASA")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body')))
    body = driver.find_element(By.XPATH, '/html/body')
    assert body.value_of_css_property("background-color") == "rgba(248, 249, 250, 1)"

def test_nasa_wikipedia_page(driver):
    driver.get("https://en.wikipedia.org/wiki/NASA")

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/ul[5]')))

    ul_element = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/ul[5]')
    list_items = ul_element.find_elements(By.TAG_NAME, 'li')

    for item in list_items:
        links = item.find_elements(By.TAG_NAME, 'a')
        for link in links:
            font_family = link.value_of_css_property("font-family").lower()
            font_size = float(link.value_of_css_property("font-size").strip("px"))

            assert "sans serif" in font_family
            assert 12.6 == font_size

if __name__ == "__main__":
    pytest.main([__file__, '--html=report.html', '--self-contained-html'])
