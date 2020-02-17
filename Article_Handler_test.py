"""Article_Handler_test.py: Article Handler Tests."""

__author__      = "Roland Bell"
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import Article_Handler as ah
a = ah.Article_Handler()

import unittest, requests

class TestArticleHandlerMethods(unittest.TestCase):
	
	def test_ah_search_fail(self):
		with self.assertRaises(ValueError):
			a.search_article()

	def test_ah_search(self):
		self.assertTrue(len(a.search_article(keyword_string="democrats, republicans")) > 0)
		self.assertTrue(len(a.search_article(keyword_string="democrats, republicans")) < 280)

if __name__ == "__main__":
	unittest.main()
