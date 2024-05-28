## 1. Příprava prostředí

Předpokládáme, že máte nainstalovaný Python verze 3.10 nebo vyšší. Pro ověření verze Pythonu použijte příkaz:

```bash
python --version
```

### 1.1 Naklonování projektu

Pro začátek si naklonujte projekt do svého lokálního prostředí:

```bash
git clone https://github.com/svjis/svjis2.git
cd svjis2
```

### 1.2 Vytvoření a aktivace virtuálního prostředí

Vytvořte si virtuální prostředí a aktivujte ho:

```bash
python -m venv venv
# v Linuxu
source venv/bin/activate
# ve Windows
source venv/Scripts/activate
```

### 1.3 Instalace závislostí

Nainstalujte závislosti pro vývoj:

```bash
pip install -r requirements-dev.txt
```

### 1.4 Instalace pre-commit hook

Pro kontrolu kvality kódu a dodržování konvencí používáme nástroj `pre-commit`. Pro jeho instalaci použijte příkaz:

```bash
pre-commit install
```

## 2. Testování

Před odesláním změn je důležité ověřit, že váš kód nezpůsobuje žádné chyby. To můžete udělat pomocí unit testů:

```bash
python manage.py test
```

## 3. Odeslání změn

Před odesláním změn se ujistěte, že jste provedli všechny potřebné kroky:

1. Ověřte, že váš kód splňuje všechny požadavky `pre-commit`.
2. Ověřte, že všechny testy procházejí.
3. Vytvořte novou větev pro vaše změny.
4. Commitněte a pushněte vaše změny.
5. Vytvořte pull request.

Děkujeme za váš příspěvek k projektu! :octocat:
