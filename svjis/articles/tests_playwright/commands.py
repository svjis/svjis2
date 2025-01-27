# Common functions


def get_number():
    n = 0
    while True:
        n += 1
        yield n


def get_filename(cls, name):
    return f'{cls.test_output_dir}/{next(cls.numbering):04}-{name}.png'


def scrshot(page, path):
    w = page.viewport_size['width']
    h = page.viewport_size['height']
    full_height = page.evaluate("document.body.scrollHeight")
    if full_height > h:
        page.set_viewport_size({"width": w, "height": full_height})
    page.screenshot(path=path)
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


# Login / Logout


def login(cls, page, user, password):
    page.goto(f"{cls.live_server_url}/")
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.wait_for_selector('id=login-submit')
    scrshot(page, get_filename(cls, f'login-{user}'))
    page.fill('[id=login-input]', user)
    page.fill('[id=password-input]', password)
    scrshot(page, get_filename(cls, f'login-{user}'))
    page.click('id=login-submit')
    scrshot(page, get_filename(cls, f'login-{user}'))


def logout(cls, page):
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.wait_for_selector('id=logout-submit')
    page.click('id=logout-submit')
    scrshot(page, get_filename(cls, 'logout'))


# Administration


def fill_company(cls, page):
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
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
    page.wait_for_selector('text=Saved')
    scrshot(page, get_filename(cls, 'admin-company'))


def fill_building(cls, page):
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Building')
    scrshot(page, get_filename(cls, 'admin-building'))
    page.fill('[id=id_address]', 'Práčská 1')
    page.fill('[id=id_city]', 'Praha')
    page.fill('[id=id_post_code]', '102 00')
    page.fill('[id=id_land_registry_no]', 'KAT001')
    page.click('id=submit')
    page.wait_for_selector('text=Saved')
    scrshot(page, get_filename(cls, 'admin-building'))


def fill_entrances(cls, page):
    data = [{'description': 'vchod 1', 'address': 'Práčská 1'}, {'description': 'vchod 2', 'address': 'Práčská 2'}]
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Entrances')
    scrshot(page, get_filename(cls, 'admin-entrances'))
    for e in data:
        page.click('text=Add new entrance')
        page.fill('[id=id_description]', e['description'])
        page.fill('[id=id_address]', e['address'])
        scrshot(page, get_filename(cls, 'admin-entrances'))
        page.click('id=submit')
        page.wait_for_selector('text=Saved')
        scrshot(page, get_filename(cls, 'admin-entrances'))


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
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Building units')
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
        page.wait_for_selector('text=Saved')
        scrshot(page, get_filename(cls, 'admin-building-units'))


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
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Users')
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
        page.wait_for_selector('text=Saved')
        scrshot(page, get_filename(cls, 'admin-users'))


def fill_board(cls, page):
    data = [
        {'order': '1', 'member': 'Staněk Petr', 'position': 'předseda'},
        {'order': '2', 'member': 'Hranolek Jaroslav', 'position': 'místopředseda'},
        {'order': '3', 'member': 'Ovečka Jiří', 'position': 'člen'},
        {'order': '4', 'member': 'Hamplová Jana', 'position': 'revizor'},
    ]
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Board')
    scrshot(page, get_filename(cls, 'admin-board'))
    for e in data:
        page.click('text=Add new member')
        page.fill('[id=id_order]', e['order'])
        page.select_option('[id=id_member]', label=e['member'])
        page.fill('[id=id_position]', e['position'])
        scrshot(page, get_filename(cls, 'admin-board'))
        page.click('id=submit')
        page.wait_for_selector('text=Saved')
        scrshot(page, get_filename(cls, 'admin-board'))


def fill_user_units(cls, page):
    data = [
        {'user': 'Hamplová', 'unit': 'Byt - 001 - Byt 1'},
        {'user': 'Staněk', 'unit': 'Byt - 002 - Byt 2'},
        {'user': 'Hranolek', 'unit': 'Byt - 003 - Byt 3'},
        {'user': 'Ovečka', 'unit': 'Byt - 004 - Byt 4'},
        {'user': 'Hampl', 'unit': 'Byt - 001 - Byt 1'},
    ]
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    for e in data:
        if is_element_visible(page, 'div.menu-toggle'):
            page.click('.menu-toggle')
        page.click('text=Users')
        click_link_in_row(page, e['user'], 1)
        scrshot(page, get_filename(cls, 'admin-user-units'))
        page.select_option('[id=owner-input]', label=e['unit'])
        page.click('id=submit')
        scrshot(page, get_filename(cls, 'admin-user-units'))


# Redaction


def create_articles(cls, page):
    data = [
        {
            'header': 'Vítejte na nových stránkách SVJ',
            'perex': 'Milí uživatelé, rád bych vám představil nové stránky našeho SVJ.',
            'body': 'Na těchto stránkách Vás budeme informovat o všech nových událostech v domě.'
            + ' \n\nDoufáme, že budete spokojení. \n\nVáš výbor.',
            'menu': 'Vývěska',
            'comments': True,
            'publish': True,
            'visible': ['id_visible_for_all'],
            'attachments': [],
        },
    ]
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Redaction')
    scrshot(page, get_filename(cls, 'redaction-article'))
    for e in data:
        if is_element_visible(page, 'div.menu-toggle'):
            page.click('.menu-toggle')
        page.locator("section.side-menu").locator("a", has_text="Articles").click()
        scrshot(page, get_filename(cls, 'redaction-article'))
        page.click('text=Create new article')
        page.fill('[id=id_header]', e['header'])

        locator = page.frame_locator("#id_perex_ifr")
        locator.locator("body").fill(e['perex'])

        locator = page.frame_locator("#id_body_ifr")
        locator.locator("body").fill(e['body'])

        page.select_option('[id=id_menu]', label=e['menu'])
        if e['comments']:
            page.check('[id=id_allow_comments]')
        if e['publish']:
            page.check('[id=id_published]')
        for vis in e['visible']:
            page.check(f'[id={vis}]')
        scrshot(page, get_filename(cls, 'redaction-article'))
        page.click('id=submit')
        page.wait_for_selector('text=Saved')
        scrshot(page, get_filename(cls, 'redaction-article'))
