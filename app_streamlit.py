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
st.markdown("Transformez vos PDFs de patrons en grille A0 parfaite !")
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
    grid_cols = st.number_input("Colonnes", min_value=1, max_value=10, value=4)
    grid_rows = st.number_input("Lignes", min_value=1, max_value=10, value=4)

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
    3. **Cliquez** sur "Traiter le PDF"
    4. **Téléchargez** le résultat !
    """)

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
            # Format A0 : 841 x 1189 mm = 2384 x 3370 points
            A0_width = 2384
            A0_height = 3370
            output_page = output_doc.new_page(width=A0_width, height=A0_height)
            
            # Centrage
            total_width = grid_cols * page_width
            total_height = grid_rows * page_height
            margin_x = max(0, (A0_width - total_width) / 2)
            margin_y = max(0, (A0_height - total_height) / 2)
            
            overlap_points = overlap_mm * 2.834
            
            page_index = 0
            for row in range(grid_rows):
                for col in range(grid_cols):
                    if page_index < len(pages_doc):
                        x = margin_x + col * page_width
                        y = margin_y + row * page_height
                        
                        # Debug: Afficher la position de chaque page
                        st.write(f"Page {page_index + 1}: Ligne {row + 1}, Colonne {col + 1} - Position ({x:.1f}, {y:.1f})")
                        
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
                if page_index >= len(pages_doc):
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
            st.session_state.output_filename = f"{uploaded_file.name.split('.')[0]}_A0_sans_marges.pdf"
            
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
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📁 Fichier", st.session_state.output_filename)
            with col2:
                st.metric("📊 Taille", f"{len(st.session_state.processed_pdf):,} bytes")
            with col3:
                st.metric("🔲 Grille", f"{grid_rows}×{grid_cols}")
                
        else:
            st.error("❌ Le PDF traité est vide. Veuillez retraiter le fichier.")
    else:
        st.info("ℹ️ Aucun PDF traité trouvé. Cliquez sur 'Traiter le PDF' d'abord.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for les passionnés de couture")
st.markdown("**Développé par Siouldlh**")
