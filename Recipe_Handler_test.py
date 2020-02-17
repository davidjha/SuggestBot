"""Recipe_Handler_test.py: Recipes_handler tests."""

__author__      = "Nicholas Leontiev"

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import Recipe_Handler as rh
r = rh.Recipe_Handler()

import unittest, requests

class TestRecipeHandlerMethods(unittest.TestCase):
	
    def test_rh_search(self):
        self.assertTrue(len(r.search_recipe()) > 0)
        self.assertTrue(len(r.search_recipe("potato")) > 0)

    def test_rh_recipe_exists(self):
        r.store_recipes("potato")
        self.assertTrue(r.recipe_exists("potato"))
        self.assertFalse(r.recipe_exists("tomato"))

if __name__ == "__main__":
	unittest.main()
