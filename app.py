import streamlit as st
import os
from Huffman_Coding import fun



st.set_page_config(
    page_title = "File Compression",
    page_icon= "📂",
)

st.sidebar.markdown('<p style="color: red;">Note: The uploaded text file should not contain any emoji.</p>', unsafe_allow_html=True)

st.title("Welcome to File Compression")


btn1 = st.sidebar.button("File Compression 📂")
btn2 = st.sidebar.button("File Decompression 📂")
btn_instructions = st.sidebar.button("How to Use❓🤔\nClick Me😊")
if btn_instructions:
        st.sidebar.info("Instructions:\n1. Upload a text file using the file uploader➡️.\n2. Click on 'File Compression' to compress the file⬆️.\n3. Click on 'File Decompression' to decompress the file.⬆️")

uploaded_file = st.file_uploader("Upload a text file to compress", type=["txt"])
if uploaded_file is not None:
    file_path = "huffman.txt"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.success("File compressed successfully.")
    st.info("⬅️ Click on 'File Compression' to download Compressed file.")
 
    if btn1:

        compressed_file, _ = fun(file_path)
        st.sidebar.download_button("⬇️ Download ⬇️ ", data=compressed_file, file_name=os.path.basename(compressed_file))

    if btn2:
        _, decompressed_file = fun(file_path)
        # st.write(decompressed_file)
        file_path = "decompress.txt"
        with open(file_path, "w") as f:
            f.write(decompressed_file)
        st.sidebar.download_button("⬇️ Download  ⬇️", data=decompressed_file, file_name=file_path)
        st.success("File decompressed successfully.")
# import streamlit as st
# import Huffman_Coding 

# st.set_page_config(
#     page_title="File Compression",
#     page_icon="📂",
# )

# st.sidebar.markdown('<p style="color: red;">Note: The uploaded text file should not contain any emoji.</p>', unsafe_allow_html=True)

# st.title("Welcome to File Compression")

# btn1 = st.sidebar.button("File Compression 📂")
# btn2 = st.sidebar.button("File Decompression 📂")
# btn_instructions = st.sidebar.button("How to Use❓🤔\nClick Me😊")
# if btn_instructions:
#     st.sidebar.info("Instructions:\n1. Upload a text file using the file uploader➡️.\n2. Click on 'File Compression' to compress the file⬆️.\n3. Click on 'File Decompression' to decompress the file.⬆️")

# uploaded_file = st.file_uploader("Upload a text file to compress", type=["txt"])
# if uploaded_file is not None:
#     # Convert the uploaded file to text
#     text = uploaded_file.read().decode("utf-8")

#     # Perform compression and decompression
#     compress_file, decompress_file = Huffman_Coding.fun(text)

#     if btn1:
#         st.sidebar.download_button("⬇️ Download ⬇️ ", data=compress_file, file_name="compressed_file.bin")

#     if btn2:
#         st.sidebar.download_button("⬇️ Download ⬇️", data=decompress_file, file_name="decompressed_file.txt")

#     st.success("File compressed and decompressed successfully.")
