import json
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw

st.title("Visualisation des détections YOLO")

uploaded_image = st.file_uploader("Chargez une image", type=["jpg", "png", "jpeg"])
json_input = st.text_area("Collez le JSON des détections ici")

if uploaded_image and json_input:
    try:
        # Charger l'image
        image = Image.open(uploaded_image)
        detections = json.loads(json_input)

        # Vérification de la structure du JSON
        if "boxes" not in detections:
            st.error("Le JSON ne contient pas de clé 'boxes'.")
        else:
            boxes = detections["boxes"]
            speed = detections.get("speed", {})

            # Affichage des informations de vitesse
            st.subheader("Informations sur la vitesse :")
            st.write(f"- **Pré-traitement** : {speed.get('preprocess', 'N/A')} ms")
            st.write(f"- **Inférence** : {speed.get('inference', 'N/A')} ms")
            st.write(f"- **Post-traitement** : {speed.get('postprocess', 'N/A')} ms")

            # Dessiner les boîtes sur l'image
            image_with_boxes = image.copy()
            draw = ImageDraw.Draw(image_with_boxes)

            for box in boxes:
                xmin = round(box["xmin"])
                ymin = round(box["ymin"])
                xmax = round(box["xmax"])
                ymax = round(box["ymax"])
                confidence = round(box.get("confidence", 0.0), 2)
                label = box.get("name", "Unknown")

                # Dessiner la boîte et ajouter le texte
                draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=3)
                draw.text((xmin, ymin), f"{label} ({confidence})", fill="red")

            # Afficher l'image modifiée
            st.image(image_with_boxes, caption="Image avec détections", use_column_width=True)

    except json.JSONDecodeError:
        st.error("Le JSON fourni est invalide.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
else:
    st.info("Chargez une image et collez le JSON des détections pour continuer.")