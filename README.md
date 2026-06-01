# ⚖️ Compliance Trabalhista - RPA Jusbrasil

Este é um ecossistema de automação robótica de processos (RPA) desenvolvido em Python para a extração escalável, higienização e armazenamento de processos judiciais de múltiplas empresas diretamente do portal Jusbrasil. 

O projeto transforma uma rotina manual massiva de auditoria jurídica em um pipeline de dados automatizado e seguro, **reduzindo o tempo de execução diária de 4 horas para apenas 10 minutos (otimização de ~95%)**.

---

### 🚀 Funcionalidades Principais

* **Input Inteligente:** Leitura automatizada de planilhas de entrada para processamento em lote (*batch processing*) de nomes de empresas ou termos alvo.
* **Navegação e Extração Autônoma:** Automação de navegador em modo anônimo para varredura profunda (*scraping*) de dados textuais e metadados dos processos, contornando layouts assíncronos.
* **Tratamento e Higienização de Dados:** Uso de Expressões Regulares (RegEx) para limpeza de strings, remoção de caracteres especiais e padronização de campos estruturados através do Pandas.
* **Persistência Concorrente e Resiliência:** Salvamento imediato dos dados extraídos em banco de dados relacional para evitar perda de progresso, permitindo que a automação continue exatamente de onde parou caso seja interrompida.
* **Exportação Gerencial:** Geração automática de relatórios limpos e formatados em Excel para tomada de decisão e auditoria de compliance.

---

## 🛠️ Tecnologias Utilizadas

* **[Python 3.11](https://www.python.org/)** - Linguagem core do projeto.
* **[Selenium 4.20.0](https://www.selenium.dev/)** - Automação avançada de navegador e renderização dinâmica de páginas.
* **[Pandas 2.2.2](https://pandas.pydata.org/)** - Engenharia, manipulação e tratamento de estruturas de dados (DataFrames).
* **[SQLite3](https://www.sqlite.org/)** - Banco de dados relacional local para persistência de estado e garantia de resiliência.
* **[SQLAlchemy 2.0.29](https://www.sqlalchemy.org/)** - Abstração de banco de dados e ORM para consultas performáticas.

---

## 📐 Fluxo de Execução e Arquitetura do Pipeline

### 1️⃣ Primeiro Passo: Configuração do Input
O usuário insere o arquivo Excel contendo a lista de empresas a serem pesquisadas dentro do diretório `/input`, onde os dados serão mapeados e ingeridos pelo programa via Pandas.

![Configuração do arquivo de entrada](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/9b4aca9a-8840-4fe6-9a83-a137e1a7f2cb)

### 2️⃣ Segundo Passo: Execução e Automação Web
Ao iniciar a aplicação, o script inicializa o terminal de controle e orquestra o Selenium para abrir o navegador em **modo anônimo**. O robô executa as consultas sequencialmente de forma automatizada, aplicando técnicas de *Explicit Waits* para garantir estabilidade no carregamento das páginas.

![Terminal de execução do bot](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/943ca1ee-1c59-41c0-a336-ef9d4ca8e78a)

### 3️⃣ Terceiro Passo: Resiliência em Tempo de Execução
Enquanto a automação está ativa, a pasta `/output` gerencia arquivos temporários de banco de dados (`.db`) e arquivos de índice. Essa arquitetura de tolerância a falhas garante que, caso haja instabilidade de rede ou interrupção do sistema, o programa **retome o trabalho de onde parou**, sem reprocessar dados antigos.

![Arquivos temporários e banco de dados](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/9129db7d-9fc4-4868-808a-afe6a01aaf97?raw=true)

---

## 📊 Resultado Final

Após a conclusão da varredura de todas as empresas listadas, o robô realiza o tratamento final dos dados, consolida as informações e exporta o arquivo final criptografado e formatado `Processos Jusbrasil.xlsx` na pasta `/output`. Os arquivos temporários do banco de dados são limpos de forma autônoma pelo robô.

![Estrutura do arquivo final gerado](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/2f71260f-1f09-48f2-bde8-62f07860bf21)

Abaixo, a estrutura de dados e colunas perfeitamente higienizada e organizada pelo pipeline ao final do processo:

![Visualização da planilha Excel gerada](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA/assets/65497402/19f3263b-c7a5-449e-942a-4d3fabddbd9f)

---

## ⚙️ Como Executar o Projeto

```bash
# 1. Clone o repositório
git clone [https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA.git](https://github.com/FranciscoAlveJr/COMPLIENCE-TRABALHISTA.git)

# 2. Acesse o diretório do projeto
cd COMPLIENCE-TRABALHISTA

# 3. Instale as dependências necessárias
pip install -r requirements.txt

# 4. Adicione sua planilha na pasta input e execute a automação
python main.py
