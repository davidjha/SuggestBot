"""SuggestBot_test.py: SuggestBot tests."""

__author__      = "David Ha"

import os, sys, inspect
import SuggestBot
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

sb = SuggestBot.SuggestBot()


class TestSuggestBot(unittest.TestCase):

    # Test article pulling and caching
    def test_article_pulling_and_caching(self):

        # Article object should not be in the cache
        article = sb.pull_article()
        self.assertFalse(article in sb.article_cache, msg="Found " + article + " in cache")

        # Article title should be in cache
        title = sb.get_title(article)
        self.assertTrue(title in sb.article_cache, msg="Did not find " + title + " in cache")

        # Article title should also match an entry in the file
        with open("posted_articles.txt", "r") as file:
            for line in file:
                if self.assertNotEqual(title, line):
                    self.assertEqual(line, title, msg="Found " + line + " \nbut should be " + title)
        file.close()

    # Test recipe pulling and caching
    def test_recipe_pulling_and_caching(self):

        recipe = sb.pull_recipe()
        title = sb.get_recipe_title(recipe)

        # Recipe matches an entry in file
        with open("posted_recipes.txt", "r+") as file:
            for line in file:
                if self.assertNotEqual(title, line):
                    self.assertEqual(title, line)
        file.close()

        # Recipe is found in cache
        self.assertTrue(title in sb.recipe_cache, msg="Did not find " + title + " in the cache")

    #def handle_duplicate_posts(self):
    #    sb.time_interval = 5

    #    for i in range(0, 5):
    #        sb.interval_post()


if __name__ == "__main__":
    unittest.main()
