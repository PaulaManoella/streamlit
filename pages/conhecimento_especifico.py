import streamlit as st
from main import COURSE_CODES, plot_performance_graph, show_best_hei_ranking_table, UFPA_data
from app import atualiza_cursos

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

div[data-testid="stImageContainer"] img {
    max-width: 75%;
}            
</style>

""", unsafe_allow_html=True)

municipios = UFPA_data['NOME_MUNIC_CURSO'].unique().tolist()
municipios.sort()

#se nao ha nenhumaopção selecionada, pega o primeiro valor de municipios/atualiza_cursos
if 'municipio_op' not in st.session_state:
    st.session_state['municipio_op'] = municipios[0]

if 'curso_op' not in st.session_state:
    st.session_state['curso_op'] = atualiza_cursos(st.session_state['municipio_op'])[0]

st.selectbox(
    "Selecione o Município",
    municipios,
    index=municipios.index(st.session_state['municipio_op']),
    key='municipio'
)

#atualiza a opção quando mudada
st.session_state['municipio_op'] = st.session_state['municipio']

cursos = atualiza_cursos(st.session_state['municipio'])

if st.session_state['curso_op'] not in cursos:
    st.session_state['curso_op'] = cursos[0]

st.selectbox(
    'Selecione o Curso',
    cursos,
    index=cursos.index(st.session_state['curso_op']),
    key='curso'
)
st.session_state['curso_op'] = st.session_state['curso']          
        
tab1, tab2, tab3= st.tabs(["Gráfico Razão do Percentual", "Gráfico Percentual", "Tabela Ranking"])

for code,item in COURSE_CODES.items():
    if item[1] == st.session_state['curso_op'] and item[3] == st.session_state['municipio_op']:
        fig1, fig2 = plot_performance_graph(item[0], code, ratio_graph=True)
        with tab1:
            if fig1:
                st.subheader("Gráfico 1")
                st.pyplot(fig1)
        with tab2:
            if fig2:
                st.subheader("Gráfico 2")
                st.pyplot(fig2)
        with tab3:
            fig = show_best_hei_ranking_table(item[0], code, public_only=True)
            st.dataframe(fig, use_container_width=True)
