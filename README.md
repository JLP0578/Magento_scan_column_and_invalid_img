# Magento_scan_column_and_invalid_img

Le script permet de parcourir les produits en font prod, dev ou local.
Tous les produits simple & parent configurable de Magento, seront vérifié.

## Pourquoi ?

## Installation

### Basic

Télécharger et installer [Python3](https://www.python.org/downloads/).
Durant l'installation cocher la case `pip`

pur installer les extentions requis faites : `pip install -r requirements.txt`

## Utilisation

Il est necéssaire d'avoir `Python3`, `pip`, et les extentions requis pour lancer le script.

Vérifié, que votre projet fraîchement cloné a les dossier `logs` et `output`, vous devrez aussi copier le `.env_sample`, renommez le en `.env` et renseignez les éléments

Suivant le thème utiliser les selecteur CSS devrons être mis à jours


|      Option      | Description                                               | Type   |
| :----------------: | :---------------------------------------------------------- | -------- |
|      --env      | Environement que le script va utiliser pour faire le scan | string |
|     --stores     | Les `store_id` de vos stores à parcourir (ex: "1, 5, 7")   | string |
| -- nb_processing | Le nombre de process qui seront lancé pour chaque stores | int    |

Exécuter `py ./main.py` avec les options voulu pour lancer le script.
Il va vous demander sur quel environnement vous voulez qu'il travaille.

Si le script trouve une erreur, il va générer un fichier dans `output`, il vous restera plus qu'à le réparer 🛠️

## Le `.env`


| Nom               | Description                                              |
| ------------------- | ---------------------------------------------------------- |
| `PROD_HOST`       | **Ip** de la base de données de prod                    |
| `PROD_USER`       | **Utilisateur** de la base de données de prod           |
| `PROD_PASSWORD`   | **Mot de passe** de la base de données de prod          |
| `PROD_DATABASES`  | **Nom de la base**<br /> de la base de données de prod  |
| `DEV_HOST`        | **Ip** de la base de données de dev                     |
| `DEV_USER`        | **Utilisateur** de la base de données de dev            |
| `DEV_PASSWORD`    | **Mot de passe** de la base de données de dev           |
| `DEV_DATABASES`   | **Nom de la base**<br /> de la base de données de dev   |
| `LOCAL_HOST`      | **Ip** de la base de données du local                   |
| `LOCAL_USER`      | **Utilisateur** de la base de donnée du local           |
| `LOCAL_PASSWORD`  | **Mot de passe** de la base de données du local         |
| `LOCAL_DATABASES` | **Nom de la base**<br /> de la base de données du local |
| `EXCLUDE_STORE`   | **ID** des store a exclure (ex :`"0, 3, 5"`)             |
| `EXCLUDE_URI`     | **URI** des URI a exclure (ex :`"pieces-"`)              |
| `DOMAINE_ADMIN_URL`| **URL** du domaine admin pour faire un racoursi sur la page de modification du produit|

## Quelles seraient les vulnérabilités de l'outil ?

Les identifiants dans le .env et la connexion SSL, j'ai dû désactiver les erreurs pour le local
