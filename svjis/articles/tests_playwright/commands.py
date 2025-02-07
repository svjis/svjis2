from datetime import datetime
from playwright.sync_api import expect

# Common functions


def get_number():
    n = 0
    while True:
        n += 1
        yield n


def get_filename(cls, name):
    return f'{cls.test_output_dir}/{next(cls.numbering):04}-{name}.png'


def scrshot(page, path, full_height=False):
    if full_height:
        w = page.viewport_size['width']
        h = page.viewport_size['height']
        full_height = page.evaluate("document.body.scrollHeight")
        if full_height > h:
            page.set_viewport_size({"width": w, "height": full_height})
    page.screenshot(path=path)
    if full_height:
        page.set_viewport_size({"width": w, "height": h})


def is_element_visible(page, selector):
    return page.is_visible(selector)


def click_link_in_row(page, text_to_find, i):
    rows = page.query_selector_all("table tr")

    for index, row in enumerate(rows):
        if text_to_find in row.inner_text():
            links = row.query_selector_all("a")
            if len(links) >= i:
                links[i].click()
                break


def show_menu(page):
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')


def menu(page, tray_menu_item, side_menu_item, is_exact):
    show_menu(page)
    page.locator('ul.menu').get_by_text(tray_menu_item, exact=is_exact).click()
    show_menu(page)
    page.locator('ul.side-menu__nav').get_by_text(side_menu_item, exact=is_exact).click()


# Login / Logout


def login(cls, page, user, password):
    page.goto(f"{cls.live_server_url}/")
    show_menu(page)
    page.wait_for_selector('id=login-submit')
    scrshot(page, get_filename(cls, f'login-{user}'))
    page.fill('[id=login-input]', user)
    page.fill('[id=password-input]', password)
    scrshot(page, get_filename(cls, f'login-{user}'))
    page.click('id=login-submit')
    scrshot(page, get_filename(cls, f'login-{user}'))


def logout(cls, page):
    show_menu(page)
    page.wait_for_selector('id=logout-submit')
    scrshot(page, get_filename(cls, 'logout'))
    page.click('id=logout-submit')
    scrshot(page, get_filename(cls, 'logout'))


# Administration


