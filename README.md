# COMPLIENCE TRABALHISTA

## DESCRIÇÃO
Este é um bot para extração de dados do site Jusbrasil, que trata de processos de diversas empresas.<br><br>
Primeiramente, o bot lê uma planilha pré-formatada contendo nomes de empresas que o usuário quer pesquisar. Depois, ele abre o navegador automático para acessar o site Jusbrasil e preenche, automaticamente, os campos para a pesquisa. Ao encontrar os processos referentes a empresa, ele faz uma varredura no site para encontrar os dados disponíveis, fazendo a extração.<br><br> Os dados extraídos, então, são salvos em um banco de dados, para que possam ser devidamente tratados e, por fim, serem salvos em uma nova planilha em Excel.

## TECNOLOGIAS UTILIZADAS
- [Python 3.11](https://www.python.org/) (Linguagem de Programação)
- [Pandas 2.2.2](https://pandas.pydata.org/) (Tratamento de dados)
- [Selenium 4.20.0](https://www.selenium.dev/) (Automação de navegador)
- [SQLite3](https://www.sqlite.org/) (Armazenamento de dados)
- [SQLAlchemy 2.0.29](https://www.sqlalchemy.org/) (Leitura de dados)

## PRIMEIRO PASSO
O usuário coloca o arquivo Excel dentro da pasta input, onde será lido pelo programa.
![20240511_183018](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/9b4aca9a-8840-4fe6-9a83-a137e1a7f2cb)

## EXECUTANDO
Ao ser executado, o programa abre um terminal onde fará a inicialização. Logo depois, abre o navegador no modo anônimo, rodando automaticamente os nomes contidos na planilha.

![executar](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/943ca1ee-1c59-41c0-a336-ef9d4ca8e78a)

## RESULTADO
Após extrair os dados dos processos de todas as empresas lidas na planilha de origem, o arquivo "Processos Jusbrasil.xlsx" será salvo na pasta output, contendo a planilha com todos os dados extraídos.

![dados ](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/2f71260f-1f09-48f2-bde8-62f07860bf21)<br>
Enquanto o programa está rodando, a pasta output mantém o arquivo de banco de dados e arquivos de índice, para que o programa continue de onde parou, caso seja interrompido.

*******

![output](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/9129db7d-9fc4-4868-808a-afe6a01aaf97?raw=true)<br>
Depois de terminar o trabalho, o bot substitui os arquivos de dados pelo arquivo da planilha final.

*******

![planilha final](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/19f3263b-c7a5-449e-942a-4d3fabddbd9f)<br>
Como fica a planilha no final do trabalho.


