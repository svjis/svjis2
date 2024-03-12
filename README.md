# SVJIS PY

Tento repozitář obsahuje pokus o reimplementaci [SVJIS](https://svjis.github.io/) do [Django](https://www.djangoproject.com/).

## 1 Instalace
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

Aplikace běží na adrese http://127.0.0.1:8000/ uživatel je `admin` heslo je `masterkey`. Heslo změňte v **Administrace - Uživatelé**.

## 3 Parametrizace

### 3.1 Údaje o SVJ

Nastavení údajů o SVJ je v aplikaci v sekci `Administrace`

### 3.2 Nastavení odesílání e-mailů

Systém SVJIS při různých událostech používá odesílání emailů, proto je správné nastavení e-mailového rozhraní pro funkci aplikace podstatné.

Vytvořte nový soubor `svjis/svjis/local_settings.py` a v něm vytvořte následující konfiguraci

```
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

Při testování aplikace ho můžete spouštět ručně. Při produkčním nastavení je potřeba nastavit plánovač systému (například cron) aby ho spoštěl v určitých itervalech (třeba každých 5 minut).

## 4 Spolupráce

Jakákoliv forma spolupráce je vítána. :octocat:
