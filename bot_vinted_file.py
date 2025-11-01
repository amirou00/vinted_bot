from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib


email = ""
receiver_email = ""
subject = "***NOTIFICATION VINTED***"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, "your app password")

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

seen_articles = set()

def etoiles_et_lot(t) -> tuple: # t is a WebElement
    element_lot = "probablement pas un lot :("
    element_etoiles = False
    
    try:
        t.click()
        time.sleep(1)
        # partie lot
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "summary-max-lines-4"))) 
        text = driver.find_element(By.CLASS_NAME, "summary-max-lines-4").text.lower()
        if "lot" in text or "ensemble" in text or "pack" in text or "set" in text or "bundle" in text:
            element_lot = "!!! LOT POTENTIEL !!!"
        time.sleep(1)
        # partie étoile/score
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label^="Le membre est noté"]')))
        element = driver.find_element(By.CSS_SELECTOR, 'div[aria-label^="Le membre est noté"]')
        rating_str = element.get_attribute("aria-label")
        if (rating_str == "Le membre est noté 5 sur 5") or (rating_str == "Le membre est noté 4,9 sur 5"):
            element_etoiles = True
        driver.back()  
        return element_etoiles, element_lot
    except :
        return element_etoiles, element_lot

i = 0

while True:

    try :
        driver.get("https://www.vinted.fr/catalog/4-clothing")

        if i == 0:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))  
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            i += 1

        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--brand-filter--trigger"]')))

        #pour gérer la marque des vêtements
        marque0 = driver.find_element(By.CSS_SELECTOR,'[data-testid="catalog--brand-filter--trigger"]')
        marque0.click() 

        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "brand_filter_search")))

        searcher = driver.find_element(By.ID, "brand_filter_search")
        searcher.clear()
        searcher.send_keys("ralph lauren")
        searcher.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "brand_ids-list-item-88")))
        marque1 = driver.find_element(By.ID, "brand_ids-list-item-88") #ralph lauren
        marque1.click() 
        time.sleep(1)

        searcher.send_keys(Keys.CONTROL + "a")
        searcher.send_keys(Keys.DELETE)
        searcher.send_keys("lacoste")
        searcher.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "brand_ids-list-item-304")))
        marque2 = driver.find_element(By.ID, "brand_ids-list-item-304") #lacoste
        marque2.click() 
        time.sleep(1)

        searcher.send_keys(Keys.CONTROL + "a")
        searcher.send_keys(Keys.DELETE)
        searcher.send_keys("nike")
        searcher.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "brand_ids-list-item-53")))
        marque3 = driver.find_element(By.ID, "brand_ids-list-item-53") #nike
        marque3.click()
        time.sleep(1)

        searcher.send_keys(Keys.CONTROL + "a")
        searcher.send_keys(Keys.DELETE)
        searcher.send_keys("dickies")
        searcher.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "brand_ids-list-item-65")))
        marque4 = driver.find_element(By.ID, "brand_ids-list-item-65") #dickies
        marque4.click()
        time.sleep(1)

        searcher.send_keys(Keys.CONTROL + "a")
        searcher.send_keys(Keys.DELETE)
        searcher.send_keys("souleiado")
        searcher.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "brand_ids-list-item-46957")))
        marque5 = driver.find_element(By.ID, "brand_ids-list-item-46957") #souleiado
        marque5.click()
        time.sleep(1)

        searcher.send_keys(Keys.CONTROL + "a")
        searcher.send_keys(Keys.DELETE)
        searcher.send_keys("vintage")
        searcher.send_keys(Keys.ENTER)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "brand_ids-list-item-14803")))
        marque6 = driver.find_element(By.ID, "brand_ids-list-item-14803") #vintage
        marque6.click()
        #fin de la partie marque

        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--status-filter--trigger"]')))

        #gérer l'état des vêtements
        etat0 = driver.find_element(By.CSS_SELECTOR,'[data-testid="catalog--status-filter--trigger"]')
        etat0.click()

        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "status_ids-list-item-6")))

        etat1 = driver.find_element(By.ID, "status_ids-list-item-6") #neuf avec étiquette
        etat1.click()
        etat2 = driver.find_element(By.ID, "status_ids-list-item-1") #neuf sans étiquette
        etat2.click()
        etat3 = driver.find_element(By.ID, "status_ids-list-item-2") #très bon état
        etat3.click()
        #fin de la partie état

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--price-filter--trigger"]')))

        #pour gérer le prix (max)
        prix0 = driver.find_element(By.CSS_SELECTOR,'[data-testid="catalog--price-filter--trigger"]')
        prix0.click()

        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "price_to")))

        prix1 = driver.find_element(By.ID, "price_to")
        prix1.clear()
        prix1.send_keys("5" + Keys.ENTER) #pour mettre le prix max à 5 euros
        #fin de la partie prix

        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--sort-filter--trigger"]')))

        #trie
        trie0 = driver.find_element(By.CSS_SELECTOR,'[data-testid="catalog--sort-filter--trigger"]') 
        trie0.click()

        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "sort_by-list-item-price_low_to_high")))

        trie1 = driver.find_element(By.ID, "sort_by-list-item-price_low_to_high") #pour trier par prix croissant
        trie1.click()
        #fin de la partie trie

        time.sleep(1)

        # the real deal
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1)

        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'[data-testid="grid-item"]')))

        articles = driver.find_elements(By.CSS_SELECTOR,'[data-testid="grid-item"]')
        for j in range(min(3, len(articles))):
            time.sleep(2)
            current_articles = driver.find_elements(By.CSS_SELECTOR,'[data-testid="grid-item"]')
            article = current_articles[j]
            link_element = article.find_element(By.TAG_NAME, 'a')
            link = link_element.get_attribute('href')  
            if link and link not in seen_articles:
                etoile, lot = etoiles_et_lot(link_element)
                if etoile:
                    seen_articles.add(link)
                    message = link
                    text = f"Subject: {subject}\n\n{message}\n\n{lot}"
                    server.sendmail(email, receiver_email, text)
                    print(f"****************************** Article {j+1}: {link}")
            time.sleep(1)

        time.sleep(30)

    except :
        print("An error occurred, retrying...")
        continue
        # If an error occurs, we just continue to the next iteration

# not sure if i should keep these...
driver.quit()
server.quit()   


