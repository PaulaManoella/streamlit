import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from textwrap import fill

import plotly.express as px
import tempfile
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import streamlit as st
import plotly.io as pio


ENADE_2023_CE_URL = "https://github.com/PaulaManoella/Microdados-Enade/raw/main/databases2023/microdados2023_arq3.zip"
ENADE_2023_QE_URL = "https://github.com/PaulaManoella/Microdados-Enade/raw/main/databases2023/microdados2023_arq4.zip"

#remover - arquivo nao esta sendo utilizado
ENADE_2023_arq1 = "https://github.com/PaulaManoella/Microdados-Enade/raw/main/databases2023/microdados2023_arq1.zip"

QE_2022_URL = 'https://github.com/PaulaManoella/Microdados-Enade/raw/main/micro_QE_2022.zip'

UFPA_CODE = 569
PRESENT_STUDENT_CODE = 555
NUM_SK_QUESTIONS = 27 #Número de questões da componente de conhecimento específico

PUBLIC_ADMIN_CATEGORY = 1 # Categoria administrativa: pública federal
FEDERAL_ORG_CATEGORY = 10028 # Categoria organizacional: universidade

# ''' O dicionário está estruturado da seguinte forma:

# COURSE_CODES = CO_GRUPO: ["Área de Avaliação", "Grau Acadêmico", "Nome Arquivo CSV", {CO_CURSO: ["Município do Curso"]}]

# '''

#URL do arquivo CSV no GitHub
QUESTIONS_SUBJECTS_URL = "https://raw.githubusercontent.com/PaulaManoella/Microdados-Enade/main/databases2023/"
# "https://github.com/PaulaManoella/Microdados-Enade/tree/main/databases2023/"

question_sub_eude = "https://raw.githubusercontent.com/PaulaManoella/Microdados-Enade/main/databases2022/"
#modificar linha abaixo
HEI_CODES_URL = question_sub_eude + "hei.csv"

#Definindo o tipo dos dados como: String
DTYPES = {"DS_VT_ACE_OFG" : str,
          "DS_VT_ACE_OCE" : str,
          "DS_VT_ESC_OCE" : str,
          "DS_VT_ESC_OFG" : str}

##################### mudar nome da variavel

base = "https://raw.githubusercontent.com/PaulaManoella/Microdados-Enade/refs/heads/main/databases2023/base_db.csv"
database = pd.read_csv(base, sep=";")

cpc_base_url = "https://raw.githubusercontent.com/PaulaManoella/Microdados-Enade/refs/heads/main/databases2023/CPC_2023.csv"
cpc2023 = pd.read_csv(cpc_base_url, sep=";")


def get_raw_data(url: str, extract_to: str = '.') -> None:

    # Faz o download do arquivo ZIP
    http_response = urlopen(url)

    # Extrai o conteúdo do arquivo ZIP
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

    # Fazle.extractall(path=extract_to)

def filter_courses_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra somente os participantes presentes na prova, que tiveram resultado
    válido e que preencheram o cartão-resposta do exame.

    Parameters
    ----------
    df : pandas.DataFrame
        O DataFrame contendo os dados dos participantes.

    Returns
    -------
    pandas.DataFrame
        O DataFrame filtrado com os participantes que atendem aos critérios.

    Examples
    --------
    >>> filtered_df = filter_courses_results(df)
    """
    for curso in cod_curso:
      df = df.loc[df["CO_GRUPO"].isin(cod_grupo_list)]

    df = df.loc[(df["TP_PRES"] == PRESENT_STUDENT_CODE) &
                (df["TP_PR_GER"] == PRESENT_STUDENT_CODE) &
                (~df["DS_VT_ESC_OCE"].isna())]

    return df

def reduce_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona os atributos relevantes para a realização da análise dos dados.

    Parameters
    ----------
    df : pandas.DataFrame
        O DataFrame contendo os dados completos.

    Returns
    -------
    pandas.DataFrame
        O DataFrame reduzido contendo somente os atributos relevantes.

    Examples
    --------
    Exemplo de uso:

    >>> reduced_df = reduce_data(df)
    """

    columns = ["NU_ANO",
               "CO_IES",
               "CO_GRUPO",
               "CO_CURSO",
               "NOME_CURSO",
               "NOME_MUNIC_CURSO",
               "CO_CATEGAD",
               "CO_ORGACAD",
               "DS_VT_ACE_OCE",
               "DS_VT_ACE_OFG",
               "DS_VT_ESC_OCE",
               "NT_CE",
               "NT_GER",
               "NT_OBJ_CE",
               "TP_PRES",
               "TP_PR_GER"]

    return df[columns]

