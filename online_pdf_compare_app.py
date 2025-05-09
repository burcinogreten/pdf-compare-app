
import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image, ImageChops
import io

st.set_page_config(page_title="PDF Görsel Karşılaştırıcı", layout="wide")
st.title("📄 PDF Karşılaştırıcı (Yan Yana Görsel)")

uploaded_files = st.file_uploader("PDF dosyalarınızı yükleyin (en fazla 10 tane)", type="pdf", accept_multiple_files=True)

if uploaded_files and len(uploaded_files) >= 2:
    file_names = [f.name for f in uploaded_files]
    file_dict = {f.name: f for f in uploaded_files}

    col1, col2 = st.columns(2)
    with col1:
        file1_name = st.selectbox("📂 Önceki Versiyon", file_names)
    with col2:
        file2_name = st.selectbox("📂 Yeni Versiyon", file_names, index=1)

    if file1_name != file2_name:
        if st.button("🔍 Karşılaştır"):
            pdf1 = file_dict[file1_name].read()
            pdf2 = file_dict[file2_name].read()

            st.subheader("🖼️ Sayfa 1 Görsel Karşılaştırması")
            try:
                img1 = convert_from_bytes(pdf1, first_page=1, last_page=1)[0]
                img2 = convert_from_bytes(pdf2, first_page=1, last_page=1)[0]

                # Boyutları eşitle
                img1 = img1.resize((1000, 1400))
                img2 = img2.resize((1000, 1400))

                diff = ImageChops.difference(img1, img2)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(img1, caption="Önceki Versiyon")
                with col2:
                    st.image(img2, caption="Yeni Versiyon")
                with col3:
                    st.image(diff, caption="Farklılıklar (1. Sayfa)")

            except Exception as e:
                st.error(f"Görsel karşılaştırma sırasında hata oluştu: {e}")
else:
    st.info("Lütfen karşılaştırmak için en az iki PDF dosyası yükleyin.")
