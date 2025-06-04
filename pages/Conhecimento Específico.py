import streamlit as st
from app import *

st.markdown("""
<style>
#conhecimento-especifico-enade-2025 
{font-size: 30px;
padding:1rem 0;}     

.stMainBlockContainer
{padding:3rem 0;
max-width: none;
}  

.st-emotion-cache-ocqkz7{
    padding: 0 1rem;
}              
</style>""", unsafe_allow_html=True)

st.title('Conhecimento Específico ENADE 2025')

col1, col2 = st.columns([0.5, 0.5])

municipios = UFPA_data['NOME_MUNIC_CURSO'].unique().tolist()

cursos=[]
def atualiza_cursos():
    cursos = UFPA_data.query("NOME_MUNIC_CURSO == @municipio_op")['NOME_CURSO'].unique().tolist()
    cursos.sort()
    return cursos

with st.container():   
    with col1:
        municipio_op = st.selectbox(
            "Selcione o Município", 
            municipios,
            key='municipio'
        )

    with col2:
        curso_op = st.selectbox(
            "Selcione o Curso", 
            atualiza_cursos()
        )
    
col1, col2, col3 = st.columns(3)
tab1, tab2, tab3 = st.tabs(["Organização Didático Pedagógica", "Infraestrutura e Instalações Físicas", "Oportunidades de Ampliação da Formação"])

for code, item in COURSE_CODES.items():
    if item[1] == curso_op and item[3] == municipio_op:
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_average_graph(
                    code,
                    ['QE_I27', 'QE_I28', 'QE_I29', 'QE_I30', 'QE_I31', 'QE_I32', 'QE_I33', 'QE_I34', 'QE_I35', 'QE_I36', 'QE_I37', 'QE_I38', 'QE_I39', 'QE_I40', 'QE_I42', 'QE_I47', 'QE_I48', 'QE_I49', 'QE_I51', 'QE_I55', 'QE_I57', 'QE_I66']), use_container_width=True)
            with col2:
                st.plotly_chart(plot_count_graph(
                    code,
                    ['QE_I27', 'QE_I28', 'QE_I29', 'QE_I30', 'QE_I31', 'QE_I32', 'QE_I33', 'QE_I34', 'QE_I35', 'QE_I36', 'QE_I37', 'QE_I38', 'QE_I39', 'QE_I40', 'QE_I42', 'QE_I47', 'QE_I48', 'QE_I49', 'QE_I51', 'QE_I55', 'QE_I57', 'QE_I66']), use_container_width=True)
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_average_graph(code, 
                ['QE_I50', 'QE_I54', 'QE_I56', 'QE_I58', 'QE_I59', 'QE_I60', 'QE_I61','QE_I62', 'QE_I63', 'QE_I64', 'QE_I65', 'QE_I67', 'QE_I68']), use_container_width=True)
            with col2:
                st.plotly_chart(plot_count_graph(code, 
                ['QE_I50', 'QE_I54', 'QE_I56', 'QE_I58', 'QE_I59', 'QE_I60', 'QE_I61','QE_I62', 'QE_I63', 'QE_I64', 'QE_I65', 'QE_I67', 'QE_I68']), use_container_width=True)
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(plot_average_graph(code, 
                                            ['QE_I43', 'QE_I44', 'QE_I45', 'QE_I46', 'QE_I52', 'QE_I53']), use_container_width=True)
            with col2:
                st.plotly_chart(plot_count_graph(code, 
                                            ['QE_I43', 'QE_I44', 'QE_I45', 'QE_I46', 'QE_I52', 'QE_I53']), use_container_width=True)
        break  # se quiser só um gráfico