from typing import Dict, List, NamedTuple

import db


class Category(NamedTuple):
    tag: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self):
        categories = db.fetchall(
            "category", "tag is_base_expense aliases".split()
        )
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories):
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["tag"])
            categories_result.append(Category(
                tag=category["tag"],
                is_base_expense=category["is_base_expense"],
                aliases=aliases
            ))
        return categories_result

    def get_all_categories(self):
        return self._categories

    def get_category(self, category_name):
        found = None
        other_category = None
        for category in self._categories:
            if category.tag == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        if not found:
            found = other_category
        return found