def fill_company(cls, page):
    menu(page, 'Administration', 'Company', True)
    scrshot(page, get_filename(cls, 'admin-company'))
    page.fill('[id=id_name]', 'Společenství vlastníků domu Práčská 1')
    page.fill('[id=id_address]', 'Práčská 1')
    page.fill('[id=id_city]', 'Praha')
    page.fill('[id=id_post_code]', '102 00')
    page.fill('[id=id_phone]', '+420 111 111')
    page.fill('[id=id_email]', 'pracska@seznam.cz')
    page.fill('[id=id_registration_no]', '123456')
    page.fill('[id=id_vat_registration_no]', 'CZ123456')
    page.fill('[id=id_internet_domain]', 'www.pracska.cz')
    page.set_input_files('[id=id_header_picture]', 'articles/tests_playwright/assets/Header_1.png')
    page.click('id=submit')
    scrshot(page, get_filename(cls, 'admin-company'))
    expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def fill_building(cls, page):
    menu(page, 'Administration', 'Building', True)
    scrshot(page, get_filename(cls, 'admin-building'))
    page.fill('[id=id_address]', 'Práčská 1')
    page.fill('[id=id_city]', 'Praha')
    page.fill('[id=id_post_code]', '102 00')
    page.fill('[id=id_land_registry_no]', 'KAT001')
    page.click('id=submit')
    scrshot(page, get_filename(cls, 'admin-building'))
    expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def fill_entrances(cls, page):
    data = [{'description': 'vchod 1', 'address': 'Práčská 1'}, {'description': 'vchod 2', 'address': 'Práčská 2'}]
    menu(page, 'Administration', 'Entrances', False)
    scrshot(page, get_filename(cls, 'admin-entrances'))
    for e in data:
        page.click('text=Add new entrance')
        page.fill('[id=id_description]', e['description'])
        page.fill('[id=id_address]', e['address'])
        scrshot(page, get_filename(cls, 'admin-entrances'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'admin-entrances'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def fill_building_units(cls, page):
    data = [
        {
            'type': 'Byt',
            'entrance': 'vchod 1, Práčská 1',
            'id': '001',
            'description': 'Byt 1',
            'numerator': '1',
            'denominator': '10',
        },
        {
            'type': 'Byt',
            'entrance': 'vchod 1, Práčská 1',
            'id': '002',
            'description': 'Byt 2',
            'numerator': '1',
            'denominator': '10',
        },
        {
            'type': 'Byt',
            'entrance': 'vchod 2, Práčská 2',
            'id': '003',
            'description': 'Byt 3',
            'numerator': '1',
            'denominator': '10',
        },
        {
            'type': 'Byt',
            'entrance': 'vchod 2, Práčská 2',
            'id': '004',
            'description': 'Byt 4',
            'numerator': '1',
            'denominator': '10',
        },
    ]
    menu(page, 'Administration', 'Building units', False)
    scrshot(page, get_filename(cls, 'admin-building-units'))
    for e in data:
        page.click('text=Add new unit')
        page.select_option('[id=id_type]', label=e['type'])
        page.select_option('[id=id_entrance]', label=e['entrance'])
        page.fill('[id=id_registration_id]', e['id'])
        page.fill('[id=id_description]', e['description'])
        page.fill('[id=id_numerator]', e['numerator'])
        page.fill('[id=id_denominator]', e['denominator'])
        scrshot(page, get_filename(cls, 'admin-building-units'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'admin-building-units'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def fill_users(cls, page):
    data = [
        {
            'salutation': 'Ing.',
            'first_name': 'Petr',
            'last_name': 'Staněk',
            'note': 'Předseda',
            'address': 'Práčská 1',
            'city': 'Praha',
            'postcode': '102 00',
            'country': 'CZ',
            'phone': '+420 111 111 111',
            'email': 'petr.stanek@myseznam.cz',
            'show_in_contacts': True,
            'login': 'petr',
            'password': cls.user_password,
            'enabled': True,
            'roles': ['Člen výboru', 'Redaktor', 'Vlastník'],
        },
        {
            'salutation': 'Mgr.',
            'first_name': 'Jana',
            'last_name': 'Hamplová',
            'note': 'Vlastník od 19.11.2020',
            'address': 'Práčská 2',
            'city': 'Praha',
            'postcode': '102 00',
            'country': 'CZ',
            'phone': '+420 211 111 111',
            'email': 'jana.hamplova@myseznam.cz',
            'show_in_contacts': False,
            'login': 'jana',
            'password': cls.user_password,
            'enabled': True,
            'roles': ['Vlastník'],
        },
        {
            'salutation': 'Pan',
            'first_name': 'Karel',
            'last_name': 'Lukáš',
            'note': 'Údržbář',
            'address': 'Kozinova 2',
            'city': 'Praha',
            'postcode': '102 00',
            'country': 'CZ',
            'phone': '+420 601 333 333',
            'email': 'karel@myseznam.cz',
            'show_in_contacts': False,
            'login': 'karel',
            'password': cls.user_password,
            'enabled': True,
            'roles': ['Řešitel'],
        },
        {
            'salutation': 'MUDr.',
            'first_name': 'Jaroslav',
            'last_name': 'Hranolek',
            'note': 'Vlastník od 21.11.2020',
            'address': 'Práčská 2',
            'city': 'Praha',
            'postcode': '102 00',
            'country': 'CZ',
            'phone': '+420 311 111 111',
            'email': 'jaroslav.hranolek@myseznam.cz',
            'show_in_contacts': True,
            'login': 'jaroslav',
            'password': cls.user_password,
            'enabled': True,
            'roles': ['Člen výboru', 'Redaktor', 'Vlastník'],
        },
        {
            'salutation': 'MUDr.',
            'first_name': 'Jiří',
            'last_name': 'Ovečka',
            'note': 'Vlastník od 21.11.2020',
            'address': 'Práčská 2',
            'city': 'Praha',
            'postcode': '102 00',
            'country': 'CZ',
            'phone': '+420 411 111 111',
            'email': 'jiri.ovecka@myseznam.cz',
            'show_in_contacts': True,
            'login': 'jiri',
            'password': cls.user_password,
            'enabled': True,
            'roles': ['Člen výboru', 'Redaktor', 'Vlastník'],
        },
        {
            'salutation': 'Prof.',
            'first_name': 'Tomáš',
            'last_name': 'Hampl',
            'note': 'Vlastník od 21.11.2020',
            'address': 'Práčská 2',
            'city': 'Praha',
            'postcode': '102 00',
            'country': 'CZ',
            'phone': '+420 511 111 111',
            'email': 'tomas.hampl@myseznam.cz',
            'show_in_contacts': True,
            'login': 'tomas',
            'password': cls.user_password,
            'enabled': True,
            'roles': ['Vlastník'],
        },
    ]
    menu(page, 'Administration', 'Users', False)
    scrshot(page, get_filename(cls, 'admin-users'))
    for e in data:
        page.click('text=Create new user')
        page.fill('[id=id_salutation]', e['salutation'])
        page.fill('[id=id_first_name]', e['first_name'])
        page.fill('[id=id_last_name]', e['last_name'])
        page.fill('[id=id_internal_note]', e['note'])
        page.fill('[id=id_address]', e['address'])
        page.fill('[id=id_city]', e['city'])
        page.fill('[id=id_post_code]', e['postcode'])
        page.fill('[id=id_country]', e['country'])
        page.fill('[id=id_phone]', e['phone'])
        page.fill('[id=id_email]', e['email'])
        if e['show_in_contacts']:
            page.check("input[type='checkbox']#id_show_in_phonelist")
        page.fill('[id=id_username]', e['login'])
        page.fill('[id=lpass-input]', e['password'])
        if e['enabled']:
            page.check("input[type='checkbox']#id_is_active")
        for r in e['roles']:
            page.check(f'[id="{r}-input"]')

        scrshot(page, get_filename(cls, 'admin-users'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'admin-users'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def fill_board(cls, page):
    data = [
        {'order': '1', 'member': 'Staněk Petr', 'position': 'předseda'},
        {'order': '2', 'member': 'Hranolek Jaroslav', 'position': 'místopředseda'},
        {'order': '3', 'member': 'Ovečka Jiří', 'position': 'člen'},
        {'order': '4', 'member': 'Hamplová Jana', 'position': 'revizor'},
    ]
    menu(page, 'Administration', 'Board', False)
    scrshot(page, get_filename(cls, 'admin-board'))
    for e in data:
        page.click('text=Add new member')
        page.fill('[id=id_order]', e['order'])
        page.select_option('[id=id_member]', label=e['member'])
        page.fill('[id=id_position]', e['position'])
        scrshot(page, get_filename(cls, 'admin-board'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'admin-board'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def fill_user_units(cls, page):
    data = [
        {'user': 'Hamplová', 'unit': 'Byt - 001 - Byt 1', 'description': 'Byt 1'},
        {'user': 'Staněk', 'unit': 'Byt - 002 - Byt 2', 'description': 'Byt 2'},
        {'user': 'Hranolek', 'unit': 'Byt - 003 - Byt 3', 'description': 'Byt 3'},
        {'user': 'Ovečka', 'unit': 'Byt - 004 - Byt 4', 'description': 'Byt 4'},
        {'user': 'Hampl', 'unit': 'Byt - 001 - Byt 1', 'description': 'Byt 1'},
    ]
    for e in data:
        menu(page, 'Administration', 'Users', False)
        click_link_in_row(page, e['user'], 1)
        scrshot(page, get_filename(cls, 'admin-user-units'))
        page.select_option('[id=owner-input]', label=e['unit'])
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'admin-user-units'))
        expect(page.locator('.main-content').get_by_text(e['user'])).to_be_visible()
        expect(page.locator('.main-content').get_by_text(e['description'])).to_be_visible()


# Redaction


def create_articles(cls, page):
    data = [
        {
            'header': 'Vítejte na nových stránkách SVJ',
            'perex': 'Milí uživatelé, rád bych vám představil nové stránky našeho SVJ.',
            'body': 'Na těchto stránkách Vás budeme informovat o všech nových událostech v domě.\n'
            'Doufáme, že budete spokojení.\n'
            'Váš výbor.',
            'menu': 'Vývěska',
            'comments': True,
            'publish': True,
            'visible': ['id_visible_for_all'],
            'attachments': [],
        },
        {
            'header': 'Nová úklidová firma',
            'perex': 'Vážení vlastníci, '
            'chtěli bychom Vás informovat, že od února převzala úklid v našem domě nová firma Blesk.',
            'body': '{uklid.jpg}\n'
            'V anketě na hlavní stránce se můžete vyjádřit zda jste s novou firmou spokojení.\n'
            'Váš výbor',
            'menu': 'Vývěska',
            'comments': True,
            'publish': True,
            'visible': ['id_visible_for_all'],
            'attachments': ['uklid.jpg'],
        },
        {
            'header': 'Podklady pro nadcházející shromáždění vlastníků',
            'perex': 'Vážení vlastníci v příloze pod článkem naleznete '
            'podklady pro shromáždění vlastníků, které se bude konat v pátek 2.4.2021.',
            'body': 'Viz. přílohy. \n\nVáš výbor.',
            'menu': 'Vývěska',
            'comments': False,
            'publish': True,
            'visible': ['id_visible_for_all'],
            'attachments': [],
        },
    ]
    for e in data:
        menu(page, 'Redaction', 'Articles', True)
        scrshot(page, get_filename(cls, 'redaction-article'))
        page.click('text=Create new article')
        page.fill('[id=id_header]', e['header'])

        page.wait_for_selector('#id_perex_ifr')
        page.wait_for_timeout(1000)
        locator = page.frame_locator('#id_perex_ifr')
        locator.locator('body').fill(e['perex'])

        page.wait_for_selector('#id_body_ifr')
        page.wait_for_timeout(1000)
        locator = page.frame_locator('#id_body_ifr')
        locator.locator('body').fill(e['body'])

        page.select_option('[id=id_menu]', label=e['menu'])
        if e['comments']:
            page.check('[id=id_allow_comments]')
        if e['publish']:
            page.check('[id=id_published]')
        for vis in e['visible']:
            page.check(f'[id={vis}]')
        scrshot(page, get_filename(cls, 'redaction-article'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'redaction-article'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()

        for f in e['attachments']:
            page.fill('[id=id_description]', f)
            page.set_input_files('[id=id_file]', f'articles/tests_playwright/assets/{f}')
            page.click('id=submit2')
            scrshot(page, get_filename(cls, 'redaction-article'))


def create_comments(cls, page):
    data = [
        {
            'header': 'Nová úklidová firma',
            'comment': 'Úklid se zlepšil.',
        },
    ]
    for e in data:
        menu(page, 'Articles', 'All articles', True)
        page.click('text=' + e['header'])
        page.fill('[id=body]', e['comment'])
        scrshot(page, get_filename(cls, 'redaction-article-comment'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'redaction-article-comment'))
        expect(page.locator('.main-content').get_by_text(e['comment'])).to_be_visible()


def search_for_article(cls, page):
    data = [
        {
            'search': 'nová',
            'article': 'Nová úklidová firma',
        },
    ]
    for e in data:
        menu(page, 'Articles', 'All articles', True)
        show_menu(page)
        page.fill('[id=search-input]', e['search'])
        scrshot(page, get_filename(cls, 'redaction-article-search'))
        page.click('id=search-submit')
        scrshot(page, get_filename(cls, 'redaction-article-search'))
        expect(page.locator('.main-content').get_by_text(e['article'])).to_be_visible()
        page.click('text=' + e['article'])
        scrshot(page, get_filename(cls, 'redaction-article-search'))


def create_news(cls, page):
    data = [
        {
            'body': 'Zprovozněny nové stránky výboru.',
            'publish': True,
        },
        {
            'body': 'V pátek 2.4.2021 se bude konat Shromáždění vlastníků jednotek.',
            'publish': True,
        },
    ]
    for e in data:
        menu(page, 'Redaction', 'News', True)
        scrshot(page, get_filename(cls, 'redaction-news'))
        page.click('text=Create new news')
        page.fill('[id=id_body]', e['body'])
        if e['publish']:
            page.check('[id=id_published]')
        scrshot(page, get_filename(cls, 'redaction-news'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'redaction-news'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def create_survey(cls, page):
    data = [
        {
            'description': 'Jste spokojeni s novou úklidovou firmou?',
            'options': ['Ano', 'Ne', 'Nevím'],
            'publish': True,
        },
    ]
    for e in data:
        menu(page, 'Redaction', 'Surveys', True)
        scrshot(page, get_filename(cls, 'redaction-survey'))
        page.click('text=Create new survey')
        page.fill('[id=id_description]', e['description'])
        page.locator('#id_starting_date').press_sequentially(datetime.today().strftime('%m%d%Y'))
        page.locator('#id_ending_date').press_sequentially(datetime.today().strftime('%m%d%Y'))
        i = 1
        for o in e['options']:
            page.fill(f'[id=o{i}-input]', o)
            page.click('id=add-option')
            i += 1
        if e['publish']:
            page.check('[id=id_published]')
        scrshot(page, get_filename(cls, 'redaction-survey'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'redaction-survey'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()


def vote_survey(cls, page):
    data = [
        {
            'user': 'petr',
            'vote': '1',
        },
        {
            'user': 'tomas',
            'vote': '1',
        },
        {
            'user': 'jana',
            'vote': '2',
        },
    ]
    for e in data:
        login(cls, page, e['user'], cls.user_password)
        menu(page, 'Articles', 'All articles', True)
        scrshot(page, get_filename(cls, 'survey-vote-' + e['user']))
        page.check('id=vote-' + e['vote'])
        page.click('id=survey-submit')
        scrshot(page, get_filename(cls, 'survey-vote-' + e['user']))
        expect(page.locator('.survey_box').locator('#survey-submit')).not_to_be_visible()
        logout(cls, page)


def create_useful_links(cls, page):
    data = [
        {
            'header': 'Důležité kontakty',
            'link': '/',
            'order': '10',
            'publish': True,
        },
        {
            'header': 'Stanovy společenství',
            'link': '/',
            'order': '20',
            'publish': True,
        },
        {
            'header': 'Domovní řád',
            'link': '/',
            'order': '30',
            'publish': True,
        },
    ]
    for e in data:
        menu(page, 'Redaction', 'Useful Links', True)
        scrshot(page, get_filename(cls, 'redaction-links'))
        page.click('text=Create new useful link')
        page.fill('[id=id_header]', e['header'])
        page.fill('[id=id_link]', e['link'])
        page.fill('[id=id_order]', e['order'])
        if e['publish']:
            page.check('[id=id_published]')
        scrshot(page, get_filename(cls, 'redaction-links'))
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'redaction-links'))
        expect(page.locator('#msg-info').get_by_text('Saved')).to_be_visible()
