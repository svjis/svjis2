# Contributing to the Project

If you want to contribute to the project and improve it, your help is very welcome. You can contribute in various ways:

* You can report a bug or request in the [issues](https://github.com/svjis/svjis2/issues);
* You can discuss and answer questions in the [discussions](https://github.com/orgs/svjis/discussions);
* You can maintain translations to any language (see `svjis/articles/locale`);
* You can test newly added functionalities;
* You can fork the project, make modifications, and send them back as a [pull-request](https://github.com/svjis/svjis2/pulls)


## Before Creating a Pull Request

Install the development dependencies:

```bash
uv sync
source .venv/bin/activate
```

We use the `pre-commit` tool for code quality checks and adherence to conventions. To install it, use the command:

```bash
pre-commit install
```

Before submitting changes, it is important to verify that your code does not cause any errors. You can do this using unit tests:

```bash
python manage.py test articles.tests
```

To run Playwright tests, follow these steps:

```bash
playwright install
python manage.py test articles.tests_playwright
```

Before submitting changes, make sure you have completed all necessary steps:

1. Verify that your code meets all `pre-commit` requirements.
1. Ensure that all tests pass.
1. Create a new branch for your changes.
1. Commit and push your changes.
1. Create a pull request.

In case of any uncertainties, feel free to ask a question in the [discussions](https://github.com/orgs/svjis/discussions).

Thank you for your contribution to the project! :octocat:
