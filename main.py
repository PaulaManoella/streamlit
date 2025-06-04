import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np

import dash
from dash import html, dcc
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

#####################


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
    
############################

for col in QE_data_2023.columns:
  QE_data_2023[col] = QE_data_2023[col].fillna(0).astype(int)

def plot_average_graph(course_code: int, questions_list):
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
    colors = ['#00712D' if val == max(questions_average) else '#F09319' if val == min(questions_average) else '#81A263' for val in questions_average]

    print(question_labels)
    graph = px.bar(x=question_labels, 
                   y=questions_average, 
                   color=colors, 
                   color_discrete_map="identity", 
                   text=questions_average)
    
    graph.update_layout(
    xaxis_type='category',
    xaxis=dict(
        categoryorder='array',
        categoryarray=question_labels
    ))

    graph.update_traces(textposition='outside')

    return graph

def plot_count_graph(course_code: int, questions_list) -> None: #, question_code: str , dimension:str
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

  plt.plot(questions, um_e_dois, marker='.')
  plt.plot(questions, tres_e_quatro, marker='.')
  plt.plot(questions, cinco_e_seis, marker='.')
  plt.plot(questions, sete_e_oito, marker='.')
  plt.xticks(fontsize=7)

  fig = px.line(x=questions, y=[um_e_dois, tres_e_quatro, cinco_e_seis, sete_e_oito])

  fig.update_layout(xaxis_type='category',
                    showlegend=False)

  return fig