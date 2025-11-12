import streamlit as st
import fitz  # PyMuPDF
import io
import time

st.set_page_config(
    page_title="Processeur de Patrons PDF",
    page_icon="✂️",
    layout="wide"
)

st.title("✂️ Processeur de Patrons PDF")
st.markdown("Transformez vos PDFs de patrons en grille parfaite !")
st.markdown("*Développé par Siouldlh*")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Pages à extraire
    st.subheader("Pages à extraire")
    start_page = st.number_input("Page de début", min_value=1, value=1)
    end_page = st.number_input("Page de fin", min_value=1, value=1)
    
    # Paramètres de traitement
    st.subheader("Traitement")
    margin_cm = st.slider("Marge à supprimer (cm)", 0.0, 5.0, 1.0, 0.1)
    overlap_mm = st.slider("Chevauchement (mm)", 0.0, 10.0, 2.0, 0.5)
    
    # Configuration de la grille
    st.subheader("Grille")
    output_format = st.selectbox("Format de sortie", ["A0", "A1"], index=0, help="Choisissez le format de la page de sortie")
    orientation = st.selectbox("Orientation", ["Portrait", "Paysage"], index=0, help="Choisissez l'orientation de la page de sortie")
    grid_cols = st.number_input("Colonnes", min_value=1, max_value=10, value=4)
    grid_rows = st.number_input("Lignes", min_value=1, max_value=10, value=4)
    
    # Initialiser la sélection des cases dans la session state
    if 'grid_selection' not in st.session_state:
        st.session_state.grid_selection = {}
    
    # Réinitialiser si la taille de la grille change
    grid_key = f"{grid_rows}x{grid_cols}"
    if grid_key not in st.session_state.grid_selection:
        st.session_state.grid_selection[grid_key] = {}

# Zone principale
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📁 Upload du PDF")
    uploaded_file = st.file_uploader(
        "Choisissez votre fichier PDF de patron",
        type="pdf",
        help="Sélectionnez un fichier PDF contenant votre patron de couture"
    )

with col2:
    st.header("ℹ️ Instructions")
    st.markdown("""
    1. **Uploadez** votre PDF de patron
    2. **Ajustez** les paramètres dans la barre latérale
    3. **Sélectionnez** les cases de la grille ci-dessous
    4. **Cliquez** sur "Traiter le PDF"
    5. **Téléchargez** le résultat !
    """)

# Section pour sélectionner les cases de la grille
st.markdown("---")
st.header("🔲 Sélection des cases de la grille")
st.markdown("**Cochez les cases où vous voulez placer les pages (dans l'ordre de lecture : de gauche à droite, de haut en bas)**")

# Créer la grille de sélection
current_grid_key = f"{grid_rows}x{grid_cols}"
if current_grid_key not in st.session_state.grid_selection:
    st.session_state.grid_selection[current_grid_key] = {}

# Boutons pour sélectionner/désélectionner toutes les cases
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("✅ Sélectionner toutes les cases"):
        for row in range(grid_rows):
            for col in range(grid_cols):
                cell_key = f"{row}_{col}"
                st.session_state.grid_selection[current_grid_key][cell_key] = True
        st.rerun()
with col_btn2:
    if st.button("❌ Désélectionner toutes les cases"):
        for row in range(grid_rows):
            for col in range(grid_cols):
                cell_key = f"{row}_{col}"
                st.session_state.grid_selection[current_grid_key][cell_key] = False
        st.rerun()

# Créer une grille visuelle avec des checkboxes
grid_container = st.container()
with grid_container:
    selected_cells = []
    
    # En-têtes de colonnes
    header_cols = st.columns(grid_cols)
    for col in range(grid_cols):
        with header_cols[col]:
            st.markdown(f"**Col {col+1}**", help=f"Colonne {col+1}")
    
    # Créer les lignes avec checkboxes
    for row in range(grid_rows):
        cols = st.columns(grid_cols)
        
        for col in range(grid_cols):
            cell_key = f"{row}_{col}"
            
            # Initialiser si nécessaire
            if cell_key not in st.session_state.grid_selection[current_grid_key]:
                st.session_state.grid_selection[current_grid_key][cell_key] = False
            
            # Afficher le checkbox dans la bonne colonne
            with cols[col]:
                # Checkbox pour chaque case avec label plus clair
                checked = st.checkbox(
                    f"L{row+1}-C{col+1}",
                    value=st.session_state.grid_selection[current_grid_key][cell_key],
                    key=f"cell_{row}_{col}",
                    label_visibility="visible",
                    help=f"Case ligne {row+1}, colonne {col+1}"
                )
                st.session_state.grid_selection[current_grid_key][cell_key] = checked
                
                if checked:
                    selected_cells.append((row, col))

