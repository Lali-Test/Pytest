import csv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("termino_de_busqueda", [
    "Albaricoque", "Motocicleta", "Aveztruz", "Helicoptero", "Hermafrodita"
])
def test_google_busqueda(browser, termino_de_busqueda):
    # wait until the search box is clickable
    search_box = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )
    search_box.send_keys(termino_de_busqueda + Keys.RETURN)

    assert termino_de_busqueda.lower() in browser.page_source.lower()



@pytest.fixture
def browser():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.ecosia.org/")
    yield driver
    driver.quit()

# Función auxiliar para leer los términos dentro del CSV
def read_search_terms():
    with open('TestData/busquedaGoogle.csv', newline= '') as csvfile:
        data = list(csv.reader(csvfile))
    # Devuelve solo los términos de búsqueda, excluyendo el título de la columna
    return [row[0] for row in data[1:]]

# Fixture para parametrizar los términos de búsqueda leídos desde el archivo CSV
@pytest.fixture(params=read_search_terms())
def termino_de_busqueda(request):
    return request.param

# Test que utiliza los datos que vienen del CSV
def test_google_busqueda(browser, termino_de_busqueda):
    search_box = browser.find_element("name", "q")
    search_box.send_keys(termino_de_busqueda + Keys.RETURN)

    results = browser.find_element("id", "search")
    assert (
        len(results.find_elements("xpath", ".//div")) > 0
    ), "Hay resultados de búsqueda"