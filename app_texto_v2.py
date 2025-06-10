import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

CHAT_FILE = "chat.csv"

# Função para carregar mensagens
def load_chat():
    try:
        return pd.read_csv(CHAT_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "user", "message"])
        df.to_csv(CHAT_FILE, index=False)
        return df

# Função para salvar mensagens
def save_chat(df):
    df.to_csv(CHAT_FILE, index=False)

st.title("Chat")

# Carrega chat
chat_data = load_chat()

# Mostra histórico do chat
st.write("### Histórico do Chat")
for idx, row in chat_data.iterrows():
    st.markdown(f"**{row['timestamp']} - {row['user']}:** {row['message']}")

st.write("---")

# Input usuário e mensagem
username = st.text_input("Seu nome", key="username")
message = st.text_input("Sua mensagem", key="message")

col1, col2, col3, col4 = st.columns((0.4, 0.6, 2, 0.48))

# Botão para ativar a câmera
with col3:
    camera_active = st.checkbox("Habilitar câmera")

if camera_active:
    img_file_buffer = st.camera_input("Tire uma foto")
    if img_file_buffer is not None:
        # Se quiser, pode salvar a imagem em disco:
        img_bytes = img_file_buffer.getvalue()
        img_filename = f"camera_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        with open(img_filename, "wb") as f:
            f.write(img_bytes)
        
        st.image(img_file_buffer, caption="Foto capturada", use_column_width=True)

        # Opcional: enviar a imagem como mensagem (exemplo: link para o arquivo salvo)
        if st.button("Enviar foto"):
            if username.strip() == "":
                st.warning("Digite seu nome antes de enviar.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_message = pd.DataFrame([{
                    "timestamp": timestamp,
                    "user": username,
                    "message": f"Foto: {img_filename}",
                }])
                chat_data = pd.concat([chat_data, new_message], ignore_index=True)
                save_chat(chat_data)
                st.rerun()

with col1:
    if st.button("Enviar"):
        if username.strip() == "" or message.strip() == "":
            st.warning("Digite nome e mensagem antes de enviar.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_message = pd.DataFrame([{
                "timestamp": timestamp,
                "user": username,
                "message": message,
            }])
            chat_data = pd.concat([chat_data, new_message], ignore_index=True)
            save_chat(chat_data)
            st.rerun()  # Recarrega a página para atualizar o chat

with col2:
    if st.button("Limpar chat"):
        chat_data = pd.DataFrame(columns=["timestamp", "user", "message"])
        save_chat(chat_data)
        st.rerun()

with col4:
    if st.button("Atualizar"):
        st.rerun()

# Rerun automático a cada 10 segundos
time.sleep(10)
st.rerun()
