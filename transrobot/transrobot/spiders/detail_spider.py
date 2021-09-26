import scrapy
import time
import math

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from transrobot.items import PaymentDetailedItem

class DetailSpider(scrapy.Spider):
    name = "detail"
    total = 300

    def __init__(self, page, *args, **kwargs):
        super(DetailSpider, self).__init__(page, *args, **kwargs)
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.page = page

    def start_requests(self):
        response = scrapy.Request(
            url='https://santacruzdocapibaribe.pe.tenosoftsistemas.com.br/portal/v81/p_index_entidades/?municipio=47&represent=1',
            callback = self.parse
        )

        yield response

    def parse(self, response):
        self.driver.get(response.url)
        # Mudar de sleep para o wait do scrapy
        time.sleep(5)

        element = self.driver.find_element_by_xpath("//*[@id='conteudo-ents']/div/div[2]/div[1]")
        element.click()
        time.sleep(8)

        despesas = self.driver.find_element_by_xpath("//*[@id='megamenu-2']")
        despesas.click()
        time.sleep(5)

        despesas_detalhadas = self.driver.find_element_by_xpath("//*[@id='201']")
        despesas_detalhadas.click()
        time.sleep(15)

        WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "_iframe")))
        WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "_iframePLD")))

        select = Select(self.driver.find_element_by_xpath("//*[@id='id_sc_field_anoempenho']"))
        select.select_by_visible_text("Todos os anos")

        search = self.driver.find_element_by_xpath("//*[@id='main_table_form']/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[2]")
        search.click()
        time.sleep(30)

        WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframeGrid")))

        total_elements = self.driver.find_element_by_xpath("//*[@id='sc_grid_toobar_bot']/table/tbody/tr/td[3]/span").text
        total_elements = total_elements.split(' ')[-1]
        total_elements = int(total_elements[:len(total_elements) - 1])

        total_per_page = 410
        total_pages = math.ceil(total_elements / total_per_page)

        input_total_pages = self.driver.find_element_by_id("quant_linhas_f0_bot")
        input_total_pages.clear()
        input_total_pages.send_keys(str(total_per_page))
        view_total_elements = self.driver.find_element_by_xpath("//*[@id='qtlin_bot']")
        view_total_elements.click()
        # WebDriverWait(self.driver, 65).until(EC.presence_of_element_located((By.ID, 'rec_f0_bot')))
        time.sleep(65)

        input_go_to_page = self.driver.find_element_by_id("rec_f0_bot")
        input_go_to_page.clear()
        input_go_to_page.send_keys(str(self.page))
        go_to_page = self.driver.find_element_by_xpath("//*[@id='brec_bot']")
        go_to_page.click()
        time.sleep(40)
        self.driver.execute_script("window.scrollTo({ top: 0 });")

        gen = self.generate_items()
        for item in gen:
            yield item

        self.driver.close()


    def generate_items(self):
        table = self.driver.find_element_by_xpath("//*[@id='sc-ui-grid-body-e2a90ee9']/tbody")
        payment_item = PaymentDetailedItem()

        row_num = 0
        actual_row = 1
        rows = table.find_elements_by_xpath(".//tr")
        for row in rows:
            if row_num >= 3:
                current = self.driver.window_handles[0]

                # Confirma que apenas a janela com a listagem está aberta
                assert(len(self.driver.window_handles) == 1)

                row_id = row.get_attribute("id")
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="{row_id}"]/td[2]')))

                payment_item['id_empenho'] = self.driver.find_element_by_class_name("css_empenho_grid_line").text
                link_detalhamento = self.driver.find_element_by_xpath(f'//*[@id="{row_id}"]/td[2]')
                self.driver.execute_script("arguments[0].scrollIntoView({ block: 'nearest'});", link_detalhamento)
                link_detalhamento.click()

                WebDriverWait(self.driver, 15).until(EC.number_of_windows_to_be(2))

                new_window = [window for window in self.driver.window_handles if window != current][0]

                self.driver.switch_to.window(new_window)
                WebDriverWait(self.driver, 7).until(EC.presence_of_element_located((By.ID, "id_sc_field_numeroemp_1")))

                empenho_num = self.driver.find_element_by_xpath("//*[@id='id_sc_field_numeroemp_1']/span").text
                payment_item['num_empenho'] = empenho_num.split(':')[-1].strip()

                tipo_empenho = self.driver.find_element_by_xpath("//*[@id='id_sc_field_empenhotipo_1']/span").text
                payment_item['tipo_empenho'] = tipo_empenho.split(':')[-1].strip()

                especie_empenho = self.driver.find_element_by_xpath("//*[@id='id_sc_field_empenhoespecie_1']/span").text
                payment_item['especie_empenho'] = especie_empenho.split(':')[-1].strip()

                unidade_jur = self.driver.find_element_by_xpath("//*[@id='id_sc_field_unidadejurisdicionada_1']/span").text
                payment_item['unidade_jurisdicionada'] = unidade_jur.split(':')[-1].strip()

                unidade_orc = self.driver.find_element_by_xpath("//*[@id='id_sc_field_unidadeorca_1']/span").text
                payment_item['unidade_orcamentaria'] = unidade_orc.split(':')[-1].strip()

                historico_empenho = self.driver.find_element_by_xpath("//*[@id='id_sc_field_historicoempenho_1']/span").text
                payment_item['historico_empenho'] = historico_empenho.split(':')[-1].strip()

                data_empenho = self.driver.find_element_by_xpath("//*[@id='id_sc_field_emissaoempenho_1']/span").text
                payment_item['data_empenho'] = data_empenho.split(':')[-1].strip()

                cpf_cnpj = self.driver.find_element_by_xpath("//*[@id='id_sc_field_cpf_cnpj_credor_1']/span").text
                payment_item['cpf_cnpj'] = cpf_cnpj.split(':')[-1].strip()

                name_social = self.driver.find_element_by_xpath("//*[@id='id_sc_field_nomerazaosocial_1']/span").text
                payment_item['nome_razao_social'] = name_social.split(':')[-1].strip()

                tipo = self.driver.find_element_by_xpath("//*[@id='id_sc_field_tipocredor_1']/span").text
                payment_item['tipo'] = tipo.split(':')[-1].strip()

                funcao = self.driver.find_element_by_xpath("//*[@id='id_sc_field_funcao_1']/span").text
                payment_item['funcao'] = funcao.split(':')[-1].strip()

                subfuncao = self.driver.find_element_by_xpath("//*[@id='id_sc_field_subfuncao_1']/span").text
                payment_item['subfuncao'] = subfuncao.split(':')[-1].strip()

                programa = self.driver.find_element_by_xpath("//*[@id='id_sc_field_programa_1']/span").text
                payment_item['programa'] = programa.split(':')[-1].strip()

                acao = self.driver.find_element_by_xpath("//*[@id='id_sc_field_acao_1']/span").text
                payment_item['acao'] = acao.split(':')[-1].strip()

                categoria_economica = self.driver.find_element_by_xpath("//*[@id='id_sc_field_cateco_1']/span").text
                payment_item['categoria_economica'] = categoria_economica.split(':')[-1].strip()

                grupo_despesa = self.driver.find_element_by_xpath("//*[@id='id_sc_field_grudes_1']/span").text
                payment_item['grupo_despesa'] = grupo_despesa.split(':')[-1].strip()

                modalidade_aplicacao = self.driver.find_element_by_xpath("//*[@id='id_sc_field_modapl_1']/span").text
                payment_item['modalidade_aplicacao'] = modalidade_aplicacao.split(':')[-1].strip()

                elemento_despesa = self.driver.find_element_by_xpath("//*[@id='id_sc_field_eledes_1']/span").text
                payment_item['elemento_despesa'] = elemento_despesa.split(':')[-1].strip()

                subelemento_despesa = self.driver.find_element_by_xpath("//*[@id='id_sc_field_subeledes_1']/span").text
                payment_item['subelemento_despesa'] = subelemento_despesa.split(':')[-1].strip()

                licitacao_modalidade = self.driver.find_element_by_xpath("//*[@id='id_sc_field_modalidade_lic_1']/span").text
                payment_item['licitacao_modalidade'] = licitacao_modalidade.split(':')[-1].strip()

                licitacao_sequencial_modalidade = self.driver.find_element_by_xpath("//*[@id='id_sc_field_licnumprocedimento_1']/span").text
                payment_item['licitacao_sequencial_modalidade'] = licitacao_sequencial_modalidade.split(':')[-1].strip()

                yield payment_item

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])

                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, "conteudo")))
                WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "_iframe")))
                WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "_iframePLD")))
                WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframeGrid")))

                actual_row += 1

            row_num += 1
