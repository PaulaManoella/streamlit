import streamlit as st
import base64
from streamlit_option_menu import option_menu
from paginas import conhecimento_especifico, questionario_do_estudante, relatorio
from pathlib import Path
import base64

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
def get_base64_image(relative_path):
    base_path = Path(__file__).parent
    image_path = base_path / relative_path

    if not image_path.exists():
        st.error(f"❌ Imagem não encontrada: {image_path}")
        return ""

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
 
with st.sidebar:
    st.markdown("### Menu")  
    
    page = option_menu(
    menu_title=None,
    options=[
        "🏠 Página Inicial",
        "📊 Conhecimento Específico",
        "📝 Questionário do Estudante",
        "📥 Baixar Relatório"
    ],
    icons=["🏠","📊","📝","📥"],                 # sem ícones Bootstrap (só os emojis)
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
    """.format(logo_cpa_base64=get_base64_image("src/img/CPA_logo.jpg"), logo_proplan_base64=get_base64_image("src/img/PROPLAN_logo.jpg"), enade_base64=get_base64_image("src/img/enade_removed.png"), diavi_logo_base64=get_base64_image("src/img/DIAVI_logo.png")), unsafe_allow_html=True)
    
    # Seção de introdução
    st.markdown("""
    <div class="intro-card">
        <h2>Apresentação</h2>
        <div class="intro-content">
            <p>A CPA, em parceria com a DIAVI/PROPLAN, apresenta as análises descritivas dos microdados do Enade 2023, com o objetivo de auxiliar as coordenações na identificação de fragilidades para subdisiar ações corretivas e preventivas nos cursos de gradução.</p>
            <p>As análises compreendem os temas do <b>Componente Específico</b> da prova do Enade e as questões do <b>Questionário do Estudante</b>, relativas às dimensões <b>Organização Didático-pedagógica</b>, <b>Infraestrutura e Instalações Físicas</b> e <b>Oportunidade Ampliação da Formação Profissional</b>.</p>
            <p>Para visualizar as análises, utilize o menu lateral para navegar entre as páginas <b>Conhecimento Específico</b> e <b>Questionário do Estudante</b>. </p>
            <p>A análise referente ao Componente Específico da prova do Enade foi desenvolvida por <b>Cunha, Sales e Santos (2021)</b>, conforme apresentado no artigo disponível em: https://doi.org/10.5753/wei.2021.15912.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# identificação de fragilidades para subsidiar acçoes corretivs e preventivcas nos cursos de graduação
# de melhorias 

elif "Conhecimento Específico" in page:
    conhecimento_especifico.show_page()
    st.stop()
elif "Questionário do Estudante" in page:
    questionario_do_estudante.show_page()
    st.stop()
elif "Baixar Relatório" in page:
    relatorio.show_page()

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 CPA - DIAVI/PROPLAN. Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
