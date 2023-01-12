import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from io import BytesIO
#from pyxlsb import open_workbook as open_xlsb


def scrap_articles():
    '''
    #------#
    #PREMIERE PARTIE : STOCKAGE DES ID ET NOMS DES ARTICLES
    #------#

    #instanciation de l'URL contenant l'arborescence des articles
    url = 'https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006072050'

    #instanciation du webdriver pour Chrome
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    #Navigation de la page web pour trouver tous les articles 
    ARTICLES = driver.find_elements(By.CLASS_NAME, "articleLink")

    #Stockage des ids et noms des articles 
    ARTICLES_IDS = []
    ARTICLES_NAMES = []
    for ids in ARTICLES:
        ARTICLES_IDS.append(ids.get_attribute('id'))
        ARTICLES_NAMES.append(ids.text)

    dict_ID_NAME_ARTICLES = {}
    for k in range(0, len(ARTICLES_IDS)):
        dict_ID_NAME_ARTICLES[ARTICLES_IDS[k]] = ARTICLES_NAMES[k]

    dict_art = {
        'Identifiant' : ARTICLES_IDS,
        'Nom' : ARTICLES_NAMES,
    }

    driver.close()

    #------#
    #DEUXIEME PARTIE : STOCKAGE DES ARTICLES
    #------#

    #Instanciation du navigateur web
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #Creation des liens menant vers les pages contenant les articles
    LIENS_VERS_ARTICLES = []
    LIEN_BASE = 'https://www.legifrance.gouv.fr/codes/article_lc/'
    for id in ARTICLES_IDS:
        lien = LIEN_BASE + str(id[3:len(id)])
        LIENS_VERS_ARTICLES.append(lien)

    #Stockage des articles (1 page web = 1 article)
    dict_ID_TEXT_ARTICLES = {}
    ARTICLES_TEXT = []
    for k in range(0, len(ARTICLES_IDS)):
        driver.get(LIENS_VERS_ARTICLES[k])
        ARTICLE = driver.find_element(By.CSS_SELECTOR, '#main > div > div.main-col > div.page-content.folding-element > article > div > div.content')
        dict_ID_TEXT_ARTICLES[ARTICLES_IDS[k]] = ARTICLE.text
        ARTICLES_TEXT.append(ARTICLE.text)

    driver.close()

    dict_id_text_art = {
        'Identifiant' : ARTICLES_IDS,
        'Article' : ARTICLES_TEXT
    }

    df_id_text_articles = pd.DataFrame.from_dict(dict_id_text_art).set_index('Identifiant')
    df_id_name_articles = pd.DataFrame.from_dict(dict_art).set_index('Identifiant')

    return df_id_text_articles, df_id_name_articles
    '''
    #------#
    #PREMIERE PARTIE : STOCKAGE DES ID ET NOMS DES ARTICLES
    #------#

    #instanciation de l'URL contenant l'arborescence des articles
    url_partie_legi = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072050/LEGISCTA000006132338/#LEGISCTA000006132338'
    url_partie_regl = 'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072050/LEGISCTA000018488235/#LEGISCTA000018532924'


    #instanciation du webdriver pour Chrome
    driver_legi = webdriver.Chrome(executable_path="chromedriver.exe")
    driver_regl = webdriver.Chrome(executable_path="chromedriver.exe")
    #driver_legi = webdriver.Chrome(ChromeDriverManager().install())
    #driver_regl = webdriver.Chrome(ChromeDriverManager().install())

    #Navigation des pages web pour trouver tous les articles 
    driver_legi.get(url_partie_legi)
    ARTICLES = driver_legi.find_elements(By.CLASS_NAME, "name-article")

    driver_regl.get(url_partie_regl)
    ARTICLES += driver_regl.find_elements(By.CLASS_NAME, "name-article")

    #Stockage des ids et noms des articles 
    ARTICLES_IDS = []
    ARTICLES_NAMES = []
    for ids in ARTICLES:
        ARTICLES_IDS.append(ids.get_attribute('data-anchor'))
        ARTICLES_NAMES.append(ids.text)

    driver_legi.close()
    driver_regl.close()

    dict_ID_NAME_ARTICLES = {}
    for k in range(0, len(ARTICLES_IDS)):
        dict_ID_NAME_ARTICLES[ARTICLES_IDS[k]] = ARTICLES_NAMES[k]

    
    #------#
    #DEUXIEME PARTIE : STOCKAGE DES ARTICLES
    #------#

    #Instanciation du navigateur web
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    #Creation des liens menant vers les pages contenant les articles
    LIENS_VERS_ARTICLES = []
    LIEN_BASE = 'https://www.legifrance.gouv.fr/codes/article_lc/'
    for id in ARTICLES_IDS:
        lien = LIEN_BASE + str(id)
        LIENS_VERS_ARTICLES.append(lien)

    #Stockage des articles (1 page web = 1 article)
    dict_ID_TEXT_ARTICLES = {}
    ARTICLES_TEXT = []
    for k in range(0, len(ARTICLES_IDS)):
        driver.get(LIENS_VERS_ARTICLES[k])
        ARTICLE = driver.find_element(By.CSS_SELECTOR, '#main > div > div.main-col > div.page-content.folding-element > article > div > div.content')
        dict_ID_TEXT_ARTICLES[ARTICLES_IDS[k]] = ARTICLE.text
        ARTICLES_TEXT.append(ARTICLE.text)

    driver.close()

    dict_id_text_art = {
        'Identifiant' : ARTICLES_IDS,
        'Article' : ARTICLES_TEXT,
        'Référence' : ARTICLES_NAMES
    }

    df_id_text_articles = pd.DataFrame.from_dict(dict_id_text_art).set_index('Identifiant')
    #df_id_name_articles = pd.DataFrame.from_dict(dict_art).set_index('Identifiant')

    return df_id_text_articles


'''
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data
'''

def to_excel(df: pd.DataFrame):
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()

def intersection(lst1, lst2):
    lst_intersection = [value for value in lst1 if value in lst2]
    return lst_intersection

def union(lst1, lst2):
    lst_union = list(set(lst1) | set(lst2))
    return lst_union    

def difference(lst1, lst2):
    s = set(lst2)
    lst_diff = [x for x in lst1 if x not in s]
    return lst_diff






