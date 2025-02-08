from .test_desktop import DesktopTests


class TabletTests(DesktopTests):

    device_width = 768
    device_height = 915
    test_output_dir = 'playwright_output/tablet'
