# SVJIS2

[![UnitTests](https://github.com/svjis/svjis2/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/svjis/svjis2/actions/workflows/unit-tests.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=svjis_svjis-py&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=svjis_svjis-py)

Informační systém pro SVJ :house_with_garden:

## Popis projektu

SVJIS je CMS pro Společenství Vlastníku Jednotek. Systém poskytuje redakční systém :memo:, diskuze pod článkem, aknkety :bar_chart:, hlášení a sledování závad, inzeráty, databázi vlastníků :family_man_woman_boy: včetně evidence jednotek a podílů. Více na [stránkách projektu](https://svjis.github.io/Vlastnosti/).


## 1 Instalace
Předpokládá se, že máte na počítači nainstalovaný python verze 3.10 a nebo vyšší.

```
python --version
```

Naklonujte si projekt
```
git clone https://github.com/svjis/svjis2.git
cd svjis2
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
python manage.py svjis_setup
```

Abyste mohli zkompilovat překlady, budete potřebovat nainstalovanou utilitu `gettext` - vyzkoušejte `gettext --version`. Pokud jí nemáte, tak následující krok klidně přeskočte a aplikace bude dostupná jen v angličtině.
```
python manage.py compilemessages
```

## 2 Spuštění

```
python manage.py runserver
```

Aplikace běží na adrese http://127.0.0.1:8000/ uživatel je `admin` heslo je `masterkey`. Heslo změňte v **Osobní nastavení - Změna hesla**.

Uvedený způsob spuštění je vhodný pro rychlé vyzkoušení aplikace na vašem počítači, nebo pro vývojáře. Pokud chcete SVJIS nasadit na server do produkce tak si prostudujte [Django dokumentaci](https://docs.djangoproject.com/en/5.0/howto/deployment/).

## 3 Parametrizace

### 3.1 Údaje o SVJ

Nastavení údajů o SVJ je v aplikaci v sekci `Administrace`

### 3.2 Nastavení odesílání e-mailů

Systém SVJIS při různých událostech používá odesílání emailů, proto je správné nastavení e-mailového rozhraní pro funkci aplikace podstatné.

Vytvořte nový soubor `svjis/svjis/local_settings.py` a v něm vytvořte následující konfiguraci

```
SECRET_KEY = 'produkcni django secret'
TIME_ZONE = 'Europe/Prague'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'vas smtp server'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'username k vasemu smtp serveru'
EMAIL_HOST_PASSWORD = 'heslo k vasemu smtp serveru'
```

Odesílání e-mailů se děje na pozadí - systém ukládá e-maily do fronty k odeslání, viz `Administrace - čekající zprávy`. Pro odeslání zprávy je třeba spustit následující příkaz:

```
python manage.py svjis_send_messages
```

Při testování aplikace ho můžete spouštět ručně. Při produkčním nastavení je potřeba nastavit plánovač systému (například cron) aby ho spoštěl v určitých itervalech (například každých 5 minut).

## 4 Spolupráce

Jakákoliv forma spolupráce je vítána. :octocat:
