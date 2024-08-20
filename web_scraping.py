from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Path to your WebDriver (e.g., chromedriver)
driver_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'



# Initialize the WebDriver (e.g., Chrome)

driver = webdriver.Chrome()

page = 1

while page < 50:

    # URL of the website you want to scrape
    url = f"https://www.coinbase.com/pt-br/explore?page=${1}"

    # Open the URL in the browser
    driver.get(url)

    # Wait for the page to load (adjust sleep time as necessary)
    time.sleep(5)

    # Find the data you want to scrape
    # This example assumes you want to scrape some text within <h2> tags
    data = []
    elements = driver.find_elements(By.TAG_NAME, 'tr')
    for i in range(len(elements)):
        time.sleep(5)
        try:
            # Re-find the elements list as it might have changed
            elements = driver.find_elements(By.TAG_NAME, 'tr')
            element = elements[i]

            aria_label = element.get_attribute('aria-label')
            
            if aria_label:
                name = aria_label.strip()[21:]  # Adjust as necessary
                
                # Construct the URL based on the name
                url1 = f"https://www.coinbase.com/pt-br/price/{name.lower()}"
                
                # Navigate to the new URL
                driver.get(url1)
                
                # Wait for the new page to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
                
                # Find the first <p> element on the new page
                paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div[role="region"] p')
                
                if paragraphs:
                    first_paragraph_text = paragraphs[1].text
                    
                    
                else:
                    first_paragraph_text = "No paragraph found"
                
                
                # Add data to the DataFrame
                data.append({'Name': name, 'Text': first_paragraph_text})
                

                time.sleep(5)
                
                # Go back to the previous page
                driver.back()
                
                # Wait for the page to reload
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
                
        except Exception as e:
            print(f"An error occurred: {e}")
    page +=1

# Close the browser
driver.quit()

# Create a pandas DataFrame from the data
df = pd.DataFrame(data, columns=["Title"])

# Save the DataFrame to a CSV file
df.to_csv("scraped_data_selenium.csv", index=False)

print("Data scraped and saved to scraped_data_selenium.csv")