get_raw_data(url=ENADE_2023_CE_URL, extract_to='.')
raw_data = pd.read_csv("microdados2023_arq3.txt", sep=";", decimal=",", dtype=DTYPES, low_memory=False)

get_raw_data(url=ENADE_2023_QE_URL, extract_to='.')
raw_QE_data_2023 = pd.read_csv("microdados2023_arq4.txt", sep=";", decimal=",", dtype=DTYPES, low_memory=False)

get_raw_data(url=QE_2022_URL, extract_to='.')
data_QE = pd.read_csv("micro_QE_2022.csv", sep=";", decimal=",", dtype=DTYPES, low_memory=False)

raw_data = raw_data.merge(
database[['CO_CURSO', 'CO_IES', 'CO_GRUPO', 'NOME_CURSO', 'NOME_MUNIC_CURSO']],
on='CO_CURSO',
how='left')

merged_selected_data = raw_data.merge(
        cpc2023[['CO_CURSO','CO_CATEGAD', 'CO_ORGACAD']],
        on='CO_CURSO',
        how='left')

UFPA_raw_data = merged_selected_data[merged_selected_data.CO_IES == 569]
cod_grupo_list = UFPA_raw_data.CO_GRUPO.unique()
cod_curso = UFPA_raw_data.CO_CURSO.unique()

selected_data = filter_courses_results(merged_selected_data)
Enade_2023 = reduce_data(selected_data)

QE_data_2023 = raw_QE_data_2023.merge(
      Enade_2023[['CO_CURSO', 'TP_PRES', 'TP_PR_GER']].drop_duplicates()[['CO_CURSO', 'TP_PRES', 'TP_PR_GER']],
      on='CO_CURSO',
      how='left')

#PaulaM
UFPA_data = Enade_2023[Enade_2023.CO_IES == 569]

COURSE_CODES = {}

questions_sub_file_name = ['ENG_CIV','ENG_ELE','ARQ','ENG_COM', 'NUT', 'ENG_MEC', 'ENG_AMB','ENF', 'ENG_COM', 'ENG_MEC','AGR', 'ENG_AMB', 'FAR', 'ENG_ALI', 'MED', 'ENG_FLO', 'AGR', 'BIO', 'ENG_CIV', 'ENG_ELE', 'ENG_QUI', 'MED_VET', 'MED', 'ODO', 'FIS']
nome_arquivo_QS = []

for curso, file_name in zip(cod_curso,questions_sub_file_name):
      COURSE_CODES[curso] = [UFPA_data.loc[UFPA_data['CO_CURSO']==curso, 'CO_GRUPO'].iloc[0],
                             UFPA_data.loc[UFPA_data['CO_CURSO']==curso, 'NOME_CURSO'].iloc[0],
                             file_name,
                             UFPA_data.loc[UFPA_data['CO_CURSO']==curso, 'NOME_MUNIC_CURSO'].iloc[0]]

for col in QE_data_2023.columns:
  QE_data_2023[col] = QE_data_2023[col].fillna(0).astype(int)

def plot_count_graph(course_code: int, questions_list) -> None:
    course_ufpa_df = QE_data_2023[
        (QE_data_2023["CO_CURSO"] == course_code) &
        (QE_data_2023["TP_PRES"] == PRESENT_STUDENT_CODE) &
        (QE_data_2023["TP_PR_GER"] == PRESENT_STUDENT_CODE)
    ]

    um_e_dois = []
    tres_e_quatro = []
    cinco_e_seis = []
    sete_e_oito = []

    for q in questions_list:
        values_count = course_ufpa_df[q].value_counts(dropna=False).to_dict()

        for i in range(1, 9):
            values_count.setdefault(i, 0)

        um_e_dois.append(values_count[1] + values_count[2])
        tres_e_quatro.append(values_count[3] + values_count[4])
        cinco_e_seis.append(values_count[5] + values_count[6])
        sete_e_oito.append(values_count[7] + values_count[8])

    questions = [q.replace('QE_I', '') for q in questions_list]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Remover bordas
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Traçar as linhas
    ax.plot(questions, um_e_dois, label='Discordo Totalmente + Discordo', color='red')
    ax.plot(questions, tres_e_quatro, label='Discordo Parc. + Concordo Parc.', color='orange')
    ax.plot(questions, cinco_e_seis, label='Concordo + Concordo Totalmente', color='green')
    ax.plot(questions, sete_e_oito, label='Não sei responder + Não se aplica', color='gray')

    # ax.set_title("Distribuição das Respostas por Questão")
    # ax.set_xlabel("Questão")
    # ax.set_ylabel("Contagem de Respostas")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

    plt.tight_layout()

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        fig.savefig(tmp_img.name)
        plt.close(fig)
        count_chart_img = tmp_img.name

    return None, count_chart_img

