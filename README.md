# SVJIS PY

Tento repozitář obsahuje pokus o reimplementaci SVJIS do Django.

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
python manage.py createsuperuser
python manage.py compilemessages
```

## Spuštění

```
python manage.py runserver
```
