import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from textwrap import fill

import plotly.express as px


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
    
    #criando df com todas as infos (media, nome questao e texto questao)
    df = pd.DataFrame({
        'num_questao': question_labels,
        'media_questao': questions_average,
        'texto_questao': question_text
    })
    
    df['cor'] = df['media_questao'].apply(lambda val: '#00712D' if val == df['media_questao'].max() else '#F09319' if val == df['media_questao'].min() else  '#81A263')
        
    graph = px.bar(df, x='num_questao', 
                   y='media_questao', 
                   color='cor', 
                   color_discrete_map="identity", 
                   text='media_questao',
                   custom_data=['texto_questao'])
                   #hover_data=['text_qe'])
    
    graph.update_layout(
        xaxis_type='category',
        xaxis=dict(
            categoryorder='array',
            categoryarray=question_labels
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            namelength = -1,
            align='left'),
        legend=dict(orientation="h",  # Horizontal orientation for better top placement
                    yanchor="bottom", # Anchor the legend's bottom to the y coordinate
                    y=1.02,           # Position slightly above the plot area (y=1 is top of plot)
                    xanchor="left",  # Anchor the legend's right to the x coordinate
                    x=0,
                    font=dict(size=14)),
        # font=dict(size=18),
        yaxis_title=None,
        xaxis_title=None
    )

    graph.update_traces(textposition='outside',
                        hovertemplate="<b>Questão %{x}:</b> %{customdata[0]}",
                        showlegend=True,
                        textfont_size=13.5)
    
    graph.data[1].name = 'Maior média'
    graph.data[2].name = 'Menor média'
    graph.data[0].showlegend=False
    
    return graph

def plot_count_graph(course_code: int, questions_list) -> None: 
  course_ufpa_df = QE_data_2023[(QE_data_2023["CO_CURSO"] == course_code) &
                            (QE_data_2023["TP_PRES"] == PRESENT_STUDENT_CODE) &
                            (QE_data_2023["TP_PR_GER"] == PRESENT_STUDENT_CODE)]

  questions = questions_list

  values_sum=[]
  um_e_dois = []
  tres_e_quatro=[]
  cinco_e_seis=[]
  sete_e_oito=[]

  for q in questions:
    values_count = (course_ufpa_df[q].value_counts(dropna=False))
    index = values_count.index.to_list()
    values = values_count.values.tolist()

    dictio = {}
    for index, value in values_count.items():
      dictio[index] = value

    for i in range(1,9):
      if i in dictio:
        pass
      else:
        dictio.update({i: 0})

    dictio = dict(sorted(dictio.items()))

    values_sum = [dictio[1] + dictio[2], dictio[3] + dictio[4], dictio[5] + dictio[6], dictio[7] + dictio[8]]
    um_e_dois.append(values_sum[0])
    tres_e_quatro.append(values_sum[1])
    cinco_e_seis.append(values_sum[2])
    sete_e_oito.append(values_sum[3])

  fig = plt.figure(figsize= (4, 2))

  #removing QE_I for bar labels
  questions = [question.replace('QE_I', '') for question in questions]
  
  fig = px.line(x=questions, y=[um_e_dois, tres_e_quatro, cinco_e_seis, sete_e_oito]) 

  fig.update_layout(xaxis_type='category',
                    yaxis_title=None,
                    xaxis_title=None,
                    legend_title_text="",
                    legend_valign='middle',
                    legend=dict(
                        orientation="h",  
                        yanchor="bottom", 
                        y=1.02,           
                        xanchor="right",  
                        x=1),
                    hoverlabel=dict(
                        font_size=16)
                    )
  
  fig.update_traces(hovertemplate='Contagem de respostas: <b>%{y}</b><extra></extra>')
  
  fig.data[0].name = 'Total de respostas Discordo Totalmente e Discordo'
  fig.data[1].name = 'Total de respostas Discordo Parc. e Corcondo Parc.'
  fig.data[2].name = 'Total de respostas Concordo e Concordo Totalm.'
  fig.data[3].name = 'Total de respostas Não sei responder e Não se aplica'
  
  
  
  return fig

def plot_performance_graph(group_code: int, course_code: int, ratio_graph=True, absolute_graph=True) -> None:

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
            f"Razão do percentual de acerto UFPA-Brasil em {COURSE_CODES[course_code][1]} "
            f"- {COURSE_CODES[course_code][3]} por tema no Enade 2023"
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

        # Gráfico de Barras representando a UFPA e o Brasil
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
        
    return fig1, fig2
       
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
