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
