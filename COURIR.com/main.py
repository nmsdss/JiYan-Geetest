# -*- coding: utf-8 -*-
import re
import traceback
import requests
from loguru import logger
import execjs
from geetest_slide import Geetestlogin

logger.add("./log/slide/geetest_slide_log.log", rotation='00:00', level="WARNING", encoding='utf-8')


class Geetest_Courir:
    def __init__(self):
        self.host = "https://www.courir.com/"
        self.url_get_challenge = "https://geo.captcha-delivery.com/captcha/"
        self.url_get_cookie = "https://geo.captcha-delivery.com/captcha/check"
        with open("./static/js/get_captchaChallenge.js", "r", encoding="utf-8")as f:
            self.ctx = execjs.compile(f.read())
        self.headers = {
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        }
        self.session = requests.Session()
        self.session.headers = self.headers

    def get_initialCid_cid_hsh_CaptchaChallenge(self):
        response = self.session.get(url=self.host)
        re_obj = re.search("var dd=\{'cid':'(.*?)',", (response.text))
        initialCid = re_obj.group(1)
        cookie_cid = self.session.cookies.get_dict()["datadome"]
        captchaChallenge = self.ctx.call("ddExecuteCaptchaChallenge", cookie_cid, "10")
        logger.debug(f"Get success -> {initialCid, cookie_cid, captchaChallenge}")
        return initialCid, cookie_cid, captchaChallenge

    def get_gt_challenge(self, initialCid, cookie_cid) -> tuple:
        try:
            params = {
                "initialCid": initialCid,
                "hash": "00D958EEDB6E382CCCF60351ADCBC5",
                "cid": cookie_cid,
                "t": 'fe',
                "referer": 'https://www.courir.com/on/demandware.store/Sites-Courir-FR-Site',
                "s": '8985',
            }
            response = requests.get(url=self.url_get_challenge, params=params, headers=self.headers)
            res_text = response.text
            gt = re.search("gt: '(.*?)',", res_text).group(1)
            challenge = re.search("challenge: '(.*?)',", res_text).group(1)
            logger.debug(f"Get success - gt_challenge -> {response.status_code, gt, challenge}")
            return gt, challenge
        except Exception as e:
            logger.error(f"Get failed - gt_challenge")
            raise e

    def get_cookie(self, cookie_cid, initialCid, challenge, validate,captchaChallenge):
        try:
            params = {
                "cid": cookie_cid,
                "icid": initialCid,
                "ccid": 'null',
                "geetest-response-challenge": challenge,
                "geetest-response-validate": validate,
                "geetest-response-seccode": validate + '|jordan',
                "hash": "00D958EEDB6E382CCCF60351ADCBC5",
                "ua": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                "referer": 'https://www.courir.com/on/demandware.store/Sites-Courir-FR-Site',
                "parent_url": 'https://www.courir.com/',
                "x-forwarded-for": '',
                "captchaChallenge": captchaChallenge,
                "s": '8985',
            }
            response = self.session.get(url=self.url_get_cookie, params=params).json()
            logger.warning(f"The Cookie -> {response}")
            self.session.cookies.set('datadome', None)
            res = self.session.get(url="https://www.courir.com/on/demandware.store/Sites-Courir-FR-Site", cookies={"datadome":response["cookie"].split(";")[0].split("=")[-1]})
            with open("./index.html", "w", encoding="utf-8")as f:
                f.write(res.text)
        except Exception as e:
            raise e

    def main(self):
        try:
            initialCid, cookie_cid, captchaChallenge = self.get_initialCid_cid_hsh_CaptchaChallenge()
            gt, challenge = self.get_gt_challenge(initialCid, cookie_cid)
            challenge, validate = Geetestlogin().main(gt, challenge)
            self.get_cookie(cookie_cid, initialCid, challenge, validate, captchaChallenge)
        except Exception:
            logger.error(traceback.format_exc())


if __name__ == '__main__':
    cc = Geetest_Courir()
    cc.main()
