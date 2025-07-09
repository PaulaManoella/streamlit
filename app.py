import streamlit as st
from main import UFPA_data

st.set_page_config(
    page_title='Análise Microdados ENADE 2023'
)

st.markdown("""
<style>
.text p{
    font-size: 18px
}
</style>""", unsafe_allow_html=True)

st.image('enade.PNG')

st.markdown("""
<div class="text">
    <p>A CPA, em parceria com a DIAVI/PROPLAN, apresenta as análises descritivas dos microdados do Enade 2023, com o objetivo de auxiliar as coordenações de curso na identificação de melhorias a serem implementadas na graduação.</p>
    <p>As análises compreendem os temas do Componente Específico da prova do Enade e as questões do Questionário do Estudante, relativas às dimensões “Organização Didático-pedagógica”, “Infraestrutura e Instalações Físicas” e “Oportunidade Ampliação da Formação Profissional”.</p>
    <p>Para visualizar as análises, basta navegar entre as páginas disponíveis no menu lateral.</p>
</div>
""", unsafe_allow_html=True)
    
municipios = UFPA_data['NOME_MUNIC_CURSO'].unique().tolist()
municipios.sort()
    
def atualiza_cursos(opcao):
    cursos = UFPA_data.query("NOME_MUNIC_CURSO == @opcao")['NOME_CURSO'].unique().tolist()
    cursos.sort()  
    print(cursos)
    return cursos

def renderiza_filtros(UFPA_data):
    municipios = UFPA_data['NOME_MUNIC_CURSO'].unique().tolist()
    municipios.sort()

    col1, col2 = st.columns(2)

    #  NÃO sobrescreve se já existe
    if "municipio_op" not in st.session_state:
        st.session_state["municipio_op"] = municipios[0]

    with col1:
        # selectbox ligado ao session_state via key (não atribui diretamente)
        st.selectbox(
            "Selecione o Município",
            municipios,
            index=municipios.index(st.session_state["municipio_op"]),
            key="municipio_op"
        )

    # Cursos baseados no município já salvo no session_state
    cursos = UFPA_data.query(
        "NOME_MUNIC_CURSO == @st.session_state.municipio_op"
    )['NOME_CURSO'].unique().tolist()
    cursos.sort()

    #  NÃO sobrescreve se o curso já estiver válido
    if (
        "curso_op" not in st.session_state
        or st.session_state["curso_op"] not in cursos
    ):
        st.session_state["curso_op"] = cursos[0] if cursos else None

    with col2:
        st.selectbox(
            "Selecione o Curso",
            cursos,
            index=cursos.index(st.session_state["curso_op"]) if st.session_state["curso_op"] in cursos else 0,
            key="curso_op"
        )
