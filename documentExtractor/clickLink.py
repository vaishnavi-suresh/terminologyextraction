from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests

#https://news.google.com/read/CBMixAFBVV95cUxQRXFWNXFmRG9RMUJFUXpROWs1S1FwQW4ybVA1UXVMb0h4bEItYVhyWHJhcklGYkJiZWlsVDNUT3hKZ1NwcGUtYXJBY1ZraURKcFZCaGp2cG85SlJFM29YRHVpMEdhUTFpZV96TWFES3lxdWJsT1lHcERWSnZHaENaS29Wc0xscUJqTFFrYzFTRXFKMUFaREoyd1gya2pRcjlKSHNQYnFfRXdZWDExbHF6UGFMZlJCN3E1YlNXOWNzVlRqc0lH?hl=en-US&gl=US&ceid=US%3Aen

def scrapeLinks(link):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    service = Service('C:\\chromedriver_win32')
    driver = webdriver.Chrome(options=options)
    ua = UserAgent()
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
        "headers": {
            "User-Agent": ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://example.com",
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'sessionid=abc123; csrftoken=xyz456',
        }
        }
    )
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
        tags = ['main','article','body']
        for tag in tags:
            text = driver.find_element(By.TAG_NAME,tag)
                
            paragraphs = text.find_elements(By.TAG_NAME,'p')
            element = "".join([para.text for para in paragraphs])
        

            #print(element)
            if element:
                return element
            
        
    except:
        pass
        return None

