#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface simple pour traiter les PDFs de patrons
Permet de spécifier les pages à extraire et les paramètres de traitement
"""

import os
import sys
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
import io
from reportlab.lib.pagesizes import A0
from reportlab.lib.units import cm
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class PatronProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Processeur de Patrons PDF")
        self.root.geometry("600x500")
        
        # Variables
        self.input_file = tk.StringVar()
        self.start_page = tk.IntVar(value=1)
        self.end_page = tk.IntVar(value=1)
        self.margin_cm = tk.DoubleVar(value=1.0)
        self.overlap_mm = tk.DoubleVar(value=2.0)
        self.grid_cols = tk.IntVar(value=4)
        self.grid_rows = tk.IntVar(value=4)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Titre
        title_label = tk.Label(self.root, text="Processeur de Patrons PDF", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sélection du fichier
        file_frame = ttk.LabelFrame(main_frame, text="Fichier PDF", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Fichier PDF:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Parcourir", command=self.browse_file).grid(row=0, column=2)
        
        # Paramètres d'extraction
        extract_frame = ttk.LabelFrame(main_frame, text="Pages à extraire", padding="10")
        extract_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(extract_frame, text="Page de début:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(extract_frame, from_=1, to=1000, textvariable=self.start_page, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(extract_frame, text="Page de fin:").grid(row=0, column=2, sticky=tk.W)
        ttk.Spinbox(extract_frame, from_=1, to=1000, textvariable=self.end_page, width=10).grid(row=0, column=3, padx=5)
        
        # Paramètres de traitement
        process_frame = ttk.LabelFrame(main_frame, text="Paramètres de traitement", padding="10")
        process_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(process_frame, text="Marge à supprimer (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(process_frame, from_=0.0, to=5.0, increment=0.1, textvariable=self.margin_cm, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(process_frame, text="Chevauchement (mm):").grid(row=0, column=2, sticky=tk.W)
        ttk.Spinbox(process_frame, from_=0.0, to=10.0, increment=0.5, textvariable=self.overlap_mm, width=10).grid(row=0, column=3, padx=5)
        
        # Grille
        grid_frame = ttk.LabelFrame(main_frame, text="Configuration de la grille", padding="10")
        grid_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(grid_frame, text="Colonnes:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(grid_frame, from_=1, to=10, textvariable=self.grid_cols, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(grid_frame, text="Lignes:").grid(row=0, column=2, sticky=tk.W)
        ttk.Spinbox(grid_frame, from_=1, to=10, textvariable=self.grid_rows, width=10).grid(row=0, column=3, padx=5)
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Traiter le PDF", command=self.process_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quitter", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Zone de statut
        self.status_label = tk.Label(main_frame, text="Prêt", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=5)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier PDF",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Essayer de détecter le nombre de pages
            try:
                reader = PdfReader(filename)
                num_pages = len(reader.pages)
                self.end_page.set(num_pages)
                self.status_label.config(text=f"Fichier chargé: {num_pages} pages détectées")
            except Exception as e:
                self.status_label.config(text=f"Erreur lors du chargement: {str(e)}")
    
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update()
    
    def process_pdf(self):
        if not self.input_file.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF")
            return
        
        if self.start_page.get() > self.end_page.get():
            messagebox.showerror("Erreur", "La page de début doit être inférieure à la page de fin")
            return
        
        # Démarrer le traitement dans un thread séparé
        self.progress.start()
        thread = threading.Thread(target=self._process_pdf_thread)
        thread.daemon = True
        thread.start()
    
    def _process_pdf_thread(self):
        try:
            self.update_status("Début du traitement...")
            
            # Extraire les pages
            self.update_status("Extraction des pages...")
            pdf_writer = self.extract_pages_from_pdf(
                self.input_file.get(), 
                self.start_page.get(), 
                self.end_page.get()
            )
            
            # Supprimer les marges
            self.update_status("Suppression des marges...")
            pages_doc = self.remove_margins_from_pdf(pdf_writer, self.margin_cm.get())
            
            # Créer la grille
            self.update_status("Création de la grille...")
            grid_doc = self.create_grid_layout(
                pages_doc, 
                self.grid_cols.get(), 
                self.grid_rows.get(),
                self.overlap_mm.get()
            )
            
            # Carré de test supprimé pour un rendu plus propre
            
            # Sauvegarder
            self.update_status("Sauvegarde...")
            output_file = self.get_output_filename()
            grid_doc.save(output_file)
            grid_doc.close()
            pages_doc.close()
            
            self.progress.stop()
            self.update_status(f"Terminé! Fichier sauvé: {output_file}")
            messagebox.showinfo("Succès", f"Le fichier a été traité avec succès!\nSauvé sous: {output_file}")
            
        except Exception as e:
            self.progress.stop()
            self.update_status(f"Erreur: {str(e)}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite:\n{str(e)}")
    
    def get_output_filename(self):
        input_path = self.input_file.get()
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.dirname(input_path)
        return os.path.join(output_dir, f"{base_name}_A0_sans_marges.pdf")
    
    def extract_pages_from_pdf(self, input_path, start_page, end_page):
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page_num in range(start_page - 1, end_page):
            if page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        return writer
    
    def remove_margins_from_pdf(self, pdf_writer, margin_cm):
        temp_pdf = io.BytesIO()
        pdf_writer.write(temp_pdf)
        temp_pdf.seek(0)
        
        doc = fitz.open(stream=temp_pdf.read(), filetype="pdf")
        new_doc = fitz.open()
        
        margin_points = margin_cm * 28.346
        margin_points += 10  # Marge supplémentaire
        
        first_page = doc[0]
        first_rect = first_page.rect
        standard_width = first_rect.width - (2 * margin_points)
        standard_height = first_rect.height - (2 * margin_points)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            rect = page.rect
            width = rect.width
            height = rect.height
            
            new_rect = fitz.Rect(
                margin_points,
                margin_points,
                width - margin_points,
                height - margin_points
            )
            
            new_page = new_doc.new_page(width=standard_width, height=standard_height)
            page.set_cropbox(new_rect)
            new_page.show_pdf_page(fitz.Rect(0, 0, standard_width, standard_height), doc, page_num)
        
        doc.close()
        return new_doc
    
    def create_grid_layout(self, pages_doc, grid_cols, grid_rows, overlap_mm):
        first_page = pages_doc[0]
        page_width = first_page.rect.width
        page_height = first_page.rect.height
        
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
        
        overlap_points = overlap_mm * 2.834  # Conversion mm en points
        
        page_index = 0
        for row in range(grid_rows):
            for col in range(grid_cols):
                if page_index < len(pages_doc):
                    # Position centrée
                    x = margin_x + col * page_width
                    y = margin_y + row * page_height
                    
                    dest_rect = fitz.Rect(
                        x - overlap_points, 
                        y - overlap_points,
                        x + page_width + overlap_points, 
                        y + page_height + overlap_points
                    )
                    
                    output_page.show_pdf_page(dest_rect, pages_doc, page_index)
                    page_index += 1
        
        return output_doc
    
    def add_test_square(self, pdf_doc, square_size_cm=10):
        square_size_points = square_size_cm * 28.346
        page = pdf_doc[0]
        page_width = page.rect.width
        page_height = page.rect.height
        
        square_x = page_width - square_size_points - 20
        square_y = page_height - square_size_points - 20
        
        square_rect = fitz.Rect(square_x, square_y, square_x + square_size_points, square_y + square_size_points)
        page.draw_rect(square_rect, color=(0, 0, 0), width=2)
        
        page.insert_text(
            (square_x + square_size_points/2, square_y + square_size_points/2), 
            "Carré test – 10 cm", 
            fontsize=8, 
            color=(0, 0, 0)
        )

def main():
    root = tk.Tk()
    app = PatronProcessor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
