
# In[1]:


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import uuid

firefox_options = Options()
firefox_options.add_argument("window-size=1920,1080")
# Headless mode means no GUI
firefox_options.add_argument("--headless")
firefox_options.add_argument("start-maximized")
firefox_options.add_argument("disable-infobars")
firefox_options.add_argument("--disable-extensions")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
firefox_options.add_argument('--disable-blink-features=AutomationControlled')

# Set the location of the executable Firefox program on Brown
firefox_options.binary_location = '/depot/datamine/bin/firefox/firefox'

profile = webdriver.FirefoxProfile()

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()

desired = DesiredCapabilities.FIREFOX


# In[14]:


# Set the location of the executable geckodriver program on Scholar
uu = uuid.uuid4()
driver = webdriver.Firefox(service_log_path=f"/tmp/{uu}", options=firefox_options, executable_path='/depot/datamine/bin/geckodriver', firefox_profile=profile, desired_capabilities=desired)


# In[3]:


import time


# In[15]:


driver.get("https://www.amazon.com/s?k=lightweight+laptop&i=computers&rh=n%3A565108%2Cp_36%3A2421891011%2Cp_85%3A2470955011&dc&page=2&crid=1YE9T4260HL9H&qid=1651533451&rnid=2470954011&sprefix=lightweight+laptop%2Caps%2C115&ref=sr_pg_2")


# In[5]:


time.sleep(2)


# In[85]:


element = driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]')
element.send_keys("Gaming Laptop")
time.sleep(2)


# In[7]:


from selenium.webdriver.common.keys import Keys


# In[86]:


element.send_keys(Keys.RETURN)


# In[87]:


time.sleep(2)


# In[16]:


element = driver.find_element_by_xpath('//div[@data-component-type="s-search-result"][1]')
print(element.get_attribute('outerHTML')[:200])


# ('//span[@class="a-size-medium a-color-base a-text-normal"]').text

# In[17]:


mycards = driver.find_elements_by_xpath('//div[@data-component-type="s-search-result"]')
for mycounter, specificcard in enumerate(mycards):
    print(f'{mycounter}.{specificcard.get_attribute("data-asin")}')


# In[18]:


mycards[2].find_element_by_xpath('.//a[@class="a-link-normal s-no-outline"]').get_attribute('href')


# In[19]:


# Let's load every 2 cards or so at a time
url_list=[]
for mycounter, card in enumerate(mycards):
    ulink = card.find_element_by_xpath('.//a[@class="a-link-normal s-no-outline"]').get_attribute('href')
    url_list.append((mycounter+1, ulink))


# In[10]:


import lxml.html
import requests

my_headers={'User-Agent': 'Mozilla/5.0'}


# In[11]:


def get_computer_info(gid, url):
    response = requests.get(url, stream=True, headers=my_headers)
    tree = lxml.html.fromstring(response.text)
    img_url = tree.xpath('//div[@id="main-image-container"]//img[@id="landingImage"]/@src')[0]
    price = tree.xpath('//div[starts-with(@id,"corePrice")]//span[@class = "a-offscreen"][1]')[0].text.lstrip('$').replace(',','')
    description = tree.xpath('//span[@id="productTitle"]')[0].text.rstrip(' ').lstrip(' ')
    
    brand = tree.xpath('//div[@id="productOverview_feature_div"]//tr[1]/td[2]/span')[0].text
    name = tree.xpath('//div[@id="productOverview_feature_div"]//tr[2]/td[2]/span')[0].text
    displaysize = tree.xpath('//div[@id="productOverview_feature_div"]//tr[3]/td[2]/span')[0].text
    hd_capacity = tree.xpath('//div[@id="productOverview_feature_div"]//tr[5]/td[2]/span')[0].text
    cpu_type = tree.xpath('//div[@id="productOverview_feature_div"]//tr[6]/td[2]/span')[0].text
    memory_capacity = tree.xpath('//div[@id="productOverview_feature_div"]//tr[7]/td[2]/span')[0].text
    card_model = tree.xpath('//div[@id="productOverview_feature_div"]//tr[10]/td[2]/span')[0].text
    
    cpu_brand = tree.xpath('//table[@id="productDetails_techSpec_section_2"]//tr[10]/td')[0].text.rstrip(' ')[-5:]
    if cpu_brand.lower() != 'intel':
        cpu_brand = 'AMD'
    
    
    qtuple = (gid, name, float(price), description, brand, cpu_brand, cpu_type, memory_capacity, hd_capacity, card_model, displaysize, img_url)
    return qtuple


# In[11]:


