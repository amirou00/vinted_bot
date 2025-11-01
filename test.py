from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import smtplib

# Initialize email server
email = ""
receiver_email = ""
subject = "***NOTIFICATION VINTED***"
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, "your app password")

# Initialize Chrome driver
service = Service("chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

seen_articles = set()

def etoiles_et_lot(link: str) -> tuple:
    """Check rating and lot status for a given link"""
    try:
        # Open link in new tab
        driver.execute_script(f"window.open('{link}');")
        driver.switch_to.window(driver.window_handles[1])
        
        # Wait for page to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".details-list--wrapper")))
        except TimeoutException:
            print(f"Timeout loading {link}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return False, "Timeout loading page"
        
        # Check for lot
        try:
            description = driver.find_element(By.CSS_SELECTOR, ".details-list--wrapper").text.lower()
            element_lot = "!!! LOT POTENTIEL !!!" if any(
                word in description for word in ["lot", "ensemble", "pack", "set", "bundle"]
            ) else "probablement pas un lot :("
        except NoSuchElementException:
            element_lot = "description not found"
        
        # Check rating
        try:
            rating_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label^="Le membre est noté"]')))
            rating_str = rating_element.get_attribute("aria-label")
            element_etoiles = rating_str in ["Le membre est noté 5 sur 5", "Le membre est noté 4,9 sur 5"]
        except (TimeoutException, NoSuchElementException):
            element_etoiles = False
        
        # Close tab and return to main window
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return element_etoiles, element_lot
        
    except Exception as e:
        print(f"Error processing {link}: {str(e)}")
        # Ensure we return to main window if something goes wrong
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        return False, f"Error: {str(e)}"

def apply_filters():
    """Apply all Vinted filters"""
    # Accept cookies if needed
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
    except TimeoutException:
        pass
    
    # Brand filters
    brands = [
        ("ralph lauren", "brand_ids-list-item-88"),
        ("lacoste", "brand_ids-list-item-304"),
        ("nike", "brand_ids-list-item-53"),
        ("dickies", "brand_ids-list-item-65"),
        ("souleiado", "brand_ids-list-item-46957"),
        ("vintage", "brand_ids-list-item-14803")
    ]
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--brand-filter--trigger"]'))).click()
    
    search = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "brand_filter_search")))
    
    for brand_name, brand_id in brands:
        search.clear()
        search.send_keys(brand_name + Keys.ENTER)
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, brand_id))).click()
            time.sleep(0.5)
        except TimeoutException:
            print(f"Brand {brand_name} not found")
    
    # Status filters
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--status-filter--trigger"]'))).click()
    
    for status_id in ["status_ids-list-item-6", "status_ids-list-item-1", "status_ids-list-item-2"]:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, status_id))).click()
        except TimeoutException:
            print(f"Status {status_id} not found")
    
    # Price filter
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--price-filter--trigger"]'))).click()
    
    price_to = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "price_to")))
    price_to.clear()
    price_to.send_keys("5" + Keys.ENTER)
    
    # Sort filter
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="catalog--sort-filter--trigger"]'))).click()
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "sort_by-list-item-price_low_to_high"))).click()

def main_loop():
    i = 0
    while True:
        try:
            driver.get("https://www.vinted.fr/catalog/4-clothing")
            
            if i == 0:
                apply_filters()
                i += 1
            
            time.sleep(2)
            
            # Scroll and wait for items
            driver.execute_script("window.scrollBy(0, 600);")
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,'[data-testid="grid-item"]')))
            
            # Process items
            articles = driver.find_elements(By.CSS_SELECTOR,'[data-testid="grid-item"]')
            for j in range(min(3, len(articles))):
                try:
                    article = articles[j]
                    link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    
                    if link and link not in seen_articles:
                        print(f"Processing article {j+1}: {link}")
                        etoile, lot = etoiles_et_lot(link)
                        
                        if etoile:
                            seen_articles.add(link)
                            message = f"Subject: {subject}\n\n{link}\n\n{lot}"
                            server.sendmail(email, receiver_email, message)
                            print(f"****************************** Article {j+1}: {link}")
                
                except (StaleElementReferenceException, NoSuchElementException) as e:
                    print(f"Error processing article {j+1}: {str(e)}")
                    continue
            
            time.sleep(10)
            
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            time.sleep(30)
            continue

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("Stopping bot...")
    finally:
        driver.quit()
        server.quit()