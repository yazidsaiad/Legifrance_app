"""
This file contains the streamlit code of the project report page.
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
    st.sidebar.image('https://www.patrimoineculturel.com/wp-content/uploads/2020/10/1200px-Logo_SNCF_R%C3%A9seau_2015.svg_.png', 
                     width = 250)

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
    st.markdown("<h1 style='text-align: center; color: black; font-size : 30px;'>INTERFACE D'AUTOMATISATION DE VEILLE</h1>",
                unsafe_allow_html=True)
    st.markdown("---")

    st.header("BILAN DES MODIFICATIONS DES ARTICLES")
    st.info("Le bilan des modifications des articles est effectué relativement à deux sauvegardes d'inventaire des articles.", 
            icon="ℹ️")
    st.markdown('---')

    # load first articles inventory
    st.info("Veuillez charger l'inventaire qui va servir de référentiel au bilan des modifications :", 
            icon='💡')
    uploaded_file_base = st.file_uploader("Choisissez un fichier")
    df_base_inventaire = pd.DataFrame()
    if uploaded_file_base is not None:
        df_base_inventaire = pd.read_excel(uploaded_file_base)
        df_base_inventaire = df_base_inventaire.set_index('Identifiant')
        st.dataframe(df_base_inventaire)

    # load second articles inventory
    st.markdown(" ")
    st.info("Veuillez charger un nouvel inventaire :", icon='💡')
    uploaded_file_new = st.file_uploader("Choisissez un nouveau fichier")
    df_new_inventaire = pd.DataFrame()
    if uploaded_file_new is not None:
        df_new_inventaire = pd.read_excel(uploaded_file_new)
        df_new_inventaire = df_new_inventaire.set_index('Identifiant')
        st.dataframe(df_new_inventaire)

    base_list = list(df_base_inventaire.index)
    new_list = list(df_new_inventaire.index)
    
    if st.button("EFFECTUER L'INVENTAIRE DES MODIFICATIONS"):
        st.info("Bilan en cours...")
        
        # count modified articles
        list_intersection = utils.intersection(base_list, new_list)
        nb_modif = 0
        list_id_modif = []
        for id in list_intersection:
            if list(df_base_inventaire.loc[id])[0] != list(df_new_inventaire.loc[id])[0]:
                list_id_modif.append(id)
                nb_modif += 1
        st.info("⚠️ " + str(nb_modif) + " article(s) modifié(s) depuis la dernière mise à jour :")
        st.dataframe(df_new_inventaire.loc[list_id_modif])

        # modified articles backup
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_new_inventaire.loc[list_id_modif])
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES MODIFIES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_articles_modifiés_' + str(dt_string) + '.xlsx')

        # count deleted articles
        list_supp = utils.difference(utils.union(base_list, new_list), new_list)
        st.info("⚠️ " + str(len(list_supp)) + " article(s) supprimé(s) depuis la dernière mise à jour :")
        st.dataframe(df_base_inventaire.loc[list_supp])
        
        # deleted articles backup 
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_base_inventaire.loc[list_supp])
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES SUPPRIMES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_articles_supprimés_' + str(dt_string) + '.xlsx')

        # count new articles
        list_add = utils.difference(utils.union(base_list, new_list), base_list)
        st.info("⚠️ " + str(len(list_add)) + " article(s) ajouté(s) depuis la dernière mise à jour :")
        st.dataframe(df_new_inventaire.loc[list_add])

        # new artciles backup
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_new_inventaire.loc[list_add])
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES AJOUTES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_articles_ajoutés_' + str(dt_string) + '.xlsx')

        # count revoked articles 
        list_abroges_new = []       
        for ref in list(df_new_inventaire['Référence']):
            if 'abrogé' in ref:
                list_abroges_new.append(ref)
        list_abroges_base = []
        for ref in list(df_base_inventaire['Référence']):
            if 'abrogé' in ref:
                list_abroges_base.append(ref)
        list_abroges = utils.difference(list_abroges_new, list_abroges_base)
        df_abroges = pd.DataFrame(list_abroges, columns = ['Articles Abrogés'])
        st.info("⚠️ " + str(len(list_abroges)) + " article(s) abrogé(s) depuis la dernière mise à jour :")
        st.dataframe(df_abroges)

        # revoked articles backup 
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_abroges)
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES ABROGES ENTRE LES DATES DES DEUX INVENTAIRES",
                                    data = df_to_save ,
                                    file_name = 'références_articles_abrogés_' + str(dt_string) + '.xlsx')
        
        # revoked articles counted at the date corresponding to the second inventory
        list_revoked = []       
        for ref in list(df_new_inventaire['Référence']):
            if 'abrogé' in ref:
                list_revoked.append(ref)
        df_revoked = pd.DataFrame(list_revoked, columns = ['Articles Abrogés'])
        st.info("⚠️ " + str(len(list_revoked)) + " article(s) abrogé(s) au dernier inventaire :")
        st.dataframe(df_revoked)

        # revoked articles at the date corresponding to the second inventory backup 
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_revoked)
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DE TOUS LES ARTICLES ABROGES A LA DERNIERE DATE",
                                    data = df_to_save ,
                                    file_name = 'tous_les_articles_abrogés_' + str(dt_string) + '.xlsx')
        


        st.success("Bilan terminé.")