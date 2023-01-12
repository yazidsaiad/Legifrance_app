import streamlit as st
import pandas as pd
from datetime import datetime
import time
import utils


def app():
    
    st.sidebar.image('https://www.patrimoineculturel.com/wp-content/uploads/2020/10/1200px-Logo_SNCF_R%C3%A9seau_2015.svg_.png', width = 250)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image('https://www.dila.premier-ministre.gouv.fr/IMG/arton223.png',
        width = 400)
    with col3:
        st.image('https://www.tnpandyou.com/wp-content/uploads/2020/08/TNP-logo_1653x1006.png',
        width= 200)
    st.markdown("---")
    #st.title("INTERFACE D'AUTOMATISATION DE VEILLE")
    st.markdown("<h1 style='text-align: center; color: black; font-size : 30px;'>INTERFACE D'AUTOMATISATION DE VEILLE</h1>", unsafe_allow_html=True)
    st.markdown("---")

    st.header("INVENTAIRE DES ARTICLES")
    st.markdown("💡 Téléchargez l'inventaire des articles répertoriés sur Légifrance à cette date.")
    df_id_text_articles = pd.DataFrame()
    #df_id_name_articles = pd.DataFrame()
    inventaire = st.button("📝 EFFECTUER L'INVENTAIRE DES ARTICLES")
    if inventaire is True:
        st.markdown("❗️ Cette étape prend un certain temps. Afin d'optimiser le temps de calcul, branchez votre ordinateur sur un secteur et limitez le nombre d'applications ouvertes simultanément.")
        st.markdown("⌛ Inventaire des articles en cours...")
        df_id_text_articles = utils.scrap_articles()
        st.markdown("✅ Inventaire des articles terminé.")
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_id_text_articles)
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_legifrance_' + str(dt_string) + '.xlsx')
        #st.markdown("Liste des articles répertoriés :")
        #st.dataframe(df_id_name_articles.head(10))
        #st.markdown("Liste des textes :")
        #st.dataframe(df_id_text_articles.head(10))


    st.markdown("---")
    st.header("BILAN DES MODIFICATIONS DES ARTICLES")
    st.markdown("Le bilan des modifications des articles est effectué relativement à deux sauvegardes d'inventaire des articles.")
    
    st.markdown("💡 Veuillez charger l'inventaire qui va servir de référentiel au bilan des modifications :")
    uploaded_file_base = st.file_uploader("Choisissez un fichier")
    df_base_inventaire = pd.DataFrame()
    if uploaded_file_base is not None:
        df_base_inventaire = pd.read_excel(uploaded_file_base)
        df_base_inventaire = df_base_inventaire.set_index('Identifiant')
        st.dataframe(df_base_inventaire)


    st.markdown(" ")

    st.markdown("💡 Veuillez charger un nouvel inventaire :")
    uploaded_file_new = st.file_uploader("Choisissez un nouveau fichier")
    df_new_inventaire = pd.DataFrame()
    if uploaded_file_new is not None:
        df_new_inventaire = pd.read_excel(uploaded_file_new)
        df_new_inventaire = df_new_inventaire.set_index('Identifiant')
        st.dataframe(df_new_inventaire)

    base_list = list(df_base_inventaire.index)
    new_list = list(df_new_inventaire.index)
    
    if st.button("EFFECTUER L'INVENTAIRE DES MODIFICATIONS"):
        st.markdown("⌛ Bilan en cours...")
        
        #articles modifiés
        list_intersection = utils.intersection(base_list, new_list)
        nb_modif = 0
        list_id_modif = []
        for id in list_intersection:
            if list(df_base_inventaire.loc[id])[0] != list(df_new_inventaire.loc[id])[0]:
                list_id_modif.append(id)
                nb_modif += 1
        st.markdown("⚠️ " + str(nb_modif) + " article(s) modifié(s) depuis la dernière mise à jour :")
        st.dataframe(df_new_inventaire.loc[list_id_modif])
        #sauvegarde articles modifiés
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_new_inventaire.loc[list_id_modif])
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES MODIFIES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_articles_modifiés_' + str(dt_string) + '.xlsx')



        #articles supprimés
        list_supp = utils.difference(utils.union(base_list, new_list), new_list)
        st.markdown("⚠️ " + str(len(list_supp)) + " article(s) supprimé(s) depuis la dernière mise à jour :")
        st.dataframe(df_base_inventaire.loc[list_supp])
        #sauvegarde articles supprimés
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_base_inventaire.loc[list_supp])
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES SUPPRIMES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_articles_supprimés_' + str(dt_string) + '.xlsx')



        #articles ajoutés
        list_add = utils.difference(utils.union(base_list, new_list), base_list)
        st.markdown("⚠️ " + str(len(list_add)) + " article(s) ajouté(s) depuis la dernière mise à jour :")
        st.dataframe(df_new_inventaire.loc[list_add])
        #sauvergarde articles ajoutés
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_new_inventaire.loc[list_add])
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES AJOUTES",
                                    data = df_to_save ,
                                    file_name = 'inventaire_articles_ajoutés_' + str(dt_string) + '.xlsx')


        #articles abrogés
        list_abroges = []
        for ref in list(df_new_inventaire['Référence']):
            if 'abrogé' in ref:
                list_abroges.append(ref)
        df_abroges = pd.DataFrame (list_abroges, columns = ['Articles Abrogés'])
        st.markdown("⚠️ " + str(len(list_abroges)) + " article(s) abrogé(s) depuis la dernière mise à jour :")
        st.dataframe(df_abroges)
        #sauvegarde des références abrogés
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y_%Hh%Mmin%Ss")
        df_to_save = utils.to_excel(df_abroges)
        st.download_button(label = "📥 TELECHARGER L'INVENTAIRE DES ARTICLES ABROGES",
                                    data = df_to_save ,
                                    file_name = 'références_articles_abrogés_' + str(dt_string) + '.xlsx')

        st.markdown("✅ Bilan terminé.")






    



