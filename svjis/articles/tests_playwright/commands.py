def get_number():
    n = 0
    while True:
        n += 1
        yield n


def get_filename(cls, page, name):
    w = page.viewport_size['width']
    h = page.viewport_size['height']
    return f'{cls.test_output_dir}/{w}x{h}-{next(cls.numbering):04}-{name}.png'


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


def login(cls, page, user, password):
    page.goto(f"{cls.live_server_url}/")
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.wait_for_selector('id=login-submit')
    scrshot(page, get_filename(cls, page, f'login-{user}'))
    page.fill('[id=login-input]', user)
    page.fill('[id=password-input]', password)
    scrshot(page, get_filename(cls, page, f'login-{user}'))
    page.click('id=login-submit')
    scrshot(page, get_filename(cls, page, f'login-{user}'))


def logout(cls, page):
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.wait_for_selector('id=logout-submit')
    page.click('id=logout-submit')
    scrshot(page, get_filename(cls, page, 'logout'))


def fill_company(cls, page):
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    scrshot(page, get_filename(cls, page, 'admin-company'))
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
    scrshot(page, get_filename(cls, page, 'admin-company'))


def fill_building(cls, page):
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Building')
    scrshot(page, get_filename(cls, page, 'admin-building'))
    page.fill('[id=id_address]', 'Práčská 1')
    page.fill('[id=id_city]', 'Praha')
    page.fill('[id=id_post_code]', '102 00')
    page.fill('[id=id_land_registry_no]', 'KAT001')
    page.click('id=submit')
    page.wait_for_selector('text=Saved')
    scrshot(page, get_filename(cls, page, 'admin-building'))


def fill_entrances(cls, page):
    data = [{'description': 'vchod 1', 'address': 'Práčská 1'}, {'description': 'vchod 2', 'address': 'Práčská 2'}]
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Administration')
    if is_element_visible(page, 'div.menu-toggle'):
        page.click('.menu-toggle')
    page.click('text=Entrances')
    scrshot(page, get_filename(cls, page, 'admin-entrances'))
    for e in data:
        page.click('text=Add new entrance')
        page.fill('[id=id_description]', e['description'])
        page.fill('[id=id_address]', e['address'])
        scrshot(page, get_filename(cls, page, 'admin-entrances'))
        page.click('id=submit')
        page.wait_for_selector('text=Saved')
        scrshot(page, get_filename(cls, page, 'admin-entrances'))


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
    scrshot(page, get_filename(cls, page, 'admin-building-units'))
    for e in data:
        page.click('text=Add new unit')
        page.select_option('[id=id_type]', label=e['type'])
        page.select_option('[id=id_entrance]', label=e['entrance'])
        page.fill('[id=id_registration_id]', e['id'])
        page.fill('[id=id_description]', e['description'])
        page.fill('[id=id_numerator]', e['numerator'])
        page.fill('[id=id_denominator]', e['denominator'])
        scrshot(page, get_filename(cls, page, 'admin-building-units'))
        page.click('id=submit')
        page.wait_for_selector('text=Saved')
        scrshot(page, get_filename(cls, page, 'admin-building-units'))
