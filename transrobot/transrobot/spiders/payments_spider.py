import scrapy
import time
import math

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from transrobot.items import PaymentItem, PaymentDetailedItem

class PaymentsSpider(scrapy.Spider):
    name = "payments"
    total = 300

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def start_requests(self):
        response = scrapy.Request(
            url='https://santacruzdocapibaribe.pe.tenosoftsistemas.com.br/portal/v81/p_index_entidades/?municipio=47&represent=1',
            callback = self.parse
        )

        yield response

    def parse(self, response):
        self.driver.get(response.url)
        # Mudar de sleep para o wait do scrapy
        time.sleep(10)

        element = self.driver.find_element_by_xpath("//*[@id='conteudo-ents']/div/div[2]/div[1]")
        element.click()
        time.sleep(10)

        despesas = self.driver.find_element_by_xpath("//*[@id='megamenu-2']")
        despesas.click()
        time.sleep(5)

        despesas_detalhadas = self.driver.find_element_by_xpath("//*[@id='201']")
        despesas_detalhadas.click()
        time.sleep(15)

        self.driver.switch_to_frame("_iframe")
        time.sleep(5)
        self.driver.switch_to_frame("_iframePLD")
        time.sleep(5)

        select = Select(self.driver.find_element_by_xpath("//*[@id='id_sc_field_anoempenho']"))
        select.select_by_visible_text("Todos os anos")

        search = self.driver.find_element_by_xpath("//*[@id='main_table_form']/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[2]")
        search.click()
        time.sleep(30)

        self.driver.switch_to_frame("iframeGrid")
        time.sleep(10)
        total_elements = self.driver.find_element_by_xpath("//*[@id='sc_grid_toobar_bot']/table/tbody/tr/td[3]/span").text
        total_elements = total_elements.split(' ')[-1]
        total_elements = int(total_elements[:len(total_elements) - 1])

        total_per_page = 10000
        total_pages = math.ceil(total_elements / total_per_page)

        input_total_pages = self.driver.find_element_by_id("quant_linhas_f0_bot")
        input_total_pages.clear()
        input_total_pages.send_keys(str(total_per_page))
        view_total_elements = self.driver.find_element_by_xpath("//*[@id='qtlin_bot']")
        view_total_elements.click()
        time.sleep(100)

        input_go_to_page = self.driver.find_element_by_id("rec_f0_bot")
        input_go_to_page.clear()
        input_go_to_page.send_keys(str(7))
        go_to_page = self.driver.find_element_by_xpath("//*[@id='brec_bot']")
        go_to_page.click()
        time.sleep(80)

        gen = self.generate_items()
        for item in gen:
            yield item


    def generate_items(self):
        table = self.driver.find_element_by_xpath("//*[@id='sc-ui-grid-body-e2a90ee9']/tbody")
        payment_item = PaymentItem()

        row_num = 0
        for row in table.find_elements_by_xpath(".//tr"):
            if row_num >= 3:
                payment_item['data'] = row.find_element_by_class_name("css_datapagamento_grid_line").text
                payment_item['empenho'] = row.find_element_by_class_name("css_empenho_grid_line").text
                payment_item['parcela'] = row.find_element_by_class_name("css_parcela_grid_line").text
                payment_item['tipo'] = row.find_element_by_class_name("css_tipoempenho_grid_line").text
                payment_item['favorecido'] = row.find_element_by_class_name("css_doccredor_grid_line").text

                valor_pago = row.find_element_by_class_name("css_valorpagamento_grid_line").text
                valor_pago = valor_pago.replace('.', '')
                valor_pago = valor_pago.replace(',', '.')
                payment_item['valor'] = float(valor_pago)

                yield payment_item

            row_num += 1