# Afficher le nombre de cases sélectionnées
st.info(f"📊 **{len(selected_cells)} case(s) sélectionnée(s)** sur {grid_rows * grid_cols} cases disponibles")

if uploaded_file is not None:
    # Afficher les informations du fichier
    st.success(f"✅ Fichier chargé : {uploaded_file.name}")
    
    # Initialiser la variable de session pour stocker le PDF traité
    if 'processed_pdf' not in st.session_state:
        st.session_state.processed_pdf = None
    if 'output_filename' not in st.session_state:
        st.session_state.output_filename = None
    
    # Bouton de traitement
    if st.button("🚀 Traiter le PDF", type="primary"):
        # Créer des conteneurs pour afficher les étapes une par une
        progress_container = st.container()
        
        try:
            # Lire le PDF uploadé
            pdf_bytes = uploaded_file.read()
            
            # Étape 1: Extraire les pages
            with progress_container:
                st.info("📄 Extraction des pages...")
            time.sleep(0.5)  # Petit délai pour voir l'étape
            
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            # Vérifier qu'on a des pages
            if len(doc) == 0:
                st.error("❌ Aucune page trouvée dans le PDF")
                st.stop()
            
            # Créer un nouveau document avec les pages sélectionnées
            pages_doc = fitz.open()
            for page_num in range(start_page - 1, end_page):
                if page_num < len(doc):
                    pages_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            
            doc.close()
            
            # Vérifier qu'on a des pages
            if len(pages_doc) == 0:
                st.error("❌ Aucune page trouvée dans la plage spécifiée")
                st.stop()
            
            # Étape 2: Supprimer les marges
            with progress_container:
                st.info("✂️ Suppression des marges...")
            time.sleep(0.5)  # Petit délai pour voir l'étape
            
            new_doc = fitz.open()
            
            margin_points = margin_cm * 28.346 + 10
            first_page = pages_doc[0]
            first_rect = first_page.rect
            standard_width = first_rect.width - (2 * margin_points)
            standard_height = first_rect.height - (2 * margin_points)
            
            for page_num in range(len(pages_doc)):
                page = pages_doc[page_num]
                rect = page.rect
                width = rect.width
                height = rect.height
                
                new_rect = fitz.Rect(
                    margin_points, margin_points,
                    width - margin_points, height - margin_points
                )
                
                new_page = new_doc.new_page(width=standard_width, height=standard_height)
                page.set_cropbox(new_rect)
                new_page.show_pdf_page(fitz.Rect(0, 0, standard_width, standard_height), pages_doc, page_num)
            
            pages_doc.close()
            
            # Étape 3: Créer la grille
            with progress_container:
                st.info("🔲 Création de la grille...")
            time.sleep(0.5)  # Petit délai pour voir l'étape
            
            pages_doc = new_doc
            first_page = pages_doc[0]
            page_width = first_page.rect.width
            page_height = first_page.rect.height
            
            output_doc = fitz.open()
            # Dimensions selon le format choisi
            # A0 : 841 x 1189 mm = 2384 x 3370 points (portrait)
            # A0 : 1189 x 841 mm = 3370 x 2384 points (paysage)
            # A1 : 594 x 841 mm = 1684 x 2384 points (portrait)
            # A1 : 841 x 594 mm = 2384 x 1684 points (paysage)
            if output_format == "A0":
                if orientation == "Portrait":
                    output_width = 2384
                    output_height = 3370
                else:  # Paysage
                    output_width = 3370
                    output_height = 2384
            else:  # A1
                if orientation == "Portrait":
                    output_width = 1684
                    output_height = 2384
                else:  # Paysage
                    output_width = 2384
                    output_height = 1684
            
            output_page = output_doc.new_page(width=output_width, height=output_height)
            
            # Calculer la taille totale nécessaire pour la grille
            total_width = grid_cols * page_width
            total_height = grid_rows * page_height
            
            # Calculer le facteur d'échelle optimal pour utiliser au mieux l'espace disponible
            # On utilise 95% de l'espace pour laisser une petite marge
            scale_x = (output_width * 0.95) / total_width
            scale_y = (output_height * 0.95) / total_height
            scale_factor = min(scale_x, scale_y)
            
            # Si la grille est trop grande, on réduit. Si elle est trop petite, on agrandit.
            if scale_factor < 1.0:
                st.warning(f"⚠️ La grille est trop grande pour le format {output_format}. Les pages ont été redimensionnées à {scale_factor*100:.1f}% pour qu'elles rentrent.")
            elif scale_factor > 1.0:
                st.info(f"ℹ️ La grille est agrandie à {scale_factor*100:.1f}% pour mieux remplir le format {output_format}.")
            
            # Ajuster les dimensions des pages
            page_width = page_width * scale_factor
            page_height = page_height * scale_factor
            
            # Recalculer la taille totale avec les nouvelles dimensions
            total_width = grid_cols * page_width
            total_height = grid_rows * page_height
            
            # Centrage
            margin_x = max(0, (output_width - total_width) / 2)
            margin_y = max(0, (output_height - total_height) / 2)
            
            overlap_points = overlap_mm * 2.834
            
            # Recalculer la clé de la grille pour être sûr qu'elle est à jour
            current_grid_key = f"{grid_rows}x{grid_cols}"
            
            # Récupérer les cases sélectionnées dans l'ordre (de gauche à droite, de haut en bas)
            selected_cells_ordered = []
            for row in range(grid_rows):
                for col in range(grid_cols):
                    cell_key = f"{row}_{col}"
                    if st.session_state.grid_selection.get(current_grid_key, {}).get(cell_key, False):
                        selected_cells_ordered.append((row, col))
            
            # Vérifier qu'il y a au moins une case sélectionnée
            if len(selected_cells_ordered) == 0:
                st.error("❌ Veuillez sélectionner au moins une case dans la grille")
                st.stop()
            
            # Vérifier qu'on a assez de pages
            if len(selected_cells_ordered) > len(pages_doc):
                st.warning(f"⚠️ Vous avez sélectionné {len(selected_cells_ordered)} cases mais seulement {len(pages_doc)} page(s) disponible(s). Seules les {len(pages_doc)} premières cases seront remplies.")
            
            # Placer les pages dans les cases sélectionnées
            page_index = 0
            for row, col in selected_cells_ordered:
                if page_index < len(pages_doc):
                    x = margin_x + col * page_width
                    y = margin_y + row * page_height
                    
                    dest_rect = fitz.Rect(
                        x - overlap_points, y - overlap_points,
                        x + page_width + overlap_points, 
                        y + page_height + overlap_points
                    )
                    
                    output_page.show_pdf_page(dest_rect, pages_doc, page_index)
                    page_index += 1
                else:
                    # Si on a fini toutes les pages, sortir de la boucle
                    break
            
            # Étape 4: Sauvegarder
            with progress_container:
                st.info("💾 Sauvegarde...")
            time.sleep(0.5)  # Petit délai pour voir l'étape
            
            output_bytes = output_doc.tobytes()
            output_doc.close()
            pages_doc.close()
            
            # Stocker le PDF traité dans la session
            st.session_state.processed_pdf = output_bytes
            orientation_short = "P" if orientation == "Portrait" else "L"
            st.session_state.output_filename = f"{uploaded_file.name.split('.')[0]}_{output_format}_{orientation_short}_sans_marges.pdf"
            st.session_state.output_format = f"{output_format} {orientation}"
            
            # Debug: Vérifier la taille du PDF
            st.write(f"🔍 **Debug:** PDF créé avec {len(output_bytes)} bytes")
            
            # Étape 5: Terminé
            with progress_container:
                st.success("✅ Traitement terminé !")
            
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement : {str(e)}")
            import traceback
            st.error(f"Détails de l'erreur : {traceback.format_exc()}")
    
    # Afficher le PDF traité directement dans la page
    if st.session_state.processed_pdf is not None:
        st.success("✅ **PDF traité avec succès !**")
        
        # Vérifier que le PDF n'est pas vide
        if len(st.session_state.processed_pdf) > 0:
            # Afficher le PDF directement dans la page
            st.markdown("---")
            st.markdown("### 📄 **Votre PDF traité est prêt !**")
            st.markdown("*Cliquez sur les trois points (⋮) en haut à droite du PDF pour le télécharger*")
            
            # Encoder en base64 pour l'affichage
            import base64
            b64_pdf = base64.b64encode(st.session_state.processed_pdf).decode()
            pdf_display = f"""
            <iframe src="data:application/pdf;base64,{b64_pdf}" 
                    width="100%" 
                    height="700" 
                    type="application/pdf"
                    style="border: 2px solid #ddd; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            </iframe>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Informations simples
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📁 Fichier", st.session_state.output_filename)
            with col2:
                st.metric("📊 Taille", f"{len(st.session_state.processed_pdf):,} bytes")
            with col3:
                st.metric("🔲 Grille", f"{grid_rows}×{grid_cols}")
            with col4:
                format_display = st.session_state.get('output_format', 'A0')
                st.metric("📐 Format", format_display)
                
        else:
            st.error("❌ Le PDF traité est vide. Veuillez retraiter le fichier.")
    else:
        st.info("ℹ️ Aucun PDF traité trouvé. Cliquez sur 'Traiter le PDF' d'abord.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for les passionnés de couture")
st.markdown("**Développé par Siouldlh**")
