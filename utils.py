import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from io import BytesIO
from selenium.webdriver.chrome.options import Options

def scrap_articles():

    """
    Allow the legislative and regulatory texts scraping on Légifrance website.

    This function takes no keyword arguments.

    This function returns a dataframe containing the law articles with names and identifiers.
    """
    #------#
    #FIRST PART : IDENTIFIERS AND ARTICLE NAMES STORAGE
    #------#

    
    options = Options()     # chrome options for the webdrivers
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--no-sandbox')     
    options.add_argument('--disable-dev-shm-usage')        
    
    
    url_legi_part = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072050/LEGISCTA000006132338/#LEGISCTA000006132338'     # URL of legislative part
    url_regu_part = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072050/LEGISCTA000018488235/#LEGISCTA000018532924'     # URL of regulatory part
    
    
    driver_legi = webdriver.Chrome(executable_path='chromedriver.exe', options=options)     # webdriver instantiation for legislative part
    driver_regl = webdriver.Chrome(executable_path='chromedriver.exe', options=options)     # webdriver instanciation for regulatory part


    driver_legi.get(url_legi_part)
    ARTICLES = driver_legi.find_elements(By.CLASS_NAME, "name-article")     # store all articles information of legislative part in ARTICLES variable

    driver_regl.get(url_regu_part)
    ARTICLES += driver_regl.find_elements(By.CLASS_NAME, "name-article")       # add all articles information of regulatory part in ARTICLES variable      

    ARTICLES_IDS = []
    ARTICLES_NAMES = []
    for ids in ARTICLES:
        ARTICLES_IDS.append(ids.get_attribute('data-anchor'))
        ARTICLES_NAMES.append(ids.text)

    driver_legi.close()
    driver_regl.close()
    
    #------#
    #SECOND PART : ARTICLE STORAGE
    #------#

    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)      # webdriver instanciation


    LINKS_TO_ARTICLES = []      # variable for all web links 
    BASE_LINK = 'https://www.legifrance.gouv.fr/codes/article_lc/'      # basic link contained by all links to articles
    for id in ARTICLES_IDS:
        link = BASE_LINK + str(id)
        LINKS_TO_ARTICLES.append(link)      # article links storage

    ARTICLES_TEXT = []      # variable for articles content 
    timeout = 10        # timeout set in order to wait for the web page loading 
    counter = 0
    for k in range(0, len(ARTICLES_IDS)):
        driver.get(LINKS_TO_ARTICLES[k])
        try:
            # presence of element is detected after the web page loads
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '#main > div > div.main-col > div.page-content.folding-element > article > div > div.content'))
            WebDriverWait(driver, timeout).until(element_present)
            # article content storage  : one web page per article
            ARTICLE = driver.find_element(By.CSS_SELECTOR, '#main > div > div.main-col > div.page-content.folding-element > article > div > div.content')
            ARTICLES_TEXT.append(ARTICLE.text)
            print("ARTICLE " + str(ARTICLES_IDS[k])+ " STORED")

        except TimeoutException:
            # error printed if web page doesnt load
            print("⚠️ Timed out waiting for page to load")
            counter += 1
    
    print("NOMBRE D'ARTICLES NON CHARGES : " + str(counter))
        

    driver.close()

    # dictionary of all information related to all articles
    articles_description = {
        'Identifiant' : ARTICLES_IDS,
        'Article' : ARTICLES_TEXT,
        'Référence' : ARTICLES_NAMES
    }

    df_articles_description = pd.DataFrame.from_dict(articles_description).set_index('Identifiant')

    return df_articles_description


def to_excel(df: pd.DataFrame):
    """
    This function converts a pandas dataframe to an excel file.

    Keyword argument : pandas dataframe.
    """
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()


def intersection(lst1, lst2):
    """
    This function computes the intersection of 2 sets.

    Keyword arguments : 
    two list.
    """
    lst_intersection = [value for value in lst1 if value in lst2]
    return lst_intersection


def union(lst1, lst2):
    """
    This function computes the union of 2 sets.

    Keyword arguments : 
    two list. 
    """
    lst_union = list(set(lst1) | set(lst2))
    return lst_union    


def difference(lst1, lst2):
    """
    This function computes the difference of 2 sets.

    Keyword arguments : 
    two list. 
    """
    s = set(lst2)
    lst_diff = [x for x in lst1 if x not in s]
    return lst_diff






