import requests
import json

from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from helper.webex_helper import WebexHelper
from wxc_sdk import WebexSimpleApi


class WebexFetchMeetingsSchema(BaseModel):
    startDate: str = Field(
        ...,
        description="start date",
    )
    endDate: str = Field(
        ...,
        description="end date",
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
            startDate: The start date in iso8601 format.
            startDate: The end date in iso8601 format.

        Returns:
            Meetings fetched successfully. or No meetings found. or error message.
        """
        try:
            webex_token=self.get_tool_config("WEBEX_TOKEN")
            webex_helper=WebexHelper(webex_token)
            api = WebexSimpleApi(tokens=webex_token)
            meetings = [meeting.json() for meeting in api.meetings.list(_start=self.args.startDate, _end=self.args.endDate)]
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