# def plot_average_graph(course_code: int, questions_list, question_text):
#     course_ufpa_df = QE_data_2023[
#         (QE_data_2023["CO_CURSO"] == course_code) &
#         (QE_data_2023["TP_PRES"] == PRESENT_STUDENT_CODE) &
#         (QE_data_2023["TP_PR_GER"] == PRESENT_STUDENT_CODE)
#     ]

#     questions_average = []
#     for question in questions_list:
#         values = course_ufpa_df[~course_ufpa_df[question].isin([7, 8])][question].values
#         questions_average.append(round(np.mean(values), 2))

#     question_labels = [q.replace('QE_I', '') for q in questions_list]

#     df = pd.DataFrame({
#         'num_questao': question_labels,
#         'media_questao': questions_average,
#         'texto_questao': question_text
#     })

#     df['cor'] = df['media_questao'].apply(
#         lambda val: '#00712D' if val == df['media_questao'].max()
#         else '#F09319' if val == df['media_questao'].min()
#         else '#81A263'
#     )

#     graph = px.bar(
#         df, x='num_questao', y='media_questao',
#         color='cor', color_discrete_map="identity",
#         text='media_questao',
#         custom_data=['texto_questao']
#     )

#     graph.update_layout(
#         xaxis_type='category',
#         xaxis=dict(categoryorder='array', categoryarray=question_labels),
#         hoverlabel=dict(
#             bgcolor="white", font_size=16, namelength=-1, align='left'
#         ),
#         legend=dict(
#             orientation="h", yanchor="bottom", y=1.02,
#             xanchor="left", x=0, font=dict(size=14)
#         ),
#         yaxis_title=None,
#         xaxis_title=None
#     )

#     graph.update_traces(
#         textposition='outside',
#         hovertemplate="<b>Questão %{x}:</b> %{customdata[0]}",
#         showlegend=True,
#         textfont_size=13.5
#     )

#     # Nomear as legendas manualmente
#     graph.data[1].name = 'Maior média'
#     graph.data[2].name = 'Menor média'
#     graph.data[0].showlegend = False

#     # ✅ Renderiza imagem em memória com plotly.io
#     buf = BytesIO()
#     img_bytes = pio.to_image(graph, format="png")
#     buf.write(img_bytes)
#     buf.seek(0)

#     # ✅ Salva em arquivo temporário para uso no PDF
#     with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
#         tmp_img.write(buf.read())
#         average_chart_img = tmp_img.name

#     return graph, average_chart_img
  
