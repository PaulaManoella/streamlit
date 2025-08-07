import streamlit as st

# Dicionário com opções conectadas
opcoes = {
    "Frutas": ["Maçã", "Banana", "Laranja", "Manga"],
    "Animais": ["Cachorro", "Gato", "Papagaio", "Peixe"],
    "Cores": ["Vermelho", "Azul", "Verde", "Amarelo"]
}

st.title("Selectbox Conectados")

# Primeiro selectbox (categoria)
categoria = st.selectbox("Escolha uma categoria:", list(opcoes.keys()))

# Segundo selectbox (opções filtradas pela categoria)
item = st.selectbox(f"Escolha um item de {categoria}:", opcoes[categoria])

st.write(f"Você escolheu: **{item}** da categoria **{categoria}**.")