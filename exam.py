import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


st.markdown("""
    <h1 style='text-align: center; background-color: #FF6347; border-radius: 12px; margin-bottom: 2em; color: white; font-family: "Arial", sans-serif; padding: 20px; border-bottom: 4px solid #FF6347;'>
     <strong>Dashboard Interactif : Analyse du Marché Immobilier</strong>
    </h1>
""", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2c3e50;'>Exploration des tendances, des prix, et des caractéristiques des maisons ! </h3>", unsafe_allow_html=True)


try:
    df = pd.read_csv('data/AmesHousing.csv', sep=',')
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier : {e}")
    df = None 


if df is not None and st.sidebar.checkbox('Afficher le DataSet avant nettoyage'):
    st.markdown("""
        <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #8e44ad; border-bottom: 3px solid #8e44ad; padding-bottom: 5px;'> 
        DataSet avant nettoyage
        </h3>
    """, unsafe_allow_html=True)
    st.write(df.head())


if df is not None:
    valeur_manquantes = df.isnull().sum()/df.shape[0]
    valeur_manquantes = valeur_manquantes[valeur_manquantes > 0].sort_values(ascending=False)
    seuil = 0.66
    supp_colonnes = valeur_manquantes[valeur_manquantes > seuil].index
    df = df.drop(columns=supp_colonnes)

    
    df_num = df.select_dtypes(include=['int64', 'float64'])
    df_cat = df.select_dtypes(exclude=['int64', 'float64'])
    df_num = df_num.fillna(df_num.mean())
    df_cat = df_cat.fillna(df_cat.mode().iloc[0])

    df = pd.concat([df_num, df_cat], axis=1)


if df is not None and st.sidebar.checkbox('Afficher le DataSet après nettoyage'):
    st.markdown("""
        <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #27ae60; border-bottom: 3px solid #27ae60; padding-bottom: 5px;'> 
         DataSet après nettoyage 
        </h3>
    """, unsafe_allow_html=True)
    st.write(df.head())


if df is not None:
    st.sidebar.header("Filtres de Recherche 🔍")
    localisation = st.sidebar.multiselect("Sélectionnez la localisation", df['Neighborhood'].unique(), key='localisation')
    prix_min, prix_max = st.sidebar.slider("Plage de prix", int(df['SalePrice'].min()), int(df['SalePrice'].max()), (50000, 300000), key='prix')
    surface_min, surface_max = st.sidebar.slider("Surface habitable", int(df['Gr Liv Area'].min()), int(df['Gr Liv Area'].max()), (int(df['Gr Liv Area'].min()), int(df['Gr Liv Area'].max())), key='surface')
    year_min, year_max = st.sidebar.slider("Année de construction", int(df['Year Built'].min()), int(df['Year Built'].max()), (int(df['Year Built'].min()), int(df['Year Built'].max())), key='year')

  
    df_filtered = df[
        (df['Neighborhood'].isin(localisation)) &
        (df['SalePrice'].between(prix_min, prix_max)) &
        (df['Gr Liv Area'].between(surface_min, surface_max)) &
        (df['Year Built'].between(year_min, year_max))
    ]

   
    if df_filtered is not None and st.sidebar.checkbox('Afficher le DataSet filtré'):
        st.markdown("""
            <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #2980b9; border-bottom: 3px solid #2980b9; padding-bottom: 5px;'> 
             DataSet Filtré 
            </h3>
        """, unsafe_allow_html=True)
        st.dataframe(df_filtered.head())


if df is not None and st.sidebar.checkbox('Résumé Statistique'):
    st.markdown("""
        <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #8e44ad; border-bottom: 3px solid #8e44ad; padding-bottom: 5px;'> 
         Résumé Statistique 
        </h3>
    """, unsafe_allow_html=True)
    st.write(df.describe().T)


tabs = st.tabs(["Distribution des Prix de Vente", "Carte de Densité des Ventes", "Ventes par Années de Construction", "Carte de Chaleur des Corrélations", "Prediction des Prix"])


with tabs[0]:
    st.markdown("""
        <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #2ecc71;'> 
         Distribution des Prix de Vente 
        </h3>
    """, unsafe_allow_html=True)
    dat_p = df["SalePrice"]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(dat_p, bins=30, color='mediumvioletred', edgecolor='orange')
    ax.set_title("Répartition des prix", fontsize=16)
    ax.set_xlabel("Intervalles", fontsize=12)
    ax.set_ylabel("Fréquences", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)


with tabs[1]:
    st.markdown("""
        <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #2ecc71;'> 
         Carte de Densité des Ventes en fonction de la Surface Habitable 
        </h3>
    """, unsafe_allow_html=True)
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='Gr Liv Area', y="SalePrice", cmap='coolwarm', shade=True, thresh=0.05)
    plt.title('Carte de Densité des Ventes vs Surface Habitable', fontsize=16)
    plt.xlabel('Surface Habitable (Gr Liv Area)', fontsize=14)
    plt.ylabel('Prix de Vente (SalePrice)', fontsize=14)
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.close()


with tabs[2]:
    st.markdown("""
        <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #2ecc71;'> 
         Diagramme en barres des ventes par années de construction �
        </h3>
    """, unsafe_allow_html=True)
    vent_ann = df.groupby('Year Built')["SalePrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.bar(vent_ann['Year Built'], vent_ann["SalePrice"], color='teal')
    ax.set_title("Ventes par Années de Construction", fontsize=16)
    ax.set_xlabel("Année de Construction", fontsize=14)
    ax.set_ylabel("Vente Totale", fontsize=14)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)


with tabs[3]:
    st.markdown("""
        <h3 style='font-family: Arial, sans-serif; text-align: center; font-size: 26px; font-weight: bold; color: #2ecc71;'> 
         Heatmap des Corrélations 
        </h3>
    """, unsafe_allow_html=True)
    df_numeric = df.select_dtypes(include=['int64', 'float64'])
    df_numeric = df_numeric.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_numeric, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Carte de Chaleur des Corrélations", fontsize=16)
    st.pyplot(plt.gcf())
    plt.close()

with tabs[4]:
    st.markdown("##  Estimation du Prix de Vente ")
    st.write("Ajoutez les caractéristiques pour obtenir une estimation du prix de vente.")
    
    
    features = ['Gr Liv Area', 'Year Built', 'Overall Qual', 'Garage Cars']
    df_filtered = df[features + ['SalePrice']].dropna()

    
    X = df_filtered[features].values
    y = df_filtered['SalePrice'].values
    
    
    X_b = np.c_[np.ones((X.shape[0], 1)), X]
    
  
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

    
    st.markdown("###  Entrez les détails de la maison")
    col1, col2 = st.columns(2)
    with col1:
        surface = st.number_input(" Surface habitable (en pieds carrés)", min_value=int(df['Gr Liv Area'].min()), max_value=int(df['Gr Liv Area'].max()), value=1500, step=50)
        qualite = st.slider(" Qualité globale de la maison", min_value=1, max_value=10, value=5)
    with col2:
        annee = st.number_input(" Année de construction", min_value=int(df['Year Built'].min()), max_value=int(df['Year Built'].max()), value=2000)
        garage = st.selectbox(" Nombre de places de garage", options=df['Garage Cars'].unique())
    
    if st.button(" Prédire le Prix"):
        prediction = theta_best[0] + theta_best[1] * surface + theta_best[2] * annee + theta_best[3] * qualite + theta_best[4] * garage
        st.success(f" Prix estimé : **${prediction:,.2f}**")
    

    
