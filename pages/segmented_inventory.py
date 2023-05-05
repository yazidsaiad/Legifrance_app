"""
This file contains the streamlit code of the project inventory page.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import utils


def app():

    """
    This function generates the project features using streamlit library.
    
    """

    # display image in the sidebar
    st.sidebar.image('https://www.patrimoineculturel.com/wp-content/uploads/2020/10/1200px-Logo_SNCF_R%C3%A9seau_2015.svg_.png', width = 250)

    # display images in separated columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/fr/e/e7/Logo-legifrance-2020.svg',
        width = 400)
    with col3:
        st.image('https://www.tnpandyou.com/wp-content/uploads/2020/08/TNP-logo_1653x1006.png',
        width= 200)
    
    # display the project title with separators
    st.markdown("---")
    st.markdown("<h1 style='text-align: center; color: black; font-size : 30px;'>INTERFACE D'AUTOMATISATION DE VEILLE</h1>", unsafe_allow_html=True)
    st.markdown("---")

    #-----------#
    # INVENTORY # 
    #-----------#
    
    st.header("INVENTAIRE DES ARTICLES")

    # message to inform users about memory consumption 
    st.info("Afin d'optimier les ressources mémoires utilisées, l'opération d'inventaire des articles sur Légifrance \
            doit être effectuée en deux parties.", icon="ℹ️")
    st.markdown("---")

    # dataframe for article storage
    df_articles_description = pd.DataFrame()
    articles_text = []

    # first part of inventory 
    st.info("Effectuez la première partie de l'inventaire des articles :", icon="💡")
    inventaire_legi = st.button("📝 EFFECTUER L'INVENTAIRE DES ARTICLES 1/2")


    if inventaire_legi is True:
        # artciles inventory        
        # get ids and names 
        st.info("Récupération des identifiants des articles... ")
        ids, names = utils.get_ids_and_names()
        st.success("Récupération des identifiants terminée. ")

        # cut ids list and names into half
        ids_left = ids[:int(len(ids)/2)]
        #names_left = names[:int(len(names)/2)]

        # chuncked versions of lists
        chuncked_ids = utils.chunck_list(ids_left, batch_size=utils.BATCH_SIZE)

        # show progress of scraping
        progress_text = "Inventaire des articles en cours. "
        text_bar = st.progress(0, progress_text)

        # text storage
        progress_ = 0

        for batch in chuncked_ids:
            text_, unloaded_ids, = utils.get_articles(batch, timeout=utils.TIMEOUT)
            articles_text += text_
            progress_ += (len(batch) - len(unloaded_ids))
            text_bar.progress(progress_/len(ids_left), text=progress_text + str(progress_) + " Articles chargés sur " + str(len(ids_left)) + ".")

        # text storage
        st.experimental_set_query_params(my_saved_result=articles_text)
        st.success("Première inventaire des articles terminé.")


    # second part of inventory
    st.markdown("---")
    st.info("Effectuez la deuxième partie de l'inventaire des articles :", icon="💡")
    inventaire_regu = st.button("📝 EFFECTUER L'INVENTAIRE DES ARTICLES 2/2")
    
    # for text storage
    app_state = st.experimental_get_query_params()  

    if inventaire_regu is True:
        # artciles inventory        
        # get ids and names 
        st.info("Récupération des identifiants des articles... ")
        ids, names = utils.get_ids_and_names()
        st.success("Récupération des identifiants terminée. ")

        # cut ids list and names into half
        ids_right = ids[int(len(ids)/2):]
        #names_right = names[int(len(names)/2):]

        # chuncked versions of lists
        chuncked_ids = utils.chunck_list(ids_right, batch_size=utils.BATCH_SIZE)

        # show progress of scraping
        progress_text = "Inventaire des articles en cours. "
        text_bar = st.progress(0, progress_text)

        # text storage
        progress_ = 0
        articles_text = app_state["my_saved_result"]

        for batch in chuncked_ids:
            text_, unloaded_ids, = utils.get_articles(batch, timeout=utils.TIMEOUT)
            articles_text += text_
            progress_ += (len(batch) - len(unloaded_ids))
            text_bar.progress(progress_/len(ids_right), text=progress_text + str(progress_) + " Articles chargés sur " + str(len(ids_right)) + ".")
            
        st.success("Deuxième inventaire des articles terminé.")
        
        
        # dataframe construction
        total_unloaded_ids = []
        st.info("Finalisation de l'inventaire... ")
        ids, names = utils.get_ids_and_names()
        for id in range(0, len(articles_text)):
            if articles_text[id] == "ERREUR DE CHARGEMENT DE L'ARTCILE":
                total_unloaded_ids.append(ids[id])
        

        # unloaded articles
        ids_string = " "
        for id in total_unloaded_ids:
            ids_string += str(id)
            ids_string += " "
        # display unloaded articles
        if len(ids_string) != 0:
            st.warning( "Articles dont le chargement a échoué : " + ids_string)
        df_articles_description = utils.get_inventory_description(ids=ids, text=articles_text, names=names)
        st.success("Inventaire terminé.")
        st.balloons()


        # artciles backup 
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_articles_description)
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_legifrance_' + str(dt_string) + '.xlsx')
        

   
