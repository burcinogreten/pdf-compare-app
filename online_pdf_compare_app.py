import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image, ImageChops, ImageDraw
import io
from datetime import date
from PyPDF2 import PdfReader

st.set_page_config(page_title="PDF Görsel Karşılaştırıcı", layout="wide")
st.title("📄 PDF Karşılaştırıcı (Sayfa Seçimli + Notlar + Görünüm)")

uploaded_files = st.file_uploader("PDF dosyalarınızı yükleyin (en fazla 10 tane)", type="pdf", accept_multiple_files=True)

if uploaded_files and len(uploaded_files) >= 2:
    file_names = [f.name for f in uploaded_files]
    file_dict = {f.name: f for f in uploaded_files}

    col1, col2 = st.columns(2)
    with col1:
        file1_name = st.selectbox("📂 Önceki Versiyon", file_names)
    with col2:
        file2_name = st.selectbox("📂 Yeni Versiyon", file_names, index=1)

    # Sayfa seçimi
    try:
        pdf1_reader = PdfReader(file_dict[file1_name])
        pdf2_reader = PdfReader(file_dict[file2_name])
        max_pages = min(len(pdf1_reader.pages), len(pdf2_reader.pages))
        selected_page = st.number_input("📄 Karşılaştırılacak Sayfa Numarası", min_value=1, max_value=max_pages, value=1)
    except:
        st.warning("Sayfa sayısı alınamadı. Dosyaları yeniden yükleyin.")
        selected_page = 1

    st.markdown("---")
    st.subheader("📝 Notlar ve Revizyon Tarihi")
    selected_date = st.date_input("📅 Revizyon Tarihi", value=date.today())
    notes = st.text_area("📌 Notlarınızı yazın (örneğin: ne değişti, kim yaptı)")

    st.markdown("---")
    view_option = st.radio("🖼️ Görüntüleme Şekli", ["Yan Yana", "Üst Üste"], horizontal=True)

    if file1_name != file2_name:
        if st.button("🔍 Karşılaştır"):
            pdf1 = file_dict[file1_name].read()
            pdf2 = file_dict[file2_name].read()

            st.subheader(f"🖼️ Sayfa {selected_page} Görsel Karşılaştırması")
            try:
                img1 = convert_from_bytes(pdf1, first_page=selected_page, last_page=selected_page)[0].convert("RGB")
                img2 = convert_from_bytes(pdf2, first_page=selected_page, last_page=selected_page)[0].convert("RGB")

                # Boyutları eşitle
                img1 = img1.resize((1000, 1400))
                img2 = img2.resize((1000, 1400))

                diff = ImageChops.difference(img1, img2)

                # Farkları işaretle
                bbox = diff.getbbox()
                highlighted = img2.copy()
                if bbox:
                    draw = ImageDraw.Draw(highlighted)
                    draw.rectangle(bbox, outline="red", width=5)

                if view_option == "Yan Yana":
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.image(img1, caption="Önceki Versiyon")
                    with col2:
                        st.image(img2, caption="Yeni Versiyon")
                    with col3:
                        st.image(highlighted, caption="Farklılıklar (Kırmızıyla İşaretli)")
                else:
                    st.image(img1, caption="Önceki Versiyon")
                    st.image(img2, caption="Yeni Versiyon")
                    st.image(highlighted, caption="Farklılıklar (Kırmızıyla İşaretli)")

                # Not ve tarih bilgisi
                st.markdown("---")
                st.success(f"🗓️ Tarih: {selected_date}  \n📝 Not: {notes if notes else 'Not girilmedi'}")

            except Exception as e:
                st.error(f"Görsel karşılaştırma sırasında hata oluştu: {e}")
else:
    st.info("Lütfen karşılaştırmak için en az iki PDF dosyası yükleyin.")
