from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from tqdm import tqdm

driver = webdriver.Chrome()

def getSku(url):
    skus_and_links = []
    driver.get(url)
    time.sleep(5)
    sku_elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-id and string-length(@data-id) > 0]')))

    for sku_element in sku_elements:
        sku_name = sku_element.get_attribute('data-id')
        sku_link = sku_element.find_element(By.CSS_SELECTOR, 'a._2rpwqI').get_attribute('href')
        skus_and_links.append([sku_name, sku_link])

    return skus_and_links


    print(str(len(skus)) + ' SKU found on ' + str(url))
 
    return skus

def getImgsnames(url):
    try:
        
        image_links = []
        driver.get(url)
        
        time.sleep(1)
        thumbnails =  WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._2E1FGS')))
  
        for thumbnail in thumbnails:
            try:
                action = ActionChains(driver)
                action.move_to_element(thumbnail).perform()
                time.sleep(0.5)

                larger_image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div._3kidJX')))
                action.move_to_element(larger_image).perform()
                time.sleep(0.5)
                
                zoom_frame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'img._3_UeBw')))
                
                image_src = zoom_frame.get_attribute('src')
             
                image_links.append(image_src)
            except:
                print('Skipping')
    except Exception as e:
        print(str(e))
    return image_links


def mainFunc(baseurl, startpg, endpg, filename):
    
    print(f"Scraping data from {baseurl}")

    current_page = startpg  
    url = ''

    while current_page <= endpg:
      
        url = baseurl+ '&page=' + str(current_page)

        for sku_name, sku_link in tqdm(getSku(url), desc="no of skus done"):
            with open(f"{filename}.txt", "a") as f:
                for echlink in getImgsnames(sku_link):
                    if echlink is not None:
                        f.write(f"SKU Name: {sku_name}, SKU Link: {sku_link}, Image Link: {echlink}\n")

        
        if current_page == endpg:
            break

        current_page += 1 

    
    print(f"Scraping from {url} is complete and data saved to {filename}.txt")

url_filename_mapping = {




      "https://www.flipkart.com/search?q=Artificial+Flowers+and+Plants&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off":"Artificial Flowers and Plants",
       "https://www.flipkart.com/search?q=Chair+Cover&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off":"Chair Cover",
        "https://www.flipkart.com/search?q=Serveware&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off":"Serveware",
         "https://www.flipkart.com/search?q=Towel+Set&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off":"Towel Set",
          "https://www.flipkart.com/search?q=Table+Covers&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off":"Table Covers",
            "https://www.flipkart.com/search?q=Pillows&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off":"Pillows",
      "https://www.flipkart.com/search?q=Bedding+set&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off":"Bedding Set",

}


for url, filename in url_filename_mapping.items():
    startpg = 1
    endpg = 2
    
    mainFunc(url, startpg, endpg, filename)


driver.quit()