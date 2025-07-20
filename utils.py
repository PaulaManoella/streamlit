from main import UFPA_data

def atualiza_cursos(opcao):
        cursos = UFPA_data.query("NOME_MUNIC_CURSO == @opcao")['NOME_CURSO'].unique().tolist()
        cursos.sort()  
        print(cursos)
        return cursos