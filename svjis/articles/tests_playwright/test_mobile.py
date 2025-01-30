from .test_desktop import DesktopTests


class MobileTests(DesktopTests):

    device_width = 396
    device_height = 854
    test_output_dir = 'playwright_output/mobile'
