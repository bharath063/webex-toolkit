import pytest
import requests
import json
from unittest.mock import patch
from ..helper.webex_helper import WebexHelper

@pytest.mark.parametrize('text,expected', [('some test text', 7), ('', 4), ('one word', 6)])
def test_count_text_tokens(text, expected):
    webex_helper = WebexHelper("token")
    assert webex_helper.count_text_tokens(text) == expected