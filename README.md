###################################################################################################

                                ----Nom Complet: Marieme Gessy Gadiaga et Marie Claire Annick Coly


##############################################################################################################

Ce projet est une application intreactif qui nous permet de faire une analyse complete d'un marche immobilier,
pour cette analyse nous avons utiliser les donnees du fichier AmesHousing.csv.
Ansi, nous avons pu donc explorer, visualiser et analyser les tendances du marche immobilier a Ames a travers une application interactif produit grace a streamlit.

##################################################################################################

                      -- FONCTIONNALITEES PRINCIPALES

###################################################################################################

Notre application a comme fonctionnalite principal :
 
         * Explorer les donnees : charger les donnees avant et apres nettoyage,
                                  
        *  Filtrage de donnees : filtrer par plage de prix, surface habitable, localisation et anne de construction

        *  Visualisation dynamique : Histogramme, Carte de densite, Diagramme en barres, Heatmap de correlation

        *  Statistique Descriptive  

        * Prediction des prix : 

##################################################################################################
                          
                                -- ETAPES

##################################################################################################

        ----> Avant tout, il nous faut un environnement virtuel: grace au ce code :
                 
                 ===> python -m venv venv
        
        ----> Apres on active notre environnement virtuel grace a la commande :

                ===> source venv/Scripts/activate

        ----> Puis on installe les bibliotheques de python que l'on va utiliser :
          
               ===> pip install numpy pandas seaborn matplotlib streamlit

        ----> on va exporter tout les paquets installer dans un fichier requirement.txt :
           
              ===> pip freeze > requirement.txt

        ----> Ensuite on a creer un dossier data ou on va mettre notre fichier csv
        ----> Puis on pourra commencer a taper notre code dans un fichier python appeler exam.py
        ----> Enfin pour voir notre commande dans le terminal on tape la commande :

             ===> streamlit run exam.py (Sachant que exam est le nom de notre fichier python)