def plot_average_graph(course_code: int, questions_list, question_text):
    course_ufpa_df = QE_data_2023[
        (QE_data_2023["CO_CURSO"] == course_code) &
        (QE_data_2023["TP_PRES"] == PRESENT_STUDENT_CODE) &
        (QE_data_2023["TP_PR_GER"] == PRESENT_STUDENT_CODE)
    ]

    questions_average = []
    for question in questions_list:
        values = course_ufpa_df[~course_ufpa_df[question].isin([7, 8])][question].values
        questions_average.append(round(np.mean(values), 2))

    question_labels = [q.replace('QE_I', '') for q in questions_list]

    df = pd.DataFrame({
        'num_questao': question_labels,
        'media_questao': questions_average,
        'texto_questao': question_text
    })

    # Definindo cores conforme maior e menor média
    max_val = df['media_questao'].max()
    min_val = df['media_questao'].min()

    df['cor'] = df['media_questao'].apply(
        lambda val: '#00712D' if val == max_val else '#F09319' if val == min_val else '#81A263'
    )

    # Criar gráfico com matplotlib
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.bar(df['num_questao'], df['media_questao'], color=df['cor'])

    # Adicionar rótulos
    for bar, value in zip(bars, df['media_questao']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{value:.2f}', ha='center', va='bottom', fontsize=15)

    # ax.set_title('Média por Questão')
    # ax.set_xlabel('Questão')
    # ax.set_ylabel('Média')
    # ax.set_ylim(0, max(df['media_questao']) + 1)
    # ax.
    
    # Remover bordas do gráfico
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    # Salvar como imagem para o PDF
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        fig.savefig(tmp_img.name)
        plt.close(fig)
        average_chart_img = tmp_img.name

    return None, average_chart_img  

def plot_performance_graph(group_code: int, course_code: int, ratio_graph=True, absolute_graph=True) -> None:
    
    fig1, fig2=None,None
    fig1_img, fig2_img=None,None

    #sk_national_df é o dataframe filtrado a partir do valor de CO_GRUPO informado (NACIONAL)
    sk_national_df = Enade_2023[Enade_2023["CO_GRUPO"] == group_code]

    #sk_ufpa_df é o dataframe filtrado a partir do valor de CO_CURSO informado (UFPA)
    sk_ufpa_df = sk_national_df[sk_national_df["CO_CURSO"] == course_code]

    questions_subjects_df = pd.read_csv(QUESTIONS_SUBJECTS_URL + COURSE_CODES[course_code][2] + "_questions_subjects.csv", sep=";") #, encoding='latin-1'

    subject_score_ufpa  = get_score_per_subject(questions_subjects_df, sk_ufpa_df)
    subject_score_national = get_score_per_subject(questions_subjects_df, sk_national_df)

    merged_score_df = pd.DataFrame({"Nota UFPA (%)":  subject_score_ufpa["Nota (%)"],
                                    "Nota Enade (%)": subject_score_national["Nota (%)"]
                                    }).set_index(subject_score_national["Conteúdo"])

    # Função lambda para calcular razão de acerto (axis=0: Aplicar o cálculo "por coluna"; axis=1: Aplicar o cálculo "em linha")
    ratio = lambda col: (col["Nota UFPA (%)"] / col["Nota Enade (%)"]).round(2)
    merged_score_df["Razão"] = merged_score_df.apply(ratio, axis=1)
    
    if ratio_graph:
        title = (
            f"Razão do percentual de acerto UFPA Brasil em {COURSE_CODES[course_code][1]} "
            f" {COURSE_CODES[course_code][3]} por tema no Enade 2023"
            f"Razão do percentual de acerto UFPA Brasil em {COURSE_CODES[course_code][1]} "
            f" {COURSE_CODES[course_code][3]} por tema no Enade 2023"
        )

        fig1, ax = plt.subplots(figsize=(6, 6))

        ax.spines[['top', 'right']].set_visible(False)
        ax.axvline(x=1.0, color="red")
        ax.grid(axis='x', color='white', linestyle='-')
        ax.set_xlabel("Razão do percentual de acerto")

        merged_score_df.sort_values(by=["Razão"], inplace=True)
        merged_score_df = merged_score_df[merged_score_df["Razão"].notnull()]

        labels = [
            fill(x, len(x) // 2 + 5) if len(x) > 60 else x
            for x in merged_score_df.index
        ]

        plt.barh(labels, merged_score_df["Razão"], color='k', height=0.6)

        r = 0.2
        min_xlim = round(min(merged_score_df["Razão"]) / r) * r
        xticks = np.linspace(min_xlim - r, 2 - min_xlim + r, 9)
        ax.set_xticks(xticks)
        ax.set_xticklabels([str(val) for val in xticks])
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

        for tick_label in ax.get_yticklabels():
            if "\n" in tick_label.get_text():
                tick_label.set_fontsize(12)

        if subject_score_national.shape[0] > 16:
            fig1.set_size_inches(8, 12)

        plt.xlim(min_xlim - r, 2 - min_xlim + r)

        fig1.suptitle(title, fontsize=15, x=0.25, y=0.93)  
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img1:
            fig1.savefig(tmp_img1.name, dpi=150, bbox_inches='tight')
            fig1_img = tmp_img1.name
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img1:
            fig1.savefig(tmp_img1.name, dpi=150, bbox_inches='tight')
            fig1_img = tmp_img1.name
    
    if absolute_graph:
        fig2, ax = plt.subplots(figsize=(8, 8))
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='x', color='white', linestyle='-')
        ax.set_xlabel("Percentual de acerto")

        title = (
            f"Percentual de acerto por tema em {COURSE_CODES[course_code][1]} "
            f"{COURSE_CODES[course_code][3]} no Enade 2023"
        )

        merged_score_df.sort_values(by=["Nota UFPA (%)", "Razão"], ascending=False, inplace=True)
        merged_score_df_filtered = merged_score_df[merged_score_df["Nota UFPA (%)"] != 0]

        ind = np.arange(merged_score_df_filtered.shape[0])
        width = 0.35

        labels = [
            fill(x, len(x) // 2 + 5) if len(x) > 60 else x
            for x in merged_score_df_filtered.index
        ]

        ax.barh(ind, merged_score_df_filtered["Nota UFPA (%)"], width, color='dodgerblue', label="UFPA")
        ax.barh(ind + width, merged_score_df_filtered["Nota Enade (%)"], width, color='mediumspringgreen', label="Brasil")

        ax.set(yticks=ind + width / 1, yticklabels=labels)
        ax.legend(fontsize="large", loc='lower right', fancybox=True, shadow=True)

        for tick_label in ax.get_yticklabels():
            if "\n" in tick_label.get_text():
                tick_label.set_fontsize(12)

        if subject_score_national.shape[0] > 16:
            fig2.set_size_inches(8, 12)

        plt.xlim(0, 100)
        plt.gca().invert_yaxis()

        fig2.suptitle(title, fontsize=18, x=0.28, y=0.93)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img2:
            fig2.savefig(tmp_img2.name, dpi=150, bbox_inches='tight')
            fig2_img = tmp_img2.name
        
    return fig1, fig1_img, fig2, fig2_img
    
def generate_pdf():
    # Verifica se todas as imagens necessárias estão no session_state
    required_charts = [
        'odp_img_av', 'infra_img_av', 'oaf_img_av',
        'odp_img_co', 'infra_img_co', 'oaf_img_co',
        'razao_chart', 'percent_chart'
    ]
    # missing = [key for key in required_charts if key not in st.session_state]
    # if missing:
    #     st.warning(f"Não foi possível gerar o PDF. Faltam os gráficos: {', '.join(missing)}")
    #     return

    # Inicializa PDF
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # pagina curso e municipio
    
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font("Times", "B", 23)
    pdf.cell(0, 10, "Relatório Análise dos Microdados ENADE 2023", ln=True, align='C')
    pdf.cell(0, 10, f'{st.session_state['curso_op']} - {st.session_state['municipio_op']}', ln=True, align='C')
   
    # pagina apresentação
    pdf.add_page()
    pdf.set_y(40)
    pdf.set_font("Times", "B", 19)
    pdf.set_text_color(19, 81, 180) 
    pdf.cell(0, 10, "Apresentação", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Times", size=12)
    pdf.set_text_color(0, 0, 0) 
    pdf.multi_cell(w=0, h=6, txt=(
        "A CPA, em parceria com a DIAVI/PROPLAN, apresenta as análises descritivas dos microdados do Enade 2023, com o objetivo de auxiliar as coordenações de curso na identificação de melhorias a serem implementadas na graduação."
    ), border=0, align="J")
    pdf.ln(2)
    pdf.multi_cell(w=0, h=6, txt=(
        "As análises compreendem os temas do Componente Específico da prova do Enade e as questões do Questionário do Estudante, relativas às dimensões Organização Didático-pedagógica, Infraestrutura e Instalações Físicas e Oportunidade Ampliação da Formação Profissional."
    ), border=0, align="J")
    pdf.ln(2)
    pdf.multi_cell(w=0, h=6, txt=(
        "As análises compreendem os temas do Componente Específico da prova do Enade e as questões do Questionário do Estudante, relativas às dimensões Organização Didático-pedagógica, Infraestrutura e Instalações Físicas e Oportunidade Ampliação da Formação Profissional."
    ), border=0, align="J")
    

    ### pagina apresentação conhecimento específico
    pdf.add_page()
    pdf.set_y(40)
    pdf.set_font("Times", "B", 19)
    pdf.set_text_color(19, 81, 180)
    pdf.cell(0, 10, "Análises Conhecimento Específico", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Times", size=12)
    pdf.set_text_color(0, 0, 0) 
    pdf.multi_cell(w=0, h=6, txt=(
        "A análise gráfica fornece informações valiosas a respeito do desempenho dos alunos nas temáticas avaliadas na prova, uma vez que possibilita averiguar se as estratégias pedagógicas aplicadas nas disciplinas ministradas estão produzindo os resultados almejados. São apresentados dois gráficos que exibem a comparação entre o desempenho do curso de graduação da UFPA e o desempenho nacional, calculado a partir do mesmo curso ofertado por todas as IES no país que participam do exame."
    ), border=0, align="J")
    pdf.ln(2)
    pdf.multi_cell(w=0, h=6, txt=(
        "O Gráfico da Razão do Percentual de Acerto exibe o desempenho do curso da UFPA em comparação com a média nacional, por tema avaliado no ENADE 2023. A interpretação do gráfico da razão é a seguinte: Razão > 2,0: a UFPA apresentou desempenho superior à média nacional; Razão < 2,0: a UFPA obteve desempenho inferior à média nacional; Razão = 2,0: o desempenho da UFPA foi equivalente à média nacional."
    ), border=0, align="J")
    pdf.ln(2)
    pdf.multi_cell(w=0, h=6, txt=(
        "O Gráfico de Percentual de Acerto por Tema apresenta a comparação entre o percentual de acertos do curso da UFPA e o percentual médio nacional, para cada temática do componente específico da prova."
    ), border=0, align="J")
    pdf.ln(2)
    pdf.multi_cell(w=0, h=6, txt=(
        "Na Tabela Ranking é apresentada a instituição com melhor percentual de desempenho, por temática do exame, em comparação com o desempenho do curso da UFPA."
    ), border=0, align="J")

    # graficos conhecimento especifico
    pdf.add_page()
    pdf.ln(10)
    pdf.image(st.session_state['razao_chart'], x=10, w=180)
    pdf.ln(2)
    pdf.set_font("Times", size=11)
    pdf.ln(2)
    pdf.cell(0,0,"Figura 1: Gráfico Razão do Percentual", align='C')
    pdf.ln(5)

    pdf.image(st.session_state['percent_chart'], x=10, w=180)
    pdf.ln(1)
    pdf.set_font("Times", size=11)
    pdf.cell(0,0,"Figura 2: Gráfico Percentual do Acerto", align='C')

    ### página apresentação questionario do estudante
    pdf.add_page()
    pdf.set_y(40)
    pdf.set_font("Times", "B", 19)
    pdf.set_text_color(19, 81, 180)    
    pdf.cell(0, 10, "Análises Questionário do Estudante", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Times", size=12)
    pdf.set_text_color(0, 0, 0)   
    pdf.multi_cell(w=0, h=6, txt=(
        "Para cada questão no Questionário do Estudante, são disponibilizadas 6 alternativas de resposta que indicam o grau de concordância com cada assertiva, "
        "em uma escala que varia de 1 (discordância total) a 6 (concordância total), além das alternativas 7 (Não sei responder) e 8 (Não se aplica)."
    ), border=0, align="J")
    pdf.ln(1)
    pdf.multi_cell(w=0, h=6, txt=(
        "Para cada dimensão do questionário, foram gerados dois gráficos. O gráfico de barras apresenta a média atribuída pelos alunos para cada questão, "
        "excluídas as alternativas 7 e 8. São destacadas as questões com a maior e a menor média."
    ), border=0, align="J")
    pdf.ln(1)
    pdf.multi_cell(w=0, h=6, txt=(
        "O gráfico de linhas representa, por questão, o total de respostas absolutas (contagem) agrupadas pelo tipo de alternativa escolhida, da seguinte forma: 1-2; 3-4; 5-6; 7-8."
    ), border=0, align="J")

    ### graficos odp
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.set_text_color(19, 81, 180)    
    pdf.cell(0, 10, "Organização Didático Pedagógica", ln=True)
    pdf.ln(3)
    pdf.set_font("Times", size=12)
    pdf.image(st.session_state['odp_img_av'], x=10, w=180)
    pdf.set_font("Times", size=11)
    pdf.set_text_color(0, 0, 0)   
    pdf.cell(0,0,"Figura 3: Gráfico de Médias Organização Didático-Pedagógica", align='C')
    
    pdf.image(st.session_state['odp_img_co'], x=10, w=180)
    pdf.set_font("Times", size=11)
    pdf.cell(0,0,"Figura 4: Gráfico de Linhas Organização Didático-Pedagógica", align='C')

    ### Página 4 – Infraestrutura
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.set_text_color(19, 81, 180)    
    pdf.cell(0, 10, "Infraestrutura e Instalações Físicas", ln=True)
    
    pdf.image(st.session_state['infra_img_av'], x=10, w=180)
    pdf.ln(1)
    pdf.image(st.session_state['infra_img_co'], x=10, w=180)

    ### Página 5 – Oportunidades de Ampliação da Formação
    pdf.add_page()
    pdf.cell(0, 10, "Oportunidades de Ampliação da Formação", ln=True)
    pdf.image(st.session_state['oaf_img_av'], x=10, w=180)
    pdf.ln(3)
    pdf.image(st.session_state['oaf_img_co'], x=10, w=180)
    
    # pagina anexo
    pdf.add_page()
    pdf.set_y(100)
    pdf.set_font("Times", "B", 19)
    pdf.cell(0, 10, "Anexo Questionário do Estudante", ln=True, align='L')

    # Salvar em arquivo temporário
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        pdf.output(tmp_pdf.name)
        # return tmp_pdf.name
    anexo_path = "anexo_qe_2023.pdf"
    capa_path= "src/file/capa_relatorio.pdf"

# Novo PDF combinando ambos
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as final_pdf:
        writer = PdfWriter()
        
        # lendo e inserindo capa pdf
        capa_pdf = PdfReader(capa_path)
        for page in capa_pdf.pages:
            writer.add_page(page)

        # ✅ 1. Adiciona páginas do PDF gerado com fpdf
        reader_fpdf = PdfReader(tmp_pdf.name)
        for page in reader_fpdf.pages:
            writer.add_page(page)

        # ✅ 2. Adiciona páginas do PDF existente
        reader_existente = PdfReader(anexo_path)
        for page in reader_existente.pages:
            writer.add_page(page)

        # ✅ 3. Escreve o PDF final com ambos os conteúdos
        writer.write(final_pdf)
        caminho_final = final_pdf.name

    # Agora `caminho_final` é o PDF completo
    return caminho_final    

#     anexo_path = "anexo_qe_2023.pdf"  # <- substitua com o caminho real

# # Novo PDF combinando ambos
#     with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as final_pdf:
#         writer = PdfWriter()

#         # Adiciona páginas do PDF gerado com fpdf
#         reader_fpdf = PdfReader(anexo_path)
#         for page in reader_fpdf.pages:
#             writer.add_page(page)

#         # Adiciona páginas do PDF existente
#         reader_existente = PdfReader(anexo_path)
#         for page in reader_existente.pages:
#             writer.add_page(page)

#         # Escreve o PDF final
#         writer.write(final_pdf)
#         return final_pdf.name

    
    # Botão de download
    # with open(temp_pdf_path, "rb") as f:
    #     st.download_button(
    #         "📄 Baixar PDF com Gráficos",
    #         data=f,
    #         file_name="graficos_dimensoes.pdf",
    #         mime="application/pdf"
    #     ) 
       
def get_subjects_per_question(questions_subjects_df: pd.DataFrame) -> pd.Series:

    subjects_columns = ["FIRST_SUBJECT", "SECOND_SUBJECT", "THIRD_SUBJECT"]

    subjects_per_question = (
        questions_subjects_df[subjects_columns]
        .stack()
        .value_counts()
        .sort_index()
        .astype(int)
    )
    return subjects_per_question.values


def get_invalid_subjects(questions_subjects_df: pd.DataFrame) -> list:
    invalid_subjects = questions_subjects_df.groupby("FIRST_SUBJECT")["VALIDITY"].any()
    invalid_subjects = invalid_subjects[~invalid_subjects].index.tolist()
    return invalid_subjects


def get_score_per_subject(questions_subjects_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:

    # Obtém uma lista de todos os temas distintos
    subjects = questions_subjects_df[["FIRST_SUBJECT","SECOND_SUBJECT","THIRD_SUBJECT"]].values.ravel('K')
    subjects = pd.Series(subjects).dropna().sort_values().unique()

    # Inicializa o DataFrame para armazenar os resultados dos assuntos
    subjects_score = pd.DataFrame({"Conteúdo" : subjects, "Acertos" : 0})

    # Colunas de questões relevantes
    question_columns = ["DS_VT_ACE_OCE", "DS_VT_ACE_OFG"]

    # Seleciona as respostas marcadas pelos participantes
    marked_keys = df[question_columns[0]]

    # Itera sobre as linhas do DataFrame de assuntos e contabiliza os acertos
    for index in range(questions_subjects_df.shape[0]):
        # Obtém os temas relacionados a uma questão específica
        subject_columns = questions_subjects_df.loc[index, ["FIRST_SUBJECT", "SECOND_SUBJECT", "THIRD_SUBJECT"]]
        subjects_to_update = subject_columns.dropna().values

        # Contabiliza os acertos para o(s) tema(s) relacionado(s) à questão atual
        result = marked_keys[marked_keys.str[index] == '1'].shape[0]

       # result = marked_keys[marked_keys.str[index].eq(1)].shape[0]
        subjects_score.loc[subjects_score["Conteúdo"].isin(subjects_to_update), "Acertos"] += result

    # Calcula a nota em porcentagem para cada tema
    subjects_per_question = get_subjects_per_question(questions_subjects_df)
    subject_score_column = subjects_score["Acertos"] * 100 / (subjects_per_question * df.shape[0])
    subjects_score["Nota (%)"] = subject_score_column.round(2)

    # Identifica e remove temas inválidos
    invalid_subjects = get_invalid_subjects(questions_subjects_df)
    subjects_score = subjects_score[~subjects_score["Conteúdo"].isin(invalid_subjects)]

    return subjects_score

#PLOTANDO TABELA
def show_best_hei_ranking_table(group_code:int, course_code:int, public_only:bool) -> None: #to_latex:bool = False
    """
    Exibe a tabela de classificação das melhores Instituições de Ensino Superior (IES)
    por tema, levando em consideração o desempenho dos cursos do grupo especificado.

    Parameters:
    ----------
    group_code : int
        Código do grupo a ser analisado.
    public_only : bool
        Flag indicando se devem ser consideradas apenas universidades públicas.
    to_latex : bool, optional
        Flag indicando se a tabela deve ser convertida para o formato LaTeX.
        O padrão é False.

    Returns:
    -------
    None

    Examples:
    -------
    >>> show_best_hei_ranking_table(4006)
    """

    # Carrega o DataFrame questions_subjects_df a partir de um arquivo CSV

    questions_subjects_df = pd.read_csv(QUESTIONS_SUBJECTS_URL
                                        + COURSE_CODES[course_code][2]
                                        + "_questions_subjects.csv", sep=";")

    # Carrega o DataFrame hei_df a partir de um arquivo CSV
    hei_df = pd.read_csv(HEI_CODES_URL)
    hei_dict = dict(hei_df.values)


    # Extrai os temas únicos do DataFrame questions_subjects_df
    subjects = pd.unique(questions_subjects_df[["FIRST_SUBJECT", "SECOND_SUBJECT", "THIRD_SUBJECT"]].values.ravel('K'))
    subjects = pd.Series(subjects).dropna().sort_values(ignore_index=True)

    # Obtém os temas inválidos
    invalid_subjects = get_invalid_subjects(questions_subjects_df)

    # Remove os temas inválidos da lista de temas
    subjects = np.setdiff1d(subjects, invalid_subjects)

    # Apenas universidades públicas federais
    if public_only:
        condition = (Enade_2023["CO_GRUPO"] == group_code) & \
                    (Enade_2023["CO_CATEGAD"] == PUBLIC_ADMIN_CATEGORY) & \
                    (Enade_2023["CO_ORGACAD"] == FEDERAL_ORG_CATEGORY)
    else:
        condition = (Enade_2023["CO_GRUPO"] == group_code)

    # Obtém os códigos das instituições de ensino
    hei_codes = pd.unique(Enade_2023.loc[condition, "CO_CURSO"])

    scores = []
    for code in hei_codes:
        # Filtra o DataFrame Enade_2023 pelos códigos de grupo e IES
        hei_df = Enade_2023[(Enade_2023["CO_GRUPO"] == group_code) & \
                            (Enade_2023["CO_CURSO"] == code)] #code

        # Obtém as notas por tema para a instituição de ensino
        score = get_score_per_subject(questions_subjects_df, hei_df)["Nota (%)"].values.tolist()
        scores.append([code, score])

    # Obtém os valores das notas por tema
    score_values = np.array([values[1] for values in scores])

   # Obtém as melhores notas por temas e as respectivas instituições de ensino
    best_hei_scores = [(scores[row][0], max_score)
                       for max_score, row in zip(np.max(score_values, axis=0),
                                                 np.argmax(score_values, axis=0))]


    # Separa os códigos e as notas por tema
    codes, subject_scores = zip(*best_hei_scores)


    # Obtém os nomes das instituições de ensino a partir dos códigos
    get_hei_code = lambda code: Enade_2023[Enade_2023["CO_CURSO"] == code]["CO_IES"].iloc[0]
    hei_data = [hei_dict.get(get_hei_code(code),
                             f"Código da IES: {get_hei_code(code)}")
                             for code in codes]

    # Obtém o número de participantes por instituição de ensino
    num_participants = [
        Enade_2023[
            (Enade_2023["CO_GRUPO"] == group_code) & \
            (Enade_2023["CO_CURSO"] == code)
        ].shape[0]
        for code in codes
    ]

    # Obtém as notas da UFPA por tema
    ufpa_df = Enade_2023[Enade_2023["CO_CURSO"] == course_code]
    ufpa_data = get_score_per_subject(questions_subjects_df, ufpa_df).reset_index()["Nota (%)"]

    # Cria uma lista com os dados para a tabela
    data = [subjects,
            hei_data,
            num_participants,
            subject_scores,
            ufpa_data]


    # Define as colunas do dataframe
    df_columns = ["Tema",
                  "IES com o melhor desempenho",
                  "Nº de participantes",
                  "Melhor curso",
                  "UFPA"]

    # Define os índices do dataframe como uma tupla de múltiplos níveis
    tuples = [("", "Tema"),
              ("", "IES com o melhor desempenho"),
              ("", "Nº de participantes"),
              ("Desempenho (%)", "Melhor curso"),
              ("Desempenho (%)", "UFPA")]

    idx = pd.MultiIndex.from_tuples(tuples)

    # Cria o DataFrame df_best_hei_per_subject
    df_best_hei_per_subject = pd.DataFrame(dict(zip(df_columns, data)))
    df_best_hei_per_subject.columns = idx
    
    return df_best_hei_per_subject
