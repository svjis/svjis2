from .test_desktop import DesktopTests


class TabletTests(DesktopTests):

    device_width = 878
    device_height = 1000
    test_output_dir = 'playwright_output/tablet'
