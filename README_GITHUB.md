# ✂️ Processeur de Patrons PDF

**Développé par Siouldlh**

Transformez vos PDFs de patrons de couture en grille A0 parfaite, prête à imprimer !

## 🚀 Déploiement sur Streamlit Cloud

### Étapes rapides :

1. **Fork ce repository** ou créez un nouveau repository
2. **Uploadez les fichiers** :
   - `app_streamlit.py`
   - `requirements_streamlit.txt`
   - `.streamlit/config.toml`
3. **Déployez sur [share.streamlit.io](https://share.streamlit.io)**
4. **Partagez l'URL** avec vos amis !

## 📁 Fichiers nécessaires

```
patron-processor/
├── app_streamlit.py          # Application principale
├── requirements_streamlit.txt # Dépendances Python
├── .streamlit/
│   └── config.toml           # Configuration Streamlit
└── README.md                 # Ce fichier
```

## ⚙️ Configuration Streamlit Cloud

1. Aller sur [share.streamlit.io](https://share.streamlit.io)
2. Se connecter avec GitHub
3. Sélectionner le repository
4. **Repository** : `votre-username/patron-processor`
5. **Branch** : `main`
6. **Main file path** : `app_streamlit.py`
7. Cliquer **"Deploy!"**

## 🎯 Fonctionnalités

- ✅ **Upload de PDF** : Glisser-déposer simple
- ✅ **Paramètres ajustables** : Marge, chevauchement, grille
- ✅ **Traitement automatique** : Suppression des marges
- ✅ **Centrage intelligent** : Patron centré sur A0
- ✅ **Téléchargement** : PDF prêt à imprimer
- ✅ **Interface intuitive** : Aucune installation requise

## 📱 Utilisation

1. **Uploadez** votre PDF de patron
2. **Ajustez** les paramètres dans la barre latérale
3. **Cliquez** sur "Traiter le PDF"
4. **Téléchargez** le résultat !

## 🔧 Personnalisation

Pour personnaliser l'application :

```python
# Changer le titre
st.title("Votre Titre Personnalisé")

# Changer la signature
st.markdown("*Développé par Votre Nom*")
```

## 📞 Support

Pour toute question ou suggestion, contactez Siouldlh.

---

**Made with ❤️ for les passionnés de couture**
