import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from io import BytesIO
from selenium.webdriver.chrome.options import Options
import time

BATCH_SIZE = 50
TIMEOUT = 90

def chunck_list(list_ : list, batch_size : int):
    """
    This function subdivides a list in small sets.

    Keyword arguments : 
    - list
    - batch_size : length of each set.
    """
    chuncked_list = list()
    for k in range(0, len(list_), batch_size):
        chuncked_list.append(list_[k:k+batch_size])

    return chuncked_list

def get_ids_and_names():

    """
    Allow the legislative and regulatory texts scraping on Légifrance website.

    This function takes no keyword arguments.

    This function returns two lists containing the law articles names and identifiers.
    """
    #------#
    # IDENTIFIERS AND ARTICLE NAMES STORAGE
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

    return ARTICLES_IDS, ARTICLES_NAMES

def get_articles(ids : list, timeout : int):
    """
    Allow the legislative and regulatory texts scraping on Légifrance website.

    Keyword arguments :
    - list of articles ids
    - list of articles names.

    This function returns a dataframe containing the law articles with names and identifiers.
    """
    options = Options()     # chrome options for the webdrivers
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--no-sandbox')     
    options.add_argument('--disable-dev-shm-usage')    

    #------#
    # ARTICLE STORAGE
    #------#

    ARTICLES_IDS = ids

    LINKS_TO_ARTICLES = []      # variable for all web links 
    BASE_LINK = 'https://www.legifrance.gouv.fr/codes/article_lc/'      # basic link contained by all links to articles
    for id in ARTICLES_IDS:
        link = BASE_LINK + str(id)
        LINKS_TO_ARTICLES.append(link)      # article links storage

    ARTICLES_TEXT = []      # variable for articles content 
    counter = 0     # counter for the number of pages that can't load
    IDS_UNLOADED = []
    
    # webdriver instanciation for each batch
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    
    for k in range(0, len(ids)):        
        driver.get(LINKS_TO_ARTICLES[k])
        try:
            # presence of element is detected after the web page loads
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '#main > div > div.main-col > div.page-content.folding-element > article > div > div.content'))
            WebDriverWait(driver, timeout).until(element_present)
            # article content storage  : one web page per article
            ARTICLE = driver.find_element(By.CSS_SELECTOR, '#main > div > div.main-col > div.page-content.folding-element > article > div > div.content')
            ARTICLES_TEXT.append(ARTICLE.text)
            # print("ARTICLE " + str(ARTICLES_IDS[k])+ " STORED")
        except TimeoutException:
            # error printed if web page doesnt load
            print("⚠️ Timed out waiting for page to load")
            counter += 1
            print("❗️ ARTICLE NON CHARGE : " + str(ARTICLES_IDS[k]))
            print("❗️ NOMBRE D'ARTICLES NON CHARGES : " + str(counter))
            IDS_UNLOADED.append(ARTICLES_IDS[k])
            ARTICLES_TEXT.append("ERREUR DE CHARGEMENT DE L'ARTCILE")
    driver.close()
    
    return ARTICLES_TEXT, IDS_UNLOADED

def get_inventory_description(ids : list, text : list, names : list):
    """
    This function constructs a pandas dataframe containing all information related to articles.

    Keyword argument : 3 lists of the ids, content and names of articles.
    """
    articles_description = {
        'Identifiant' : ids,
        'Article' : text,
        'Référence' : names
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

def detect_modification(df_old : pd.DataFrame, df_new : pd.DataFrame):
    df_old_ = df_old.set_index('Identifiant')
    df_new_ = df_new.set_index('Identifiant')
    old_list = list(df_old_.index)       # list of ids in old inventory
    new_list = list(df_new_.index)       # list of ids in new inventory

    # count modified articles
    list_intersection = intersection(old_list, new_list)
    nb_modif = 0
    list_id_modif = []
    for id in list_intersection:
            df_modif = df_new_.loc[df_new_['Article'] != df_old_['Article']]
            list_id_modif.append(id)
            nb_modif += 1
    
    return df_modif
    








