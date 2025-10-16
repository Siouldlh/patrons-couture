#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traiter le PDF du patron de sac cabas
- Extrait les pages 8 à 22
- Supprime 1 cm de marge tout autour
- Assemble en grille 4x4 avec case vide en haut à droite
- Ajoute un carré test de 10cm x 10cm
- Exporte en A0 sans marges
"""

import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A0, A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import io
import fitz  # PyMuPDF pour la manipulation avancée des PDFs

def extract_pages_from_pdf(input_path, start_page, end_page):
    """Extrait les pages spécifiées du PDF"""
    print(f"Extraction des pages {start_page} à {end_page}...")
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Les pages sont indexées à partir de 0, donc on soustrait 1
    for page_num in range(start_page - 1, end_page):
        if page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
    
    return writer

def remove_margins_from_pdf(pdf_writer, margin_cm=1.0):
    """Supprime les marges spécifiées de chaque page du PDF et normalise les dimensions"""
    print(f"Suppression de {margin_cm} cm de marge...")
    
    # Ouvrir le PDF avec PyMuPDF pour une manipulation plus précise
    temp_pdf = io.BytesIO()
    pdf_writer.write(temp_pdf)
    temp_pdf.seek(0)
    
    doc = fitz.open(stream=temp_pdf.read(), filetype="pdf")
    new_doc = fitz.open()
    
    margin_points = margin_cm * 28.346  # Conversion cm en points (1 cm = 28.346 points)
    # Supprimer encore plus de marge pour éliminer les espaces
    margin_points += 10  # Ajouter 10 points supplémentaires
    
    # Calculer les dimensions standardisées basées sur la première page
    first_page = doc[0]
    first_rect = first_page.rect
    standard_width = first_rect.width - (2 * margin_points)
    standard_height = first_rect.height - (2 * margin_points)
    
    print(f"Dimensions standardisées: {standard_width} x {standard_height} points")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Obtenir les dimensions de la page
        rect = page.rect
        width = rect.width
        height = rect.height
        
        # Calculer le nouveau rectangle sans les marges
        new_rect = fitz.Rect(
            margin_points,  # x0
            margin_points,  # y0
            width - margin_points,  # x1
            height - margin_points   # y1
        )
        
        # Créer une nouvelle page avec les dimensions standardisées
        new_page = new_doc.new_page(width=standard_width, height=standard_height)
        
        # Modifier la cropBox de la page source pour supprimer les marges internes
        page.set_cropbox(new_rect)
        
        # Copier le contenu de la page originale dans le nouveau rectangle standardisé
        new_page.show_pdf_page(fitz.Rect(0, 0, standard_width, standard_height), doc, page_num)
    
    doc.close()
    return new_doc

def create_grid_layout(pages_doc, grid_cols=4, grid_rows=4):
    """Crée une grille avec les pages parfaitement collées, centrée sur la page A0"""
    print("Création de la grille 4x4...")
    
    # Calculer les dimensions de chaque cellule
    first_page = pages_doc[0]
    page_width = first_page.rect.width
    page_height = first_page.rect.height
    
    print(f"Dimensions de référence: {page_width} x {page_height} points")
    
    # Créer un nouveau document A0
    output_doc = fitz.open()
    output_page = output_doc.new_page(width=A0[0], height=A0[1])
    
    # Calculer les dimensions totales de la grille
    total_width = grid_cols * page_width
    total_height = grid_rows * page_height
    
    # Calculer les marges pour centrer la grille
    margin_x = (A0[0] - total_width) / 2
    margin_y = (A0[1] - total_height) / 2
    
    # S'assurer que les marges ne sont pas négatives
    margin_x = max(0, margin_x)
    margin_y = max(0, margin_y)
    
    print(f"Centrage: marge X={margin_x:.1f}, marge Y={margin_y:.1f}")
    
    # Positionner les pages dans la grille CENTRÉE
    page_index = 0
    for row in range(grid_rows):
        for col in range(grid_cols):
            # Laisser la case en haut à droite vide (row=0, col=3)
            if row == 0 and col == 3:
                continue
                
            if page_index < len(pages_doc):
                # Position centrée
                x = margin_x + col * page_width
                y = margin_y + row * page_height
                
                print(f"Page {page_index + 1}: position ({x:.1f}, {y:.1f}) - Ligne {row + 1}, Colonne {col + 1}")
                
                # POSITIONNEMENT AVEC 2MM DE CHEVAUCHEMENT
                overlap_mm = 6  # 2 mm = environ 6 points
                dest_rect = fitz.Rect(x - overlap_mm, y - overlap_mm, 
                                    x + page_width + overlap_mm, 
                                    y + page_height + overlap_mm)
                
                # Insérer la page avec chevauchement forcé
                output_page.show_pdf_page(dest_rect, pages_doc, page_index)
                page_index += 1
    
    return output_doc

def add_test_square(pdf_doc, square_size_cm=10):
    """Ajoute un carré test de 10cm x 10cm en haut à droite"""
    print(f"Ajout du carré test de {square_size_cm}cm...")
    
    square_size_points = square_size_cm * 28.346
    
    # Obtenir la page de sortie (la seule page du document)
    page = pdf_doc[0]
    page_width = page.rect.width
    page_height = page.rect.height
    
    # Position du carré en haut à droite (coin supérieur droit)
    square_x = page_width - square_size_points - 20  # 20 points de marge du bord droit
    square_y = page_height - square_size_points - 20  # 20 points de marge du bord supérieur
    
    # Dessiner le carré
    square_rect = fitz.Rect(square_x, square_y, square_x + square_size_points, square_y + square_size_points)
    page.draw_rect(square_rect, color=(0, 0, 0), width=2)
    
    # Ajouter le texte centré
    text_rect = fitz.Rect(square_x + 5, square_y + square_size_points/2 - 10, 
                         square_x + square_size_points - 5, square_y + square_size_points/2 + 10)
    
    # Insérer le texte
    page.insert_text((square_x + square_size_points/2, square_y + square_size_points/2), 
                    "Carré test – 10 cm", 
                    fontsize=8, 
                    color=(0, 0, 0))

def main():
    input_file = "/Users/louis/patrons/Patron_PDF_Sac_cabas_double_Lea_Pilea-dzepfb.pdf"
    output_file = "/Users/louis/patrons/Patron_Sac_A0_sans_marges.pdf"
    
    try:
        # 1. Extraire les pages 8 à 22
        print("=== Début du traitement ===")
        pdf_writer = extract_pages_from_pdf(input_file, 8, 22)
        
        # 2. Supprimer 1 cm de marge tout autour
        pages_doc = remove_margins_from_pdf(pdf_writer, 1.0)
        
        # 3. Créer la grille 4x4 avec case vide en haut à droite
        grid_doc = create_grid_layout(pages_doc)
        
        # 4. Sauvegarder le résultat (carré de test supprimé)
        print("Sauvegarde du fichier final...")
        grid_doc.save(output_file)
        grid_doc.close()
        pages_doc.close()
        
        print(f"=== Traitement terminé ===")
        print(f"Fichier de sortie : {output_file}")
        
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
