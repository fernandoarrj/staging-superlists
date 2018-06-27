from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		# Edith acessa a página inicial
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		time.sleep(1)

		# Ela percebe que a caixa de entrada está elegantamente centralizada
		inputbox = self.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

		# Ela inicia uma nova lista e vê que a entrada está elegantemente
		# centralizada aí também
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)