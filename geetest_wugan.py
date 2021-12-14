# -*- coding: utf-8 -*-
# https://www.geetest.com/demo/

import json
import time
import random
import requests
import traceback
from loguru import logger

logger.add("./log/wugan/geetest_wugan_log.log", rotation='00:00', level="WARNING", encoding='utf-8')


class ResultException(Exception):
    def __init__(self, error='ResultException'):
        Exception.__init__(self, error)
        self.error = error

    def __str__(self):
        return self.error


class Geetestlogin(object):
    def __init__(self):
        self.session = requests.session()
        self.url_challenge = "https://www.geetest.com/demo/gt/register-fullpage"
        self.url_gettype = "https://apiv6.geetest.com/gettype.php"  # 非必要请求
        self.url_resources = "https://apiv6.geetest.com/get.php"
        self.url_ajax = "https://api.geetest.com/ajax.php"
        self.api_fullpage_1 = "http://127.0.0.1:3000/api_fullpage/get_w"
        self.api_fullpage_2 = "http://127.0.0.1:3000/api_fullpage/get_ajax_w"

    @staticmethod
    def get_e() -> str:
        """
        :return: 加密所需的随机字符串
        """
        data = ""
        for i in range(4):
            data += (format((int((1 + random.random()) * 65536) | 0), "x")[1:])
        return data

    def get_gt_challenge(self) -> tuple:
        """
        获取gt以及challenge
        :return: gt,challenge,captchaKey
        """
        params = {
            "t": int(time.time() * 1000)
        }
        try:
            response = self.session.get(url=self.url_challenge, params=params)
            logger.debug(f"获取初始gt_challenge成功 -> {response.status_code, response.json()}")
            # self.session.get(self.url_gettype, params={"gt": response.json()["gt"]})
            return response.json()["gt"], response.json()["challenge"]
        except Exception as e:
            logger.error(f"参数解析失败 -> {response.text}")
            raise e

    def get_s_c(self, e_e: str, gt: str, challenge: str) -> dict:
        """
         获取验证的基本参数
        @param e_e:
        @param gt:
        @param challenge:
        @return:
        """
        api_payload = {
            "e": e_e,
            "gt": gt,
            "challenge": challenge
        }
        try:
            res_api = self.session.post(url=self.api_fullpage_1, data=api_payload).json()
            if res_api["msg"] == "success":
                req_params = {
                    "gt": gt,
                    "challenge": challenge,
                    "lang": "zh-cn",
                    "pt": 0,
                    "client_type": "web",
                    "w": res_api["data"],
                }
                response = self.session.get(url=self.url_resources, params=req_params)
                response_dict = response.text[1:-1]
                response_dict = json.loads(response_dict)
                logger.debug(f"获取验证的基本参数成功 -> {response.status_code, response_dict}")
                return response_dict["data"]["s"]
            else:
                raise ResultException("参数w获取失败")
        except ResultException as e:
            raise e
        except Exception as e:
            logger.error(f"参数解析失败 -> {response.text}")
            raise e

    def get_validate(self, e_e: str, gt: str, challenge: str, s: str):
        """
        获取验证方式
        @param e_e: 加密所需的随机字符串
        @param gt:
        @param challenge:
        @param s: 加密所需字符串,上一步请求的响应所得
        @return:
        """
        api_payload = {
            "e": e_e,
            "gt": gt,
            "challenge": challenge,
            "s": s
        }
        try:
            res_api = self.session.post(url=self.api_fullpage_2, data=api_payload).json()

            if res_api["msg"] == "success":
                req_params = {
                    "gt": gt,
                    "challenge": challenge,
                    "lang": "zh-cn",
                    "pt": 0,
                    "client_type": "web",
                    "w": res_api["data"],
                }
                response = self.session.get(url=self.url_ajax, params=req_params)
                response_dict = response.text[1:-1]
                response_dict = json.loads(response_dict)
                if response_dict["data"]["result"] == "success":
                    logger.warning(f"验证通过 -> {response_dict['data']}")
                    return response_dict["data"]["validate"]
                else:
                    logger.warning(f"验证不通过 -> {response_dict['data']}")
                    return None
            else:
                raise ResultException("参数w获取失败")
        except ResultException as e:
            raise e
        except Exception as e:
            logger.error(f"参数解析失败 -> {response.text}")
            raise e

    def main(self):
        try:
            gt, challenge = self.get_gt_challenge()
            e_e = self.get_e()
            s = self.get_s_c(e_e, gt, challenge)
            validate = self.get_validate(e_e, gt, challenge, s)
        except Exception:
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    geetest = Geetestlogin()
    geetest.main()
