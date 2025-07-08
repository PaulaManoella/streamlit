import streamlit as st
from app import atualiza_cursos, municipios
from main import COURSE_CODES, plot_average_graph, plot_count_graph
from streamlit_pdf_viewer import pdf_viewer

st.markdown("""
<style>
#questionario-do-estudante-enade-2023
{font-size: 2.5rem;}     

.stMainBlockContainer
{padding:3rem 0;
max-width: none;
}  

.stHorizontalBlock{
    padding: 0 10rem;
} 

.stVerticalBlock {
    padding: 0 0.5rem;
}

.st-c2 {
    background-color: rgb(0 116 219);
}

.st-bd {
    color: rgb(0 116 219);
}

.st-aq {
    padding-left: 1rem;
}

.st-bz:focus {
    color: rgb(0 116 219);
}

.st-bn:hover {
    color: rgb(0 116 219);
}

.meu-container{
    margin: 0 10rem;
}
          
</style>""", unsafe_allow_html=True)

st.markdown("""
<div class="meu-container">
    <h1>Questionário do Estudante ENADE 2023</h1>
    <p>Para cada questão no Questionário do Estudante, são disponibilizadas 6 alternativas de resposta que indicam o grau de concordância com cada assertiva, em uma escala que varia de 1 (discordância total) a 6 (concordância total), além das alternativas 7 (Não sei responder) e 8 (Não se aplica).</p>
    <p>Para cada dimensão do questionário, foram gerados dois gráficos. O gráfico de barras apresenta a média atribuída pelos alunos para cada questão, excluídas as alternativas 7 e 8. São destacadas as questões com a maior e a menor média.</p>
    <p>O gráfico de linhas representa, por questão, o total de respostas absolutas (contagem) agrupadas pelo tipo de alternativa escolhida, da seguinte forma: 1-2; 3-4; 5-6; 7-8.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.5, 0.5])

municipio_op = st.session_state.get('municipio_op', municipios[0])

with col1:
    st.selectbox(
        "Selecione o Município",
        municipios,
        index=municipios.index(municipio_op),
        key='municipio'
    )

# Atualiza a variável persistente se o usuário trocar a seleção
st.session_state['municipio_op'] = st.session_state['municipio']


# Agora atualiza os cursos com base no município selecionado
cursos = atualiza_cursos(st.session_state['municipio'])
curso_op = st.session_state.get('curso_op', cursos[0])

# Verifica se o curso salvo ainda existe para aquele município
if curso_op not in cursos:
    curso_op = cursos[0]

with col2:
    st.selectbox(
        "Selecione o Curso",
        cursos,
        index=cursos.index(curso_op),
        key='curso'
    )

st.session_state['curso_op'] = st.session_state['curso']


col1, col2, col3 = st.columns(3)
tab1, tab2, tab3, tab4 = st.tabs(["Organização Didático Pedagógica", "Infraestrutura e Instalações Físicas", "Oportunidades de Ampliação da Formação", "Anexo Questionário do Estudante"])

odp_questions_text = ['As disciplinas cursadas contribuíram para sua formação integral, <br>como cidadão e profissional.',
                    'Os conteúdos abordados nas disciplinas do curso favoreceram sua atuação<br>em estágios ou em atividades de iniciação profissional.',
                    'As metodologias de ensino utilizadas no curso desafiaram você a aprofundar<br>conhecimentos e desenvolver competências reflexivas e críticas.',
                    'O curso propiciou experiências de aprendizagem inovadoras.',
                    'O curso contribuiu para o desenvolvimento da sua consciência ética<br>para o exercício profissional.',
                    'No curso você teve oportunidade de aprender a trabalhar em equipe.',
                    'O curso possibilitou aumentar sua capacidade de reflexão e argumentação.',
                    'O curso promoveu o desenvolvimento da sua capacidade de pensar criticamente,<br>analisar e refletir sobre soluções para problemas da sociedade.',
                    'O curso contribuiu para você ampliar sua capacidade de comunicação<br>nas formas oral e escrita.',
                    'O curso contribuiu para o desenvolvimento da sua capacidade de aprender<br>e atualizar-se permanentemente.',
                    'As relações professor-aluno ao longo do curso estimularam você a estudar e aprender.',
                    'Os planos de ensino apresentados pelos professores contribuíram para<br>o desenvolvimento das atividades acadêmicas e para seus estudos.',
                    'As referências bibliográficas indicadas pelos professores nos planos<br>de ensino contribuíram para seus estudos e aprendizagens.',
                    'Foram oferecidas oportunidades para os estudantes superarem dificuldades<br>relacionadas ao processo de formação.',
                    'O curso exigiu de você organização e dedicação frequente aos estudos.',
                    'O curso favoreceu a articulação do conhecimento teórico com atividades práticas.',
                    'As atividades práticas foram suficientes para relacionar os conteúdos<br>do curso com a prática, contribuindo para sua formação profissional.',
                    'O curso propiciou acesso a conhecimentos atualizados e/ou contemporâneos<br>em sua área de formação',
                    'As atividades realizadas durante seu trabalho de conclusão de curso contribuíram<br>para qualificar sua formação profissional.',
                    'As avaliações da aprendizagem realizadas durante o curso foram compatíveis<br>com os conteúdos ou temas trabalhados pelos professores.',
                    'Os professores demonstraram domínio dos conteúdos abordados nas disciplinas.',
                    'As atividades acadêmicas desenvolvidas dentro e fora da sala de aula<br>possibilitaram reflexão, convivência e respeito à diversidade.']

infra_questions_text = ['O estágio supervisionado proporcionou experiências <br>diversificadas para a sua formação.',
                        'Os estudantes participaram de avaliações periódicas do curso (disciplinas, <br>atuação dos professores, infraestrutura).',
                        'Os professores apresentaram disponibilidade para atender <br>os estudantes fora do horário das aulas.',
                        'Os professores utilizaram tecnologias da informação e comunicação <br>(TICs) como estratégia de ensino (projetor multimídia, laboratório de informática, <br>ambiente virtual de aprendizagem).',
                        'A instituição dispôs de quantidade suficiente de funcionários<br> para o apoio administrativo e acadêmico.',
                        'O curso disponibilizou monitores ou tutores para auxiliar os estudantes.',
                        'As condições de infraestrutura das salas de aula foram adequadas.',
                        'Os equipamentos e materiais disponíveis para as aulas práticas<br> foram adequados para a quantidade de estudantes.',
                        'Os ambientes e equipamentos destinados às aulas práticas foram adequados ao curso.',
                        'A biblioteca dispôs das referências bibliográficas que os estudantes necessitaram.',
                        'A instituição contou com biblioteca virtual ou conferiu<br> acesso a obras disponíveis em acervos virtuais.',
                        'A instituição promoveu atividades de cultura, de lazer e de interação social.',
                        'A instituição dispôs de refeitório, cantina e banheiros em<br> condições adequadas que atenderam as necessidades dos seus usuários.']

oaf_questions_text = ['Foram oferecidas oportunidades para os estudantes participarem de<br> programas, projetos ou atividades de extensão universitária.',
                    'Foram oferecidas oportunidades para os estudantes participarem de<br> projetos de iniciação científica e de atividades que estimularam a investigação acadêmica.',
                    'O curso ofereceu condições para os estudantes participarem de<br> eventos internos e/ou externos à instituição.',
                    'A instituição ofereceu oportunidades para os estudantes<br> atuarem como representantes em órgãos colegiados.',
                    'Foram oferecidas oportunidades para os estudantes<br> realizarem intercâmbios e/ou estágios no país.',
                    'Foram oferecidas oportunidades para os estudantes<br> realizarem intercâmbios e/ou estágios fora do país.']

for code, item in COURSE_CODES.items():
    if item[1] == st.session_state['curso_op'] and item[3] == st.session_state['municipio_op']:
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_average_graph(
                    code,
                    ['QE_I27', 'QE_I28', 'QE_I29', 'QE_I30', 'QE_I31', 'QE_I32', 'QE_I33', 'QE_I34', 'QE_I35', 'QE_I36', 'QE_I37', 'QE_I38', 'QE_I39', 'QE_I40', 'QE_I42', 'QE_I47', 'QE_I48', 'QE_I49', 'QE_I51', 'QE_I55', 'QE_I57', 'QE_I66'],odp_questions_text), use_container_width=True)
            with col2:
                st.plotly_chart(plot_count_graph(
                    code,
                    ['QE_I27', 'QE_I28', 'QE_I29', 'QE_I30', 'QE_I31', 'QE_I32', 'QE_I33', 'QE_I34', 'QE_I35', 'QE_I36', 'QE_I37', 'QE_I38', 'QE_I39', 'QE_I40', 'QE_I42', 'QE_I47', 'QE_I48', 'QE_I49', 'QE_I51', 'QE_I55', 'QE_I57', 'QE_I66']), use_container_width=True)
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_average_graph(code, 
                ['QE_I50', 'QE_I54', 'QE_I56', 'QE_I58', 'QE_I59', 'QE_I60', 'QE_I61','QE_I62', 'QE_I63', 'QE_I64', 'QE_I65', 'QE_I67', 'QE_I68'],infra_questions_text), use_container_width=True)
            with col2:
                st.plotly_chart(plot_count_graph(code, 
                ['QE_I50', 'QE_I54', 'QE_I56', 'QE_I58', 'QE_I59', 'QE_I60', 'QE_I61','QE_I62', 'QE_I63', 'QE_I64', 'QE_I65', 'QE_I67', 'QE_I68']), use_container_width=True)
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(plot_average_graph(code, 
                                            ['QE_I43', 'QE_I44', 'QE_I45', 'QE_I46', 'QE_I52', 'QE_I53'],
                                            oaf_questions_text), use_container_width=True)
            with col2:
                st.plotly_chart(plot_count_graph(code, 
                                            ['QE_I43', 'QE_I44', 'QE_I45', 'QE_I46', 'QE_I52', 'QE_I53']), use_container_width=True)
        break  

with tab4:
    pdf_viewer(
    "anexo_qe_2023.pdf",
    width=900,
    height=600,
    zoom_level=1.5,                    # 120% zoom
    viewer_align="center",             # Center alignment
    show_page_separator=True           # Show separators between pages
)
