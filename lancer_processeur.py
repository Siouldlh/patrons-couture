#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement pour le processeur de patrons
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from patron_processor import main
    main()
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que toutes les dépendances sont installées:")
    print("pip install PyPDF2 reportlab Pillow PyMuPDF")
    input("Appuyez sur Entrée pour continuer...")
except Exception as e:
    print(f"Erreur: {e}")
    input("Appuyez sur Entrée pour continuer...")
