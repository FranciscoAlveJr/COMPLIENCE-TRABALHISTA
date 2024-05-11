import pandas as pd
import os
import sqlalchemy

def criar():
    engine = sqlalchemy.create_engine("sqlite:///output/dados.db")
    conect = engine.connect()

    df = pd.read_sql('processos', conect)

    colunas = ['Nome da Empresa', 'Número do Processo', 'Título', 'Origem', 'Tipo de Ação']
    
    df = df.rename(columns=lambda x: colunas[df.columns.get_loc(x)])

    writer = pd.ExcelWriter('output/Processos Jusbrasil.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Planilha1', index=False)
    # wb = writer.book
    # ws = writer.sheets['Planilha1']

    # for i, col in enumerate(df.columns):
    #     column_len = max(df[col].astype(str).map(len).max(), len(col))
    #     ws.set_column(i, i, column_len)

    writer.close()

    conect.close()
    engine.dispose()

    os.remove('output/dados.db')

    print('Planilha criada.')

if __name__=="__main__":
   criar()

