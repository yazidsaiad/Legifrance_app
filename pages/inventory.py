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
    #####################################################################################################################################################
    # HEADER DEFINITION
    # display image in the sidebar
    st.sidebar.image('https://www.patrimoineculturel.com/wp-content/uploads/2020/10/1200px-Logo_SNCF_R%C3%A9seau_2015.svg_.png', width = 250)

    # display images in separated columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image('images/Logo-legifrance-2020.svg.png',
        width = 400)
    with col3:
        st.image('https://www.tnpandyou.com/wp-content/uploads/2020/08/TNP-logo_1653x1006.png',
        width= 200)
    
    # display the project title with separators
    st.markdown("---")
    st.markdown("<h1 style='text-align: center; color: black; font-size : 30px;'>INTERFACE D'AUTOMATISATION DE VEILLE</h1>", unsafe_allow_html=True)
    st.markdown("---")

    #####################################################################################################################################################



    #####################################################################################################################################################
    #-----------#
    # INVENTORY # 
    #-----------#
    
    st.header("INVENTAIRE DES ARTICLES")

    # message to inform users about memory consumption 
    st.info("L'opération d'inventaire des articles sur Légifrance peut s'interrompre lors de son exécution \
            à cause de la consommation des ressources mémoires. Si tel est le cas, veuillez rappuyer sur le bouton d'inventaire.", icon="ℹ️")
    st.markdown("---")

    # dataframe for article storage
    df_articles_description = pd.DataFrame()
    articles_text = []

    # first part of inventory 
    st.info("Effectuez l'inventaire des articles :", icon="💡")
    inventaire = st.button("📝 INVENTAIRE DES ARTICLES ")


    if inventaire is True:
        # artciles inventory        
        # get ids and names 
        st.info("Récupération des identifiants des articles... ")
        ids, names = utils.get_ids_and_names()
        st.success("Récupération des identifiants terminée. ")

        # chuncked versions of lists
        chuncked_ids = utils.chunck_list(ids, batch_size=utils.BATCH_SIZE)

        # show progress of scraping
        progress_text = "Inventaire des articles en cours. "
        text_bar = st.progress(0, progress_text)

        # text storage
        progress_ = 0

        for batch in chuncked_ids:
            text_, unloaded_ids, = utils.get_articles(batch, timeout=utils.TIMEOUT)
            articles_text += text_
            progress_ += (len(batch) - len(unloaded_ids))
            text_bar.progress(progress_/len(ids), text=progress_text + str(progress_) + " Articles chargés sur " + str(len(ids)) + ".")

        
        # dataframe construction
        st.info("Finalisation de l'inventaire... ")
        total_unloaded_ids = []
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
        
        

   
