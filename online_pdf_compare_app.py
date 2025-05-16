import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image, ImageChops, ImageDraw
from datetime import date
import numpy as np

st.set_page_config(page_title="PDF Görsel Karşılaştırıcı", layout="wide")
st.title("📄 PDF Görsel Karşılaştırıcı (Görsel + Notlar + Tarih + Görünüm Seçimi)")

uploaded_files = st.file_uploader("PDF dosyalarınızı yükleyin (en fazla 10 tane)", type="pdf", accept_multiple_files=True)

if uploaded_files and len(uploaded_files) >= 2:
    file_names = [f.name for f in uploaded_files]
    file_dict = {f.name: f for f in uploaded_files}

    col1, col2 = st.columns(2)
    with col1:
        file1_name = st.selectbox("📂 Önceki Versiyon", file_names)
    with col2:
        file2_name = st.selectbox("📂 Yeni Versiyon", file_names, index=1)

    st.markdown("---")
    st.subheader("📝 Notlar ve Revizyon Tarihi")
    selected_date = st.date_input("📅 Revizyon Tarihi", value=date.today())
    notes = st.text_area("📌 Notlarınızı yazın")

    st.markdown("---")
    view_option = st.radio("🖼️ Görüntüleme Şekli", ["Yan Yana", "Üst Üste"], horizontal=True)
    highlight_option = st.checkbox("🔴 Farklılıkları vurgula", value=True)

    if file1_name and file2_name and file1_name != file2_name:
        if st.button("🔍 Karşılaştır"):
            try:
                pdf1 = file_dict[file1_name].getvalue()
                pdf2 = file_dict[file2_name].getvalue()

                img1 = convert_from_bytes(pdf1, first_page=1, last_page=1, dpi=200)[0].convert("RGB")
                img2 = convert_from_bytes(pdf2, first_page=1, last_page=1, dpi=200)[0].convert("RGB")

                max_width = 800
                ratio = min(max_width / img1.width, max_width / img2.width)
                new_size = (int(img1.width * ratio), int(img1.height * ratio))
                img1 = img1.resize(new_size)
                img2 = img2.resize(new_size)

                diff = ImageChops.difference(img1, img2)
                highlighted = img2.copy()

                if highlight_option:
                    diff_array = np.array(diff)
                    if np.any(diff_array > 0):
                        bbox = diff.getbbox()
                        if bbox:
                            draw = ImageDraw.Draw(highlighted)
                            draw.rectangle(bbox, outline="red", width=3)
                    else:
                        st.success("✅ Fark bulunamadı.")

                st.markdown("---")
                if view_option == "Yan Yana":
                    col1, col2, col3 = st.columns(3)
                    col1.image(img1, caption="Önceki Versiyon")
                    col2.image(img2, caption="Yeni Versiyon")
                    if highlight_option:
                        col3.image(highlighted, caption="Farklılıklar")
                else:
                    st.image(img1, caption="Önceki Versiyon")
                    st.image(img2, caption="Yeni Versiyon")
                    if highlight_option:
                        st.image(highlighted, caption="Farklılıklar")

                st.markdown("---")
                st.success(f"🗓️ Tarih: {selected_date}  \n📝 Not: {notes if notes else 'Not girilmedi'}")

            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")
else:
    st.info("Karşılaştırma için en az 2 PDF yükleyin.")
