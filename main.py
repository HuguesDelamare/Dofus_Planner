"""
Module-level docstring briefly describing the purpose of the module.
"""
from scrap_dofus_app.classes.dofus_to_json_class import DofusItemScrapping
from dofus_web_app.flaskr import create_app


def main():
    create_app().run(debug=True)


if __name__ == '__main__':
    main()
