import re

with open('/home/hans/Documentos/Tesis_Chatbot/data/raw/txt/2/Historia, Geografía y Economía/augusto_leguia.txt', 'r') as f:
    text = f.read()
    text_aux = re.sub(r'-\n+', '', text)
    print(text_aux)