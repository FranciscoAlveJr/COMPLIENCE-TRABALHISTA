from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import undetected_chromedriver as uc
from seleniumbase import Driver

from time import sleep
import sqlite3
from planilha import criar
import pandas as pd
import sqlalchemy
from glob import glob
import os
import logging
from dotenv import dotenv_values

class JusBrasil:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log')

        self.url = 'https://www.jusbrasil.com.br/processos/nome/36303582/transporte-versatil-ltda'

        self.colunas = ('empresa', 'NrProcesso', 'titulo', 'origem', 'tipoAcao')

        self.conn = sqlite3.connect('output/dados.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS processos {self.colunas}")
        self.conn.commit()

    def ler_planilha(self):
        arquivo = glob('input/*')[0]
        
        df = pd.read_excel(arquivo, dtype=str, na_filter=True)
        return df

    def load_db(self):
        self.conn = sqlite3.connect('output/dados.db')
        self.cursor = self.conn.cursor()

    def ler_dados(self):
        engine = sqlalchemy.create_engine("sqlite:///output/dados.db")
        conect = engine.connect()

        df = pd.read_sql('processos', conect)

        conect.close()
        engine.dispose()

        return df

    def driver_init(self):
        # service = Service(ChromeDriverManager().install())

        # self.driver = Chrome(service=service)

        options = Options()
        options.add_argument('--disable-popup-blocking')
        options.add_argument("--password-store=basic")
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )

        self.driver = Driver(uc=True, incognito=True)
        self.driver.maximize_window()
        self.wa = WebDriverWait(self.driver, 5)
        
    # def login(self):
    #     url = r'https://www.jusbrasil.com.br/login/email?next_url=https%3A%2F%2Fwww.jusbrasil.com.br%2F'

    #     env_values = dict(dotenv_values('.env'))
    #     email = env_values['email']
    #     senha = env_values['senha']

    #     self.driver.get(url)

    #     # Email
    #     self.wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormFieldset-email"]')))
    #     input_email = self.driver.find_element(By.XPATH, '//*[@id="FormFieldset-email"]')
    #     input_email.send_keys(email)

    #     sleep(1)

    #     btn_continue = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/button')
    #     btn_continue.click()

    #     # Senha
    #     self.wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="FormFieldset-password"]')))
    #     input_senha = self.driver.find_element(By.XPATH, '//*[@id="FormFieldset-password"]')
    #     input_senha.send_keys(senha)

    #     sleep(1)

    #     btn_entrar = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/button')
    #     btn_entrar.click()

    #     sleep(2)

    def pesquisar_processo(self, empresa: str):
        self.empresa = empresa
        url = 'https://www.jusbrasil.com.br/consulta-processual/'

        self.driver.get(url)

        try:
            self.wa.until(EC.presence_of_element_located((By.CLASS_NAME, 'LawsuitSearchForm-textField')))

            input_nome = self.driver.find_element(By.CLASS_NAME, 'LawsuitSearchForm-textField')
            input_nome.send_keys(empresa)

            sleep(1)

            btn_consultar = self.driver.find_element(By.XPATH, '//*[@id="app-root"]/div/main/div/div/div/section/div[2]/div/fieldset/div/button')
            btn_consultar.click()

        except TimeoutException:
            input_nome = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/section[1]/div/div[2]/div/form/div/div/div[1]/span/input')
            input_nome.send_keys(empresa)

            sleep(1)

            input_nome.send_keys(Keys.ENTER)

        # sleep(1)

        # self.wa.until(EC.presence_of_element_located((By.CLASS_NAME, 'SearchResults-content')))

        sleep(2)

        try:
            self.driver.find_element(By.CLASS_NAME, 'JusbrasilSurvey-contentWrapper')
            fechar = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/label/span')
            fechar.click()
        except NoSuchElementException:
            pass

        processo_links = self.driver.find_elements(By.CLASS_NAME, 'EntitySnippet-anchor-wrapper')
        first_link = processo_links[0].find_element(By.TAG_NAME, 'a')
        first_link.click()

    def acessar_processos(self):
        try:
            url = 'https://www.jusbrasil.com.br/processos/nome/36303582/transporte-versatil-ltda'

            # self.driver.get(url)

            self.wa.until(EC.presence_of_element_located((By.CLASS_NAME, 'PersonPage-bodyCard')))

            qtd_processos = self.driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div[1]/main/div[1]/div[1]/div/div/div[1]/div/div[2]/p/strong[1]/span').text
            qtd_processos = int(qtd_processos.replace('.', ''))

            try:
                with open('output/i_processo.txt') as file:
                    ini = int(file.read())
            except FileNotFoundError:
                ini = 0

            # while len(elementos) < qtd_processos:
            for i in range(ini, qtd_processos):
                with open('output/i_processo.txt', 'w') as file:
                    file.write(str(i))

                try:
                    elementos = self.driver.find_elements(By.CLASS_NAME, 'LawsuitCardPersonPage-title--link')
                    elemento = elementos[i]
                except IndexError:
                    dados = self.empresa, 'A empresa possui mais de 300 processos.', '', '', ''
                    self.conn.execute(f'INSERT INTO processos {self.colunas} VALUES (?,?,?,?,?)', dados)
                    self.conn.commit()
                    break

                nr_processo = elemento.find_element(By.CLASS_NAME, 'LawsuitCardPersonPage-header-processNumber').text
                nr_processo = nr_processo.replace('Processo', '')
                nr_processo = nr_processo.replace('nº ', '')

                titulo = elemento.find_element(By.CLASS_NAME, 'LawsuitCardPersonPage-header-processInvolved').text
                item_text = elemento.find_elements(By.CLASS_NAME, 'LawsuitCardPersonPage-body-row-item-text')

                try:
                    origem = item_text[0].text
                except IndexError:
                    origem = '-'
                try:
                    tipo_acao = item_text[1].text
                except IndexError:
                    tipo_acao = '-'

                dados = self.empresa, nr_processo, titulo, origem, tipo_acao

                self.conn.execute(f'INSERT INTO processos {self.colunas} VALUES (?,?,?,?,?)', dados)
                self.conn.commit()

                logging.info(f'{i+1} - Processo nº {nr_processo}')
                logging.info(f'Empresa: {self.empresa}')

                print(f'{i+1} - Processo nº {nr_processo}')
                print(f'Empresa: {self.empresa}')
                print(f'Título: {titulo}')
                print(f'Origem: {origem}')
                print(f'Tipo de Ação: {tipo_acao}')
                print()

                if len(elementos) < 300:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(1)
                else:
                    self.driver.execute_script("window.scrollTo(0, 0);")

                    #     infinite_btn = self.driver.find_element(By.CLASS_NAME, 'InfiniteList-retry-btn')
                    #     infinite_btn.click()
            
            with open('output/i_processo.txt', 'w') as file:
                file.write('0')
        except NoSuchElementException:
            pass

    def sair_da_conta(self):
        # self.wa.until(EC.presence_of_element_located((By.CLASS_NAME, '/html/body/div[2]/topbar/header/div/div/user-menu/div[1]')))

        self.driver.execute_script("window.scrollTo(0, 0);")

        sleep(1)

        btn_perfil = self.driver.find_element(By.XPATH, '/html/body/div[2]/topbar/header/div/div/user-menu/div[1]/img')
        btn_perfil.click()

        sleep(1)

        btn_sair = self.driver.find_element(By.CLASS_NAME, 'userMenu-item-link-logout')
        btn_sair.click()