def get_computer_info2(gid, url):
    response = requests.get(url, stream=True, headers=my_headers)
    tree = lxml.html.fromstring(response.text)
    img_url = tree.xpath('//div[@id="main-image-container"]//img[@id="landingImage"]/@src')[0]
    price = tree.xpath('//div[starts-with(@id,"corePrice")]//span[@class = "a-offscreen"][1]')[0].text.lstrip('$').replace(',','')
    description = tree.xpath('//span[@id="productTitle"]')[0].text.rstrip(' ').lstrip(' ')
    
    brand = tree.xpath('//div[@id="productOverview_feature_div"]//tr[1]/td[2]/span')[0].text
    name = tree.xpath('//div[@id="productOverview_feature_div"]//tr[2]/td[2]/span')[0].text
    displaysize = tree.xpath('//div[@id="productOverview_feature_div"]//tr[3]/td[2]/span')[0].text
    hd_capacity = tree.xpath('//div[@id="productOverview_feature_div"]//tr[5]/td[2]/span')[0].text
    cpu_type = tree.xpath('//div[@id="productOverview_feature_div"]//tr[6]/td[2]/span')[0].text
    memory_capacity = tree.xpath('//div[@id="productOverview_feature_div"]//tr[7]/td[2]/span')[0].text
    card_model = tree.xpath('//div[@id="productOverview_feature_div"]//tr[10]/td[2]/span')[0].text
    
    cpu_brand = tree.xpath('//table[@id="productDetails_techSpec_section_2"]//tr[10]/td')[0].text.rstrip(' ')[-5:]
    if cpu_brand.lower() != 'intel':
        cpu_brand = 'AMD'
    
    
    qtuple = (gid, name, float(price), description, brand, cpu_brand, cpu_type, memory_capacity, hd_capacity, card_model, displaysize, img_url)
    return qtuple


# In[20]:


computer_list=[]
for (gid, url) in url_list:
    try:
        qtp=get_computer_info2(gid, url)
        computer_list.append(qtp)
    except IndexError:
        print(1)
        continue

# get_computer_info(1, 'https://www.amazon.com/HP-Display-i3-1115G4-Processor-Bluetooth/dp/B09V5PM2J6/ref=sr_1_3?crid=1WEMLNLE9RZQD&keywords=Laptop&qid=1651437130&sprefix=laptop%2Caps%2C142&sr=8-3&th=1')


# In[21]:


computer_list


# In[130]:


computer_list1


# In[13]:


computer_list2


# In[33]:


driver.get('https://www.zillow.com/homes/for_sale/34474_rb/')


# In[34]:


time.sleep(5)


# In[36]:


mybedbutton = driver.find_element_by_xpath('//button[@id="beds"]')
mybedbutton.click()


# In[37]:


bedbutton4 = driver.find_element_by_xpath('//div[@name="beds-options"]/button[@value=4]')
bedbutton4.click()


# In[38]:


bathbutton3 = driver.find_element_by_xpath('//div[@name="baths-options"]/button[@value=3]')
bathbutton3.click()


# In[39]:


cards = driver.find_elements_by_xpath('//article[starts-with(@id, "zpid_")]')
print(cards[10].get_attribute("outerHTML"))


# In[41]:


for mycounter, specificcard in enumerate(cards):
    if mycounter % 2 == 0:
        try:
            driver.execute_script('arguments[0].scrollIntoView();', specificcard)
            time.sleep(2)

        except StaleElementReferenceException:
            # every once in a while we will get a StaleElementReferenceException
            # because we are trying to access or scroll to an element that has changed.
            # this probably means we can skip it because the data has already loaded.
            continue

cards = driver.find_elements_by_xpath('//article[starts-with(@id, "zpid_")]')
print(cards[10].get_attribute("outerHTML"))


# In[42]:


prices = []
sq_ftgs = []
for ct, card in enumerate(cards):
    try:
        sqft = card.find_element_by_xpath('.//ul[@class="list-card-details"]/li[3]').text
        sqft = re.sub('[^0-9.]', '', sqft)

        # if there isn't any sq footage skip the card entirely
        if sqft == '':
            continue

        price = card.find_element_by_xpath('.//div[@class="list-card-price"]').text
        price = re.sub('[^0-9.]', '', price)

        # if there isn't any price skip the card entirely
        if price == '':
            continue

        sq_ftgs.append(float(sqft))
        prices.append(float(price))

    except NoSuchElementException:
        # verify that it is a plot of land, if not, panic
        is_lot = 'land' in card.find_element_by_xpath(".//ul[@class='list-card-details']/li[2]").text.lower()
        if not is_lot:
            print("NOT LAND")
            print(card.find_element_by_xpath(".//ul[@class='list-card-details']/li[2]").text)
            sys.exit(0)
        else:
            continue

print(sum(prices)/len(prices))
print(sum(sq_ftgs)/len(sq_ftgs))

