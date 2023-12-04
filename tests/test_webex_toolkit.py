import pytest
from unittest.mock import patch, Mock

from ..webex_list_meetings import WebexFetchMeetingsTool
from ..webex_toolkit import Toolkit

def test_webex_toolkit_properties():
    toolkit = Toolkit()
    assert toolkit.name == "Webex Toolkit"
    assert toolkit.description == "Toolkit containing tools for performing Webex operations"

def test_get_tools():
    toolkit = Toolkit()
    tools = toolkit.get_tools()
    assert isinstance(tools, list)
    assert len(tools) == 1
    print(type(tools[0]))
    assert isinstance(tools[0], WebexFetchMeetingsTool)

def test_get_env_keys():
    toolkit = Toolkit()
    keys = toolkit.get_env_keys()
    assert isinstance(keys, list)
    assert len(keys) == 1
    assert keys == ["WEBEX_TOKEN"]