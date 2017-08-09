import os
import sys
import unittest
import tempfile
import time

# Allows for importing from parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import brewer_network

test_wpa_supplicant = os.path.dirname(
    os.path.realpath(__file__)) + "/test_wpa_supplicant"


class BrewerNetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.app = brewer_network.app.test_client()
        if not os.path.isfile(test_wpa_supplicant):
            open(test_wpa_supplicant, "w")
        self.app.application.wpa_supplicant = test_wpa_supplicant

    def test_home_page(self):
        result = self.app.get("/")
        assert "Set Brewpi Wifi" in result.data

    def test_submit_form(self):
        result = self.app.post(
            "/write-supplicant",
            data=dict(
                ssid="ssid from testing :)",
                password="password from testing :D",
                priority="7"),
            follow_redirects=True)
        assert "Successful" in result.data
        assert "You don't have permission to write" not in result.data

    def test_submit_form_failure(self):
        result = self.app.post(
            "/write-supplicant",
            data=dict(
                ssid="ssid from testing :)",
                # No password field,
                priority="5"),
            follow_redirects=True)
        assert "400 Bad Request" in result.data

    def test_supplicant_window(self):
        result = self.app.get("/")
        assert "network={" not in result.data
        result = self.app.post(
            "/write-supplicant",
            data=dict(
                ssid="ssid from testing :)",
                password="password from testing :D",
                priority="7"),
            follow_redirects=True)
        assert "Set Brewpi Wifi" in result.data
        assert "network={" in result.data

    def tearDown(self):
        os.remove(test_wpa_supplicant)


if __name__ == '__main__':
    unittest.main()
