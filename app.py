import heapq
import os
import streamlit as st
import os


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


class BinaryTree:
    def __init__(self , value, freq):
          self.value = value
          self.freq = freq
          self.left = None
          self.right = None
    def __lt__(self , other):
         return self.freq < other.freq
    def __eq__(self , other):
         return self.freq == other.freq
          
class HuffmanCode:
    def __init__(self,path):
        self.path = path 
        self.__heap = []  # Min-Heap with binary tree nodes store in sorted order
        self.__code = {}  # Unique Representation code of Each char in text
        self.__reverse_code = {}  # Unique representation of key(bits) , values (char) 

    
    
    def __frequency_from_text(self , text):
            freq_dict = {}
            for ch  in text:
                if ch not in freq_dict:
                      freq_dict[ch] = 0
                freq_dict[ch] += 1
            return freq_dict

    def __Build_Heap(self , frequency_dict):
         for key in frequency_dict:
            freq = frequency_dict[key]
            node = BinaryTree(key , freq)
            heapq.heappush(self.__heap , node)

    def __Build_Binary_Tree(self):
        while len(self.__heap)>1:
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)

            sum = node1.freq + node2.freq
            newNode = BinaryTree(None, sum)
            newNode.left  = node1
            newNode.right = node2
            heapq.heappush(self.__heap , newNode)
        return 
    
    def __Build_Tree_Code_Helper(self , root , bits):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = bits
            self.__reverse_code[bits] = root.value
            return 
        self.__Build_Tree_Code_Helper(root.left , bits+'0')
        self.__Build_Tree_Code_Helper(root.right , bits+'1')

    def __Build_Tree_Code(self):
        root = heapq.heappop(self.__heap)
        self.__Build_Tree_Code_Helper(root , '')

    def __Build_Encoded_Text(self , text):
        encoded_text = ''
        for ch in text:
            encoded_text += self.__code[ch]
        return encoded_text
    
    def __Build_Padded_Text(self , encoded_text):
        padding_val = 8 - (len(encoded_text)%8)
        for i in range(padding_val):
            encoded_text += '0'
        padded_info = "{0:08b}".format(padding_val)
        padded_text = padded_info + encoded_text
        return padded_text

    def __Buid_Byte_Array(self , padded_text):
        array = []
        for i in range(0 , len(padded_text) , 8):
            byte = padded_text[i:i+8]
            array.append(int(byte,2))
        return array
    def __Remove_Padding(self , bit_string):
        padded_info = bit_string[:8]
        padding_value = int(padded_info , 2)
        bit_string = bit_string[8:]
        bit_string = bit_string[:-1*padding_value]
        return bit_string
    

    def __Decode_Text(self , text):
        current_bits = ''
        decoded_text = ''
        for char in text:
            current_bits += char 
            if current_bits in self.__reverse_code:
                decoded_text += self.__reverse_code[current_bits]
                current_bits = ''
        return decoded_text
    
    def compression(self):
        print("Compression of file starts....")

        # Access the file & extract the text from file.
        filename , fileextension = os.path.splitext(self.path)
        output_path = filename + "_compressed.bin"
        with open(self.path , 'r+') as f , open(output_path,'wb') as output:
            text = f.read()
            text = text.rstrip() # remove space
         
            # Calculate the frequncy of each character & store it in freq dictionary.
            frequency_dict = self.__frequency_from_text(text)

            # Min heap for two characters with minimum frequency.
            min_heap = self.__Build_Heap(frequency_dict)

            # Construct binary tree from min heap.
            self.__Build_Binary_Tree()
            

            # Construct unique code for each unique character & store it in dictionary.
            self.__Build_Tree_Code()

            # Construct encoded text.
            encoded_text = self.__Build_Encoded_Text(text)
            # Padding of Encoded text
            padded_text = self.__Build_Padded_Text(encoded_text)

            # Return binary file as output.
            bytes_array = self.__Buid_Byte_Array(padded_text)
         
            final_bytes = bytes(bytes_array)

            output.write(final_bytes)
        print("Compress Successfully")
        return output_path
    def decompression(self,input_path):
        filename , fileextension = os.path.splitext(input_path)
        filename = filename[:-11]
        output_path = filename +'_decompressed.txt'
        with open(input_path , "rb") as f , open(output_path , 'w') as output:
                bit_string = ''
                byte = f.read(1)
                # print(byte)
                while byte:
                    byte = ord(byte)  # hexadecimal to integer
                    # print("byte : " , byte)
                    bits = bin(byte)[2:].rjust(8 , '0') # int to binary (b'0111) ignore "b'" hence did slicing 2:
                    # print("bits : " , bits)
                    bit_string += bits
                    # print("bits_string : " , bit_string)
                    byte = f.read(1)
            
                text_after_removing_padding = self.__Remove_Padding(bit_string)
                decoded_text = self.__Decode_Text(text_after_removing_padding)
                print(decoded_text)
                output.write(decoded_text)
        return output
    

def fun(text):
    # path = input("Enter the path of File    ")
    obj  = HuffmanCode(text)
    compress_file = obj.compression()
    decompress_file = obj.decompression(compress_file)

    return compress_file , decompress_file


# 

uploaded_file = st.file_uploader("Upload a text file to compress", type=["txt"])
if uploaded_file is not None:
    file_path = "huffman.txt"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    c, d = fun(file_path)
    if btn1:
        st.sidebar.download_button("⬇️ Download  ⬇️", data=open(c, "rb"), file_name=os.path.basename(c))

    if btn2:
        output_path = d.name  # This assumes that `d` is an open file object returned from the decompression method
        with open(output_path, "r") as decompressed_file:
            decompressed_content = decompressed_file.read()
        # Provide the content for download
        st.sidebar.download_button("⬇️ Download  ⬇️", data=decompressed_content, file_name=os.path.basename(output_path))
        st.success("File decompressed successfully.")

