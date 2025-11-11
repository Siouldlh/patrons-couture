# ✂️ Processeur de Patrons PDF

**Développé par Siouldlh**

Transformez vos PDFs de patrons de couture en grille A0 parfaite, prête à imprimer !

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://patrons-couture.streamlit.app)

## 🚀 Déploiement rapide

### Option 1 : Streamlit Cloud (Recommandé)
1. Fork ce repository
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter votre compte GitHub
4. Sélectionner ce repository
5. Cliquer "Deploy" !

### Option 2 : Déploiement local
```bash
git clone https://github.com/Siouldlh/patrons-couture.git
cd patrons-couture
pip install -r requirements.txt
streamlit run app_streamlit.py
```

## 🎯 Fonctionnalités

- ✅ **Upload de PDF** : Glisser-déposer simple
- ✅ **Paramètres ajustables** : Marge, chevauchement, grille personnalisable
- ✅ **Sélection de grille** : Choisissez la taille (ex: 5x5) et les cases à utiliser
- ✅ **Traitement automatique** : Suppression des marges
- ✅ **Centrage intelligent** : Patron centré sur A0
- ✅ **Téléchargement** : PDF prêt à imprimer
- ✅ **Interface intuitive** : Aucune installation requise

## 📱 Utilisation

1. **Uploadez** votre PDF de patron
2. **Ajustez** les paramètres dans la barre latérale :
   - Pages de début/fin
   - Marge à supprimer (0-5 cm)
   - Chevauchement (0-10 mm)
   - Taille de la grille (lignes × colonnes)
3. **Sélectionnez** les cases de la grille où placer les pages
4. **Cliquez** sur "Traiter le PDF"
5. **Téléchargez** le résultat !

## 🔧 Paramètres recommandés

- **Marge à supprimer** : 1.0 cm (par défaut)
- **Chevauchement** : 2.0 mm (par défaut)
- **Grille** : 4 colonnes × 4 lignes (par défaut)

## 📁 Structure du projet

```
patrons-couture/
├── app_streamlit.py          # Application web principale
├── requirements.txt          # Dépendances Python
├── .streamlit/
│   └── config.toml           # Configuration Streamlit
└── README.md                 # Documentation
```

## 🛠️ Technologies utilisées

- **Python 3.7+**
- **Streamlit** - Interface web
- **PyMuPDF (fitz)** - Manipulation PDF (version simplifiée)

## 📞 Support

Pour toute question ou suggestion, contactez Siouldlh.

---

**Made with ❤️ for les passionnés de couture**

*Développé par Siouldlh*