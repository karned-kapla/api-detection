import json
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw

st.title("Visualisation des détections YOLO")

uploaded_image = st.file_uploader("Chargez une image", type=["jpg", "png", "jpeg"])
json_input = st.text_area("Collez le JSON des détections ici")

if uploaded_image and json_input:
    try:

        image = np.array(Image.open(uploaded_image))

        detections = json.loads(json_input)

        if "detection" in detections and "boxes" in detections["detection"]:

            boxes = detections["detection"]["boxes"]
            speed = detections["detection"].get("speed", {})

            st.subheader("Informations sur la vitesse :")
            st.write(f"- Pré-traitement : {speed.get('preprocess', 'N/A')} ms")
            st.write(f"- Inférence : {speed.get('inference', 'N/A')} ms")
            st.write(f"- Post-traitement : {speed.get('postprocess', 'N/A')} ms")

            image_with_boxes = Image.fromarray(image)
            draw = ImageDraw.Draw(image_with_boxes)

            for box in boxes:
                xmin = int(box["xmin"])
                ymin = int(box["ymin"])
                xmax = int(box["xmax"])
                ymax = int(box["ymax"])
                confidence = box.get("confidence", 0.0)
                label = box.get("name", "Unknown")

                draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=3)
                draw.text((xmin, ymin), f"{label} ({confidence:.2f})", fill="red")

            st.image(image_with_boxes, caption="Image avec détections", use_column_width=True)
        else:
            st.error("Le JSON ne contient pas de clé 'detection' ou 'boxes'.")
    except json.JSONDecodeError:
        st.error("Le JSON fourni est invalide.")
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
else:
    st.info("Chargez une image et collez le JSON des détections pour continuer.")
