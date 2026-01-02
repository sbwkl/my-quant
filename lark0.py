import warnings
# Filter pkg_resources deprecation warning from lark-oapi
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

import json
from dotenv import load_dotenv
import os
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

load_dotenv()

class LarkClient:
    def __init__(self):
        self.client = lark.Client.builder() \
            .app_id(os.getenv("LARK_APP_ID")) \
            .app_secret(os.getenv("LARK_APP_SECRET")) \
            .log_level(lark.LogLevel.INFO) \
            .build()

    def send_msg(self, msg: str):
        # 构造请求对象
        request: CreateMessageRequest = CreateMessageRequest.builder() \
            .receive_id_type("user_id") \
            .request_body(CreateMessageRequestBody.builder()
                .receive_id("2a5387c7")
                .msg_type("text")
                .content('{"text":"' + msg + '"}')
                .uuid("")
                .build()) \
            .build()

        # 发起请求
        response: CreateMessageResponse = self.client.im.v1.message.create(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return response.data

    def read_users(self, message_id: str):
        # 构造请求对象
        request: ReadUsersMessageRequest = ReadUsersMessageRequest.builder() \
            .message_id(message_id) \
            .user_id_type("user_id") \
            .build()

        # 发起请求
        response: ReadUsersMessageResponse = self.client.im.v1.message.read_users(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message.read_users failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return response.data

    def urgent_phone(self, message_id):
        # 构造请求对象
        request: UrgentPhoneMessageRequest = UrgentPhoneMessageRequest.builder() \
            .message_id(message_id) \
            .user_id_type("user_id") \
            .request_body(UrgentReceivers.builder()
                .user_id_list(["2a5387c7"])
                .build()) \
            .build()

        # 发起请求
        response: UrgentPhoneMessageResponse = self.client.im.v1.message.urgent_phone(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message.urgent_phone failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))

def main():
    client = LarkClient()
    # client.send_msg('看盘子la')

    # om_x100b5a452e435ca0b4c3da142fa47af
    # om_x100b5a476d81f0b0c384ce31f0cc368
    data = client.read_users('om_x100b5a476d81f0b0c384ce31f0cc368')

    # client.urgent_phone('om_x100b5a476d81f0b0c384ce31f0cc368')
    
# if __name__ == "__main__":
#     main()