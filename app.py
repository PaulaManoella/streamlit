import streamlit as st
import base64
from streamlit_option_menu import option_menu
from paginas import Conhecimento_Específico, Questionário_do_Estudante

st.set_page_config(
    page_title="Enade 2023 - Análises Descritivas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open('style/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Configuração da página
# Função para carregar e codificar imagem em base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Função para criar cards de navegação
def create_nav_card(title, description, icon_path=None, icon_emoji="📊"):
    icon_html = ""
    if icon_path:
        try:
            icon_base64 = get_base64_image(icon_path)
            if icon_base64:
                icon_html = f'<img src="data:image/png;base64,{icon_base64}" style="width: 30px; height: 30px;">'
            else:
                icon_html = f'<span style="font-size: 30px;">{icon_emoji}</span>'
        except:
            icon_html = f'<span style="font-size: 30px;">{icon_emoji}</span>'
    else:
        icon_html = f'<span style="font-size: 30px;">{icon_emoji}</span>'
    
    return f"""
    <div class="nav-card">
        <div class="card-icon">
            {icon_html}
        </div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """
    
with st.sidebar:
    # st.markdown("""
    # <button type="button" onclick="alert('Hello world!')">Click Me!</button>
    # """, unsafe_allow_html=True)
    page = option_menu(
    menu_title='Menu',
    options=[
        "🏠 Página Inicial",
        "📊 Conhecimento Específico",
        "📝 Questionário do Estudante"
    ],
    icons=["🏠","📊","📝"],                 # sem ícones Bootstrap (só os emojis)
    default_index=0,
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "transparent",
        },
        "nav-link": {
            "font-size": "17px",
            "color": "#4A4A4A",
            "padding": "8px 12px",
            "border-radius": "12px",
            "margin": "4px 0",
        },
        "icon": {
            "font-size": "18px",
            "margin-right": "8px",
        },
        "nav-link-selected": {
            "background-color": "rgb(209 223 255)",
            "font-weight": "700",
            "color": "#212121",
        },
        
        "icon bi-menu-up":{
            "display": "none",
        }
    },)
    st.write('Para baixar o relatório completo, primeiro selecione o Município e o Curso')
    st.button("Baixar relatório", type="primary")

# Conteúdo principal
if page == "🏠 Página Inicial":    
      # Seção Hero com logo
    st.markdown("""
    <div class="hero-section">
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_cpa_base64}" alt="ENADE 2023" style="max-width: 100%; height: auto; max-height: 60px; filter: drop-shadow(0 4px 6px -1px rgba(0, 0, 0, 0.1));">
            <img src="data:image/png;base64,{logo_proplan_base64}" style="max-height:42px;">
            <img src="data:image/png;base64,{diavi_logo_base64}" style="max-height:57px;">
        </div>
        <img src="data:image/png;base64,{enade_base64}" style="max-height:150px;">
    </div>
    """.format(logo_cpa_base64=get_base64_image("src/img/CPA_logo.jpg"), logo_proplan_base64=get_base64_image("src/img/PROPLAN_logo.jpg"), enade_base64=get_base64_image("src/img/enade_removed.PNG"), logo_diavi_base64=get_base64_image("src/img/DIAVI_logo.png"), diavi_logo_base64=get_base64_image("src/img/logo_diavi.png")), unsafe_allow_html=True)
    
    # Seção de introdução
    st.markdown("""
    <div class="intro-card">
        <h2>Apresentação</h2>
        <div class="intro-content">
            <p>A CPA, em parceria com a DIAVI/PROPLAN, apresenta as análises descritivas dos microdados do Enade 2023, com o objetivo de auxiliar as coordenações de curso na identificação de melhorias a serem implementadas na graduação.</p>
            <p>As análises compreendem os temas do <b>Componente Específico</b> da prova do Enade e as questões do <b>Questionário do Estudante</b>, relativas às dimensões <b>Organização Didático-pedagógica</b>, <b>Infraestrutura e Instalações Físicas</b> e <b>Oportunidade Ampliação da Formação Profissional</b>.</p>
            <p>Para visualizar as análises, utilize o menu lateral para navegar entre as páginas <b>Conhecimento Específico</b> e <b>Questionário do Estudante</b>. Em cada uma dessas páginas, você poderá <b>baixar o relatório completo</b> correspondente à <b>ambas análises</b>. Antes de realizar o download, <b>certifique-se de selecionar o Município e o Curso</b> desejado.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif "Conhecimento Específico" in page:
    Conhecimento_Específico.show_page()
    st.stop()
elif "Questionário do Estudante" in page:
    Questionário_do_Estudante.show_page()
    st.stop()

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 CPA - DIAVI/PROPLAN. Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
