from .test_desktop import DesktopTests


class MobileTests(DesktopTests):

    device_width = 384
    device_height = 670
    test_output_dir = 'playwright_output/mobile'
