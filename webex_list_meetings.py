from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
# from helper.webex_helper import WebexHelper
from wxc_sdk import WebexSimpleApi


import tiktoken

class WebexHelper:
    def __init__(self, webex_token):
        """
        Initializes the WebexHelper with the provided webex token.

        Args:
            Webex_token (str): Personal Webex token.
        """
        self.webex_token = webex_token
    
    @staticmethod
    def count_text_tokens(message: str) -> int:
        """
        Function to count the number of tokens in a text.

        Args:
            message (str): The text to count the tokens for.

        Returns:
            int: The number of tokens in the text.
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(message)) + 4
        return num_tokens


class WebexFetchMeetingsSchema(BaseModel):
    startDate: str = Field(
        ...,
        description="start date to list the webex meetings in iso8601 format",
    )
    endDate: str = Field(
        ...,
        description="end date to list the webex meetings in iso8601 format",
    )

class WebexFetchMeetingsTool(BaseTool):
    """
    Webex fetch Meetings tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "WebexFetchMeetings"
    description = (
        "A tool for fetching Webex meetings."
    )
    args_schema: Type[WebexFetchMeetingsSchema] = WebexFetchMeetingsSchema

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, startDate:str, endDate:str):
        """
        Execute the Webex fetch meetings tool.

        Args:
            startDate: The start date of list of webex meetings in iso8601 format.
            endDate: The end date of list of webex meetings in iso8601 format.

        Returns:
            Meetings fetched successfully. or No meetings found. or error message.
        """
        try:
            webex_token=self.get_tool_config("WEBEX_TOKEN")
            webex_helper=WebexHelper(webex_token)
            api = WebexSimpleApi(tokens=webex_token)
            startDate = "2023-12-04T00:00:00Z"
            endDate = "2023-12-06T00:00:00Z"
            if self.args.startDate:
                startDate = self.args.startDate
            if self.args.endDate:
                endDate = self.args.endDate
            lazy_meetings = api.meetings.list(_start=startDate, _end=endDate)
            meetings = [meeting.json() for meeting in lazy_meetings]
            api.meetings.create()
            if len(meetings)==0:
                return "No meetings found."
            try:
                final_result=""
                ok_meetings = []
                for index in range(0,len(meetings)):
                    meeting = meetings[index]
                    if webex_helper.count_text_tokens(final_result + ", " + meeting) > 3000:
                        break
                    final_result += ", " + meeting
                    ok_meetings.append(meeting)
                    
                final_result = ", ".join(ok_meetings) 
                final_result = f'{{ "meetings": [ {final_result} ] }}'
                return f"Webex meetings fetched successfully: {final_result}"
            except Exception as err:
                return f"Error: Unable to fetch webex meetings: {err}"
        except Exception as err:
            return f"Error: Unable to fetch webex meetings: {err}"