if __name__=='__main__':
    try:
        jusbrasil = JusBrasil()
        jusbrasil.driver_init()
        # jusbrasil.login()
        
        df = jusbrasil.ler_planilha()
        nomes = df['Nome'].to_list()

        try:
            with open('output/i_empresa.txt') as file:
                ini = int(file.read())
            print('Continuando bot COMPLIENCE TRABALHISTA')
            logging.info('Continuando bot COMPLIENCE TRABALHISTA')
        except FileNotFoundError:
            ini = 0
            print('Iniciando bot COMPLIENCE TRABALHISTA')
            logging.info('Iniciando bot COMPLIENCE TRABALHISTA')
        
        print()

        for e in range(ini, len(nomes)):
            with open('output/i_empresa.txt', 'w') as file:
                file.write(str(e))
            try:
                nome = nomes[e]
                jusbrasil.pesquisar_processo(nome)
                jusbrasil.acessar_processos()
            except IndexError:
                continue
            sleep(1)
        # jusbrasil.sair_da_conta()
        sleep(1)
        jusbrasil.driver.quit()
        jusbrasil.conn.close()
        criar()

        os.remove('output/i_empresa.txt')
        os.remove('output/i_processo.txt')

        print('Trabalho Finalizado!')
        logging.info('Trabalho Finalizado!')
        sleep(2)
    except Exception as erro:
        logging.exception(erro)
        jusbrasil.sair_da_conta()
        sleep(1)
        jusbrasil.driver.quit()
        jusbrasil.conn.close()

        # try:
        #     with open('output/i_processo.txt') as file:
        #         ini = int(file.read())
        # except FileNotFoundError:
        #     ini = 0
        
        # for i in range(ini, len(elementos)):
        #     while True:
        #         try:
        #             with open('output/i_processo.txt', 'w') as file:
        #                 file.write(str(i))

        #             elemento = elementos[i]
        #             processo_link = elemento.get_attribute('href')

        #             self.driver.execute_script(f"window.open('{processo_link}', 'new_window')")              
        #             sleep(1)

        #             janelas = self.driver.window_handles
        #             self.driver.switch_to.window(janelas[1])

        #             try:
        #                 self.coletar(i)
        #             except NoSuchElementException:
        #                 try:
        #                     error_message = self.driver.find_element(By.CLASS_NAME, 'DisclaimerMessage-message-title')
        #                     print(error_message.text)
        #                     logging.info(error_message.text)
        #                 except NoSuchElementException as nosuch:
        #                     logging.exception('Não foram encontrados processos')
        #                     print('Não foram encontrados processos')
        #             except TimeoutException:
        #                 error_message = self.driver.find_element(By.CLASS_NAME, 'DisclaimerMessage-message-title')
        #                 print(error_message.text)
        #                 logging.info(error_message.text)

        #             sleep(1)

        #             self.driver.close()

        #             self.driver.switch_to.window(janelas[0])

        #             sleep(1)

        #             elementos = self.driver.find_elements(By.CLASS_NAME, 'LawsuitCardPersonPage-title--link')

        #             break
        #         except StaleElementReferenceException as st:
        #             logging.exception(st)
        #             elementos = self.driver.find_elements(By.CLASS_NAME, 'LawsuitCardPersonPage-title--link')
        #             sleep(1)
        #             continue

        # with open('output/i_processo.txt', 'w') as file:
        #     file.write(str(0))

    # def coletar(self, i):
    #     url = 'https://www.jusbrasil.com.br/processos/301934499/processo-n-003XXXX-4920208260100-do-tjsp'

    #     # self.driver.get(url)

    #     try:
    #         self.wa.until(EC.presence_of_element_located((By.CLASS_NAME, 'LawsuitHeader-heading')))
    #         titulo = self.driver.find_element(By.CLASS_NAME, 'LawsuitHeader-heading').text
    #     except TimeoutException:
    #         titulo = '-'
    #         pass

    #     try:
    #         nr_processo = self.driver.find_element(By.CLASS_NAME, 'LawsuitHeader-number').text
    #     except NoSuchElementException:
    #         nr_processo = self.driver.find_element(By.CLASS_NAME, 'LawsuitHeader-title').text

    #     nr_processo = nr_processo.removeprefix('Processo nº ')

    #     print(f'{i+1} - {nr_processo}')
    #     logging.info(f'{i+1} - {nr_processo}')

    #     valor = '-'
    #     situacao = '-'

    #     # VERIFICANDO SE TEM VALOR DA CAUSA
    #     try:
    #         valor = self.driver.find_element(By.CLASS_NAME, 'ClaimValue-value').text
    #         exibir_btn = self.driver.find_element(By.CLASS_NAME, 'ClaimValue-cta')
    #         if exibir_btn.text.strip() == "EXIBIR":
    #             exibir_btn.click()
    #             valor = self.driver.find_element(By.CLASS_NAME, 'ClaimValue-value').text
    #     except NoSuchElementException:
    #         pass

    #     area = self.driver.find_elements(By.CLASS_NAME, 'LawsuitHeader-infoArea-item')
    #     jurisdicao = area[0].text

    #     try:
    #         situacao = self.driver.find_element(By.CLASS_NAME, 'LawsuitCurrentSituation-completion').text
    #     except NoSuchElementException:
    #         try:
    #             situacao = self.driver.find_element(By.CLASS_NAME, 'LawsuitCurrentSituation-header-description').text
    #         except NoSuchElementException:
    #             pass

    #     # INFORMAÇÕES GERAIS
    #     mostrarmais_btn = self.driver.find_element(By.CLASS_NAME, 'LawsuitInformationModalTrigger-button')
    #     mostrarmais_btn.click()

    #     self.wa.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-content')))

    #     infos_list = self.driver.find_elements(By.CLASS_NAME, 'LawsuitInformationModal-section')
    #     infos_gerais = {
    #         'empresa': self.empresa,
    #         'nrProcesso': nr_processo,
    #         'valorCausa': valor,
    #         'jurisdicao': jurisdicao,
    #         'Assunto': '-',
    #         'Poder Judiciário': '-',
    #         'Início do processo': '-',
    #         'Natureza': '-',
    #         'situacao': situacao
    #     }

    #     for info in infos_list:
    #         key = info.find_element(By.CLASS_NAME, 'LawsuitInformationModal-section-title').text
    #         value = info.find_element(By.CLASS_NAME, 'LawsuitInformationModal-section-value').text

    #         if key == 'Envolvidos' or key == 'Juiz':
    #             break

    #         infos_gerais[key.strip()] = value.strip()
        
    #     dados = list(infos_gerais.values())

    #     logging.info(f'EMPRESA: {self.empresa}')
    #     print(f'EMPRESA: {self.empresa}')
    #     print(f'Título: {titulo}')
    #     print(f'Valor da Causa: {valor}')
    #     print(f'Jurisdição: {jurisdicao}')
    #     print(f'Assunto: {infos_gerais["Assunto"]}')
    #     print(f'Poder Judiciário: {infos_gerais["Poder Judiciário"]}')
    #     print(f'Início do Processo: {infos_gerais["Início do processo"]}')
    #     print(f'Natureza: {infos_gerais["Natureza"]}')
    #     print(f'Situação Atual: {situacao}')
    #     print()

    #     self.load_db()
    #     self.conn.execute(f'INSERT INTO processos {self.colunas} VALUES (?,?,?,?,?,?,?,?,?)', dados)
    #     self.conn.commit()
    #     self.conn.close()

    #     fechar_modal = self.driver.find_element(By.CLASS_NAME, 'modal-close')
    #     fechar_modal.click()
