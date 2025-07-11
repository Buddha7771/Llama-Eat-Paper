from slack_sdk import WebClient


class SlackAPI:
    def __init__(self, token):
        self.client = WebClient(token)

    def post_thread_message(self, channel_id, message_ts, text=None, attachments=None):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts = message_ts,
            attachments=attachments,
        )
        return result

    def post_message(self, channel_id, text=None, attachments=None):
        """
        슬랙 채널에 메세지 보내기
        """
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            attachments=attachments
        )
        return result