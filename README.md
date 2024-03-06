# SVJIS PY

Tento repozitář obsahuje pokus o reimplementaci [SVJIS](https://svjis.github.io/) do [Django](https://www.djangoproject.com/).

## Instalace
Předpokládá se, že máte na počítači nainstalovaný python verze 3.10 a nebo vyšší.

```
python --version
```

Naklonujte si projekt
```
git clone https://github.com/svjis/svjis-py.git
cd svjis-py
```

Vytvořte si virtuální prostředí a přepněte se do něj
```
python -m venv venv
# v Linuxu
source venv/bin/activate
# ve Windows
source venv/Scripts/activate
```

Nainstalujte závislosti a vytvoře konfiguraci
```
pip install -r requirements.txt
cd svjis
python manage.py migrate
python manage.py setup_svjis
```

Abyste mohli zkompilovat překlady, budete potřebovat nainstalovanou utilitu `gettext`. Pokud jí nemáte, tak následující krok klidně přeskočte a aplikace bude dostupná jen v angličtině.
```
python manage.py compilemessages
```

## Spuštění

```
python manage.py runserver
```

Aplikace běží na adrese http://127.0.0.1:8000/ uživatel je `admin` heslo je `masterkey`. Heslo změňte v **Administrace - Uživatelé**.

## Spolupráce

Jakákoliv forma spolupráce je vítána. :octocat:
