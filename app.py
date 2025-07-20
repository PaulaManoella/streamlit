import streamlit as st

st.set_page_config(
    page_title="Enade 2023 - Análises Descritivas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO
from streamlit_option_menu import option_menu
from main import UFPA_data
from paginas import Conhecimento_Específico, Questionário_do_Estudante

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
    
# # CSS customizado inspirado no design original
# st.markdown("""
# <style>
#     /* Importar fonte Inter */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
#     /* Variáveis CSS */
#     :root {
#         --primary-blue: #2E5C8A;
#         --secondary-gray: #6B7280;
#         --light-blue: #E0F2FE;
#         --white: #ffffff;
#         --light-gray: #F3F4F6;
#         --border-color: #E5E7EB;
#     }
    
#     /* Reset do Streamlit */
#     .main .block-container {
#         padding-top: 1rem;
#         padding-bottom: 1rem;
#         max-width: 1200px;
#     }
    
#     /* Fonte principal */
#     html, body, [class*="css"] {
#         font-family: 'Inter', sans-serif;
#     }
    
#     /* Header principal linear-gradient(135deg, #E0F2FE 0%, #ffffff 100%)*/
#     .hero-section {
#         background: white;
#         padding: 2rem;
#         border-radius: 12px;
#         border: solid 1px #f1f1f1;
#         text-align: center;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#     }
    
#     .logo-container {
#         display: flex;
#         justify-content: left;
#         align-items: center;
#         margin-bottom: 1rem;
#     }
    
#     /* Cards de introdução */
#     .intro-card {
#         background: linear-gradient(135deg, #E0F2FE 0%, #ffffff 100%);
#         border-radius: 12px;
#         padding: 2rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#         border: 1px solid #E5E7EB;
#         margin-bottom: 2rem;
#     }
    
#     .intro-card h2 {
#         color: #2E5C8A;
#         font-size: 2rem;
#         font-weight: 600;
#         margin-bottom: 1.5rem;
#         text-align: center;
#         font-size: 33px;
#     }
    
#     .intro-content p {
#         font-size: 1.17rem;
#         line-height: 1.7;
#         margin-bottom: 1.5rem;
#         color: #4e4c4c;
#         text-align: justify;
#     }
    
#     /* Cards de navegação */
#     .nav-card {
#         background: white;
#         border-radius: 12px;
#         padding: 2rem;
#         text-align: center;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#         border: 1px solid #E5E7EB;
#         transition: all 0.3s ease;
#         margin-bottom: 1.5rem;
#         height: 100%;
#     }
    
#     .nav-card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
#     }
    
#     .card-icon {
#         width: 60px;
#         height: 60px;
#         margin: 0 auto 1.5rem;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         background: #E0F2FE;
#         border-radius: 50%;
#     }
    
#     .nav-card h3 {
#         color: #2E5C8A;
#         font-size: 1.3rem;
#         font-weight: 600;
#         margin-bottom: 1rem;
#     }
    
#     .nav-card p {
#         color: #6B7280;
#         font-size: 1rem;
#         line-height: 1.6;
#         margin-bottom: 1.5rem;
#     }
    
#     /* Botões customizados */
#     .stButton > button {
#         background: #2E5C8A;
#         color: white;
#         border: none;
#         border-radius: 6px;
#         padding: 0.75rem 1.5rem;
#         font-weight: 500;
#         transition: all 0.2s ease;
#         width: 100%;
#     }
    
#     .stButton > button:hover {
#         background: #1e3a5f;
#         transform: translateY(-1px);
#     }
    
#     /* Sidebar customizada */
#     .css-1d391kg {
#         background: white;
#         border-right: 1px solid #E5E7EB;
#     }
    
#     .css-1d391kg .css-1v0mbdj {
#         color: #2E5C8A;
#         font-weight: 600;
#     }
    
#     /* Métricas customizadas */
#     .metric-card {
#         background: white;
#         border-radius: 12px;
#         padding: 1.5rem;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#         border: 1px solid #E5E7EB;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
    
#     .metric-value {
#         font-size: 2.5rem;
#         font-weight: 700;
#         color: #2E5C8A;
#         margin-bottom: 0.5rem;
#     }
    
#     .metric-label {
#         font-size: 1rem;
#         color: #6B7280;
#         font-weight: 500;
#     }
    
#     /* Footer */
#     .footer {
#         background: #2E5C8A;
#         color: white;
#         text-align: center;
#         padding: 2rem;
#         border-radius: 12px;
#         margin-top: 3rem;
#     }
    
#     .footer p {
#         font-size: 0.9rem;
#         opacity: 0.9;
#         margin: 0;
#     }
    
#     /* Animações */
#     @keyframes fadeIn {
#         from {
#             opacity: 0;
#             transform: translateY(20px);
#         }
#         to {
#             opacity: 1;
#             transform: translateY(0);
#         }
#     }
    
#     .nav-card {
#         animation: fadeIn 0.6s ease-out;
#     }
    
#     .st-emotion-cache-zy6yx3 {
#         max-width: 1080px;
#         padding: 4rem 1rem 10rem;
#     }
    
#     .stMain{
#         background: #f9f9f9;
#     }
        
#     /* Responsividade */
#     @media (max-width: 768px) {
#         .intro-card h2 {
#             font-size: 1.5rem;
#         }
        
#         .intro-content p {
#             font-size: 1rem;
#         }
        
#         .nav-card h3 {
#             font-size: 1.1rem;
#         }
#     }
# </style>
# """, unsafe_allow_html=True)

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

# # Sidebar com menu de navegação
# with st.sidebar:
#     st.markdown("### 📋 Menu de Navegação")
    
#     page = st.selectbox(
#         "Escolha uma seção:",
#         [
#             "🏠 Início",
#             "📊 Análises Descritivas", 
#             "📝 Questionário do Estudante",
#             "📚 Organização Didático-pedagógica",
#             "🏢 Infraestrutura e Instalações",
#             "🎓 Oportunidades de Formação"
#         ]
#     )
    
#     st.markdown("---")
#     st.markdown("### ⚙️ Configurações")
#     show_details = st.checkbox("Mostrar detalhes", value=True)
#     chart_type = st.selectbox("Tipo de gráfico:", ["Barras", "Linha", "Pizza"])

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
    
    # # Cards de navegação
    # st.markdown("## 🔍 Explore as Análises")
    
    # col1, col2, col3 = st.columns(3)
    
    # with col1:
    #     st.markdown(create_nav_card(
    #         "Análises Descritivas",
    #         "Explore os dados e estatísticas detalhadas dos resultados do Enade 2023.",
    #         "icon_analises.png",
    #         "📊"
    #     ), unsafe_allow_html=True)
    #     if st.button("Acessar Análises", key="btn_analises"):
            
    #         st.success("Redirecionando para Análises Descritivas...")
    #         Conhecimento_Específico.show_page()
    
    # with col2:
    #     st.markdown(create_nav_card(
    #         "Questionário do Estudante",
    #         "Análise das respostas dos estudantes sobre sua experiência acadêmica.",
    #         "icon_questionario.png",
    #         "📝"
    #     ), unsafe_allow_html=True)
    #     if st.button("Acessar Questionário", key="btn_questionario"):
    #         st.success("Redirecionando para Questionário do Estudante...")
    
    # with col3:
    #     st.markdown(create_nav_card(
    #         "Infraestrutura e Instalações",
    #         "Avaliação da infraestrutura física e recursos disponíveis.",
    #         "icon_infraestrutura.png",
    #         "🏢"
    #     ), unsafe_allow_html=True)
    #     if st.button("Acessar Infraestrutura", key="btn_infra"):
    #         st.success("Redirecionando para Infraestrutura...")

elif "Conhecimento Específico" in page:
    Conhecimento_Específico.show_page()
    st.stop()
elif "Questionário do Estudante" in page:
    Questionário_do_Estudante.show_page()
    st.stop()

# elif page == "📊 Conhecimento Específico":
#     st.markdown("# 📊 Análises Descritivas")
    
#     # Métricas principais
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">1,234</div>
#             <div class="metric-label">Estudantes Participantes</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">85</div>
#             <div class="metric-label">Cursos Avaliados</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">4.2</div>
#             <div class="metric-label">Nota Média</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">78%</div>
#             <div class="metric-label">Taxa de Participação</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Gráficos de exemplo
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("📈 Desempenho por Área")
#         areas = ['Ciências Exatas', 'Humanas', 'Biológicas', 'Tecnológicas']
#         notas = [4.5, 4.1, 4.3, 4.7]
        
#         if chart_type == "Barras":
#             fig = px.bar(x=areas, y=notas, title="Notas Médias por Área")
#         elif chart_type == "Linha":
#             fig = px.line(x=areas, y=notas, title="Notas Médias por Área")
#         else:
#             fig = px.pie(values=notas, names=areas, title="Distribuição por Área")
        
#         fig.update_layout(
#             plot_bgcolor='rgba(0,0,0,0)',
#             paper_bgcolor='rgba(0,0,0,0)',
#             font_color='#2E5C8A'
#         )
#         st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         st.subheader("📊 Distribuição de Notas")
#         notas_dist = [1, 2, 3, 4, 5]
#         freq = [5, 15, 35, 30, 15]
        
#         fig2 = px.histogram(x=notas_dist, y=freq, title="Frequência de Notas")
#         fig2.update_layout(
#             plot_bgcolor='rgba(0,0,0,0)',
#             paper_bgcolor='rgba(0,0,0,0)',
#             font_color='#2E5C8A'
#         )
#         st.plotly_chart(fig2, use_container_width=True)
    
#     if show_details:
#         st.subheader("📋 Dados Detalhados")
#         data = {
#             'Curso': ['Engenharia', 'Medicina', 'Direito', 'Administração', 'Psicologia'],
#             'Participantes': [150, 120, 200, 180, 95],
#             'Nota Média': [4.5, 4.8, 4.1, 4.3, 4.6],
#             'Taxa Participação': ['85%', '92%', '78%', '80%', '88%']
#         }
#         df = pd.DataFrame(data)
#         st.dataframe(df, use_container_width=True)

# elif page == "📝 Questionário do Estudante":
#     st.markdown("# 📝 Questionário do Estudante")
    
#     st.info("📋 Análise das respostas dos estudantes sobre sua experiência acadêmica e percepções sobre o curso.")
    
#     # Filtros
#     col1, col2 = st.columns(2)
#     with col1:
#         curso_filter = st.selectbox("Filtrar por curso:", ["Todos", "Engenharia", "Medicina", "Direito"])
#     with col2:
#         periodo_filter = st.selectbox("Período:", ["2023.1", "2023.2", "Ambos"])
    
#     # Gráfico de satisfação
#     st.subheader("😊 Índice de Satisfação")
#     categorias = ['Ensino', 'Infraestrutura', 'Coordenação', 'Biblioteca', 'Laboratórios']
#     satisfacao = [4.2, 3.8, 4.5, 4.1, 3.9]
    
#     fig = px.bar(x=categorias, y=satisfacao, 
#                  title="Satisfação por Categoria (Escala 1-5)",
#                  color=satisfacao,
#                  color_continuous_scale="Blues")
#     fig.update_layout(
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         font_color='#2E5C8A'
#     )
#     st.plotly_chart(fig, use_container_width=True)

# elif page == "📚 Organização Didático-pedagógica":
#     st.markdown("# 📚 Organização Didático-pedagógica")
    
#     st.info("📖 Avaliação da organização curricular, metodologias de ensino e práticas pedagógicas.")
    
#     # Métricas pedagógicas
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.metric("Qualidade do Ensino", "4.3/5", "0.2")
#     with col2:
#         st.metric("Metodologias Ativas", "78%", "5%")
#     with col3:
#         st.metric("Satisfação Docente", "4.1/5", "-0.1")
    
#     # Gráfico de metodologias
#     st.subheader("🎯 Metodologias de Ensino Utilizadas")
#     metodologias = ['Aulas Expositivas', 'Estudos de Caso', 'Projetos', 'Seminários', 'Laboratórios']
#     uso = [85, 65, 45, 70, 55]
    
#     fig = px.horizontal_bar(y=metodologias, x=uso, 
#                            title="Percentual de Uso das Metodologias")
#     fig.update_layout(
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         font_color='#2E5C8A'
#     )
#     st.plotly_chart(fig, use_container_width=True)

# elif page == "🏢 Infraestrutura e Instalações":
#     st.markdown("# 🏢 Infraestrutura e Instalações")
    
#     st.info("🏗️ Avaliação da infraestrutura física, equipamentos e recursos disponíveis.")
    
#     # Avaliação por categoria
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("📊 Avaliação da Infraestrutura")
#         infra_items = ['Salas de Aula', 'Laboratórios', 'Biblioteca', 'Área de Convivência', 'Equipamentos']
#         notas_infra = [4.0, 3.8, 4.5, 3.5, 3.9]
        
#         fig = px.radar(r=notas_infra, theta=infra_items, 
#                        title="Avaliação por Categoria",
#                        range_r=[0, 5])
#         fig.update_layout(
#             plot_bgcolor='rgba(0,0,0,0)',
#             paper_bgcolor='rgba(0,0,0,0)',
#             font_color='#2E5C8A'
#         )
#         st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         st.subheader("🔧 Status dos Equipamentos")
#         status = ['Excelente', 'Bom', 'Regular', 'Ruim']
#         percentuais = [25, 45, 25, 5]
        
#         fig2 = px.pie(values=percentuais, names=status, 
#                       title="Condição dos Equipamentos")
#         fig2.update_layout(
#             plot_bgcolor='rgba(0,0,0,0)',
#             paper_bgcolor='rgba(0,0,0,0)',
#             font_color='#2E5C8A'
#         )
#         st.plotly_chart(fig2, use_container_width=True)

# elif page == "🎓 Oportunidades de Formação":
#     st.markdown("# 🎓 Oportunidades de Formação")
    
#     st.info("🌟 Análise das oportunidades de formação complementar e desenvolvimento profissional.")
    
#     # Oportunidades disponíveis
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.metric("Projetos de Extensão", "45", "8")
#     with col2:
#         st.metric("Iniciação Científica", "120", "15")
#     with col3:
#         st.metric("Estágios Disponíveis", "89", "12")
    
#     # Participação em atividades
#     st.subheader("📈 Participação em Atividades Complementares")
#     atividades = ['Monitoria', 'Extensão', 'Pesquisa', 'Estágio', 'Eventos']
#     participacao = [30, 25, 20, 45, 60]
    
#     fig = px.bar(x=atividades, y=participacao, 
#                  title="Percentual de Participação por Atividade",
#                  color=participacao,
#                  color_continuous_scale="Viridis")
#     fig.update_layout(
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         font_color='#2E5C8A'
#     )
#     st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 CPA - DIAVI/PROPLAN. Todos os direitos reservados.</p>
</div>
""", unsafe_allow_html=True)
