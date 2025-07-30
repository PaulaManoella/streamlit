import streamlit as st
from main import COURSE_CODES, plot_performance_graph, show_best_hei_ranking_table, UFPA_data
from utils import atualiza_cursos


with open('style/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def show_page():

    with st.container():

        st.markdown("""
        <div class="text-container">
            <h1>Conhecimento Específico ENADE 2023</h1>
            <p>A análise gráfica fornece informações valiosas a respeito do desempenho dos alunos nas temáticas avaliadas na prova, uma vez que possibilita averiguar se as estratégias pedagógicas aplicadas nas disciplinas ministradas estão produzindo os resultados almejados. São apresentados dois gráficos que exibem a comparação entre o desempenho do curso de graduação da UFPA e o desempenho nacional, calculado a partir do mesmo curso ofertado por todas as IES no país que participam do exame.</p>
            <p>O Gráfico da Razão do Percentual de Acerto exibe o desempenho do curso da UFPA em comparação com a média nacional, por tema avaliado no ENADE 2023. A interpretação do gráfico da razão é a seguinte: Razão > 1,0: a UFPA apresentou desempenho superior à média nacional; Razão < 1,0: a UFPA obteve desempenho inferior à média nacional; Razão = 1,0: o desempenho da UFPA foi equivalente à média nacional.</p>
            <p>O Gráfico de Percentual de Acerto por Tema apresenta a comparação entre o percentual de acertos do curso da UFPA e o percentual médio nacional, para cada temática do componente específico da prova.</p>
            <p>Na Tabela Ranking é apresentada a instituição com melhor percentual de desempenho, por temática do exame, em comparação com o desempenho do curso da UFPA.</p>
        </div>
        """, unsafe_allow_html=True)

        municipios = UFPA_data['NOME_MUNIC_CURSO'].unique().tolist()
        municipios.sort()

        col1, col2 = st.columns(2)
        #se nao ha nenhumaopção selecionada, pega o primeiro valor de municipios/atualiza_cursos
        if 'municipio_op' not in st.session_state:
            st.session_state['municipio_op'] = municipios[0]

        if 'curso_op' not in st.session_state:
            st.session_state['curso_op'] = atualiza_cursos(st.session_state['municipio_op'])[0]

        with col1:
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

        with col2:
            st.selectbox(
                'Selecione o Curso',
                cursos,
                index=cursos.index(st.session_state['curso_op']),
                key='curso'
            )
        st.session_state['curso_op'] = st.session_state['curso']         
                
        tab1, tab2, tab3= st.tabs(["Gráfico Razão do Percentual", "Gráfico Percentual", "Tabela Ranking"])
        
        for code, item in COURSE_CODES.items():
            if item[1] == st.session_state['curso_op'] and item[3] == st.session_state['municipio_op']:
                result = plot_performance_graph(item[0], code, ratio_graph=True)

                if result is None:
                    st.warning("Não foi possível gerar os gráficos para esse curso.")
                    break  # ou continue, se quiser testar os próximos

                fig1, fig1_img, fig2, fig2_img = result

                with tab1:
                    if fig1:
                        st.pyplot(fig1)
                with tab2:
                    if fig2:
                        st.pyplot(fig2)
                with tab3:
                    fig = show_best_hei_ranking_table(item[0], code, public_only=True)
                    st.dataframe(fig, use_container_width=True)

                st.session_state['razao_chart'] = fig1_img
                st.session_state['percent_chart'] = fig2_img
                break
            

