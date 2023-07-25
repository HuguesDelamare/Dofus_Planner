"""
Module-level docstring briefly describing the purpose of the module.
"""

from dofus_web_app.flaskr import create_app


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
