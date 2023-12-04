from abc import ABC
from typing import List

from superagi.tools.base_tool import BaseToolkit, BaseTool
from webex_list_meetings import WebexFetchMeetingsTool

class Toolkit(BaseToolkit, ABC):
    name: str = "Webex Toolkit"
    description: str = "Toolkit containing tools for performing Webex operations"

    def get_tools(self) -> List[BaseTool]:
        return [WebexFetchMeetingsTool()]

    def get_env_keys(self) -> List[str]:
        return ["WEBEX_TOKEN"]
