# Přispívání do projektu

Pokud chcete přispět do projektu a zlepšit jej, Vaše pomoc je velmi vítána. Přispět můžete různými způsoby:

* můžete nahlásit závadu nebo požadavek v [issues](/svjis/svjis2/issues);
* můžete diskutovat a odpovídat na dotazy v [diskuzích](/orgs/svjis/discussions);
* můžete testovat nově přidané funkcionality;
* můžete si udělat fork projektu, udělat úpravy a poslat je zpět formou [pull-requestu](/svjis/svjis2/pulls)


## Před vytvořením pull-requestu

Než vytvoříte pull-request, tak si nainstalujte nástroj `pre-commit`.

Nainstalujte si závislosti pro vývoj:

```bash
pip install -r requirements-dev.txt
```

Pro kontrolu kvality kódu a dodržování konvencí používáme nástroj `pre-commit`. Pro jeho instalaci použijte příkaz:

```bash
pre-commit install
```

Před odesláním změn je důležité ověřit, že Váš kód nezpůsobuje žádné chyby. To můžete udělat pomocí unit testů:

```bash
python manage.py test
```

Před odesláním změn se ujistěte, že jste provedli všechny potřebné kroky:

1. Ověřte, že Váš kód splňuje všechny požadavky `pre-commit`.
1. Ověřte, že všechny testy procházejí.
1. Vytvořte novou větev pro Vaše změny.
1. Commitněte a pushněte Vaše změny.
1. Vytvořte pull request.


Děkujeme za Váš příspěvek do projektu! :octocat:
