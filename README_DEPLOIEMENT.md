# 🚀 Guide de Déploiement - Processeur de Patrons PDF

## Options d'hébergement gratuites

### 1. 🌟 Streamlit Cloud (Recommandé)

**Avantages :**
- ✅ Gratuit et illimité
- ✅ Déploiement en 1 clic depuis GitHub
- ✅ Interface web automatique
- ✅ Gestion des fichiers intégrée

**Étapes :**

1. **Créer un compte GitHub** (si pas déjà fait)
2. **Créer un nouveau repository** : `patron-processor`
3. **Uploader les fichiers** :
   - `app_streamlit.py`
   - `requirements_streamlit.txt`
   - `README.md`

4. **Déployer sur Streamlit Cloud** :
   - Aller sur [share.streamlit.io](https://share.streamlit.io)
   - Se connecter avec GitHub
   - Sélectionner le repository
   - Cliquer "Deploy"

**URL finale :** `https://votre-app.streamlit.app`

---

### 2. 🐍 PythonAnywhere

**Avantages :**
- ✅ Gratuit (limité)
- ✅ Support Python complet
- ✅ Base de données incluse

**Étapes :**
1. Créer un compte sur [pythonanywhere.com](https://pythonanywhere.com)
2. Créer une nouvelle app web
3. Uploader les fichiers
4. Installer les dépendances
5. Configurer l'URL

---

### 3. ☁️ Heroku

**Avantages :**
- ✅ Très populaire
- ✅ Déploiement via Git
- ✅ Add-ons disponibles

**Étapes :**
1. Créer un compte Heroku
2. Installer Heroku CLI
3. Créer `Procfile` :
   ```
   web: streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0
   ```
4. Déployer avec `git push heroku main`

---

### 4. 🆓 Render

**Avantages :**
- ✅ Gratuit
- ✅ Déploiement automatique
- ✅ Interface simple

**Étapes :**
1. Créer un compte sur [render.com](https://render.com)
2. Connecter le repository GitHub
3. Sélectionner "Web Service"
4. Configurer :
   - Build Command : `pip install -r requirements_streamlit.txt`
   - Start Command : `streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0`

---

## 🎯 Recommandation : Streamlit Cloud

**Pourquoi Streamlit Cloud ?**
- **Simplicité** : Déploiement en 5 minutes
- **Gratuit** : Aucune limite de temps
- **Fiable** : Service professionnel
- **Intégration** : Parfait pour les apps Python

## 📋 Checklist de déploiement

- [ ] Compte GitHub créé
- [ ] Repository créé avec les fichiers
- [ ] Compte Streamlit Cloud créé
- [ ] App déployée et testée
- [ ] URL partagée avec vos amis

## 🔧 Personnalisation

**Changer le nom de l'app :**
```python
st.set_page_config(
    page_title="Votre Nom - Processeur de Patrons",
    page_icon="✂️"
)
```

**Ajouter votre logo :**
```python
st.image("votre_logo.png", width=200)
```

## 📱 Partage

Une fois déployé, partagez simplement l'URL avec vos amis :
`https://votre-app.streamlit.app`

Ils pourront :
- Uploader leurs PDFs
- Ajuster les paramètres
- Télécharger le résultat
- Tout gratuitement !
