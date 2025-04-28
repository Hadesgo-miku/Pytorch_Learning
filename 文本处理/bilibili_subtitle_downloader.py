import hashlib
import json
import time
from typing import List, Dict
import requests
from get_cid import get_cid_by_bvid
from subtitle_download import download_subtitles

class BiliSubtitleDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            # Cookie移动到headers外部的配置项
        }
        # 新增cookie配置（建议从环境变量读取）
        self.cookies = {
            "SESSDATA": "c483771a%2C1758795795%2Ca6678%2A32CjBBeBXvXG_8EwVzB2_jBN-3HfZKEJ2nnEnGXIGm2lyebrAyGH8YV6iRywT6WCjCx90SVnYwdFh4V0I3aUl5elQwcUJES1FqbjJaZmNGVVFnWFl6b0VIdjVSN0xiVTdYRW1xN0ctdjdUcHVGWlBCS2J6MHBvb0M0WjBqWWZpMlZvVTZ0RF9vVll3IIEC",
            "bili_jct": "2087b7de8dbff6c80c86c168b182d8b2",
            "sid": "6lrca326"
        }
        self.wbi_keys = []
        self._refresh_wbi_keys()  # 确保初始化时调用

    def _refresh_wbi_keys(self):
        """获取WBI签名密钥"""
        try:
            resp = self.session.get(
                "https://api.bilibili.com/x/web-interface/nav",
                headers=self.headers,
                timeout=5
            )
            data = resp.json()
            self.wbi_keys = [
                data['data']['wbi_img']['img_url'].split('/')[-1].split('.')[0],
                data['data']['wbi_img']['sub_url'].split('/')[-1].split('.')[0]
            ]
            print(f"已更新WBI密钥: {self.wbi_keys}")
        except Exception as e:
            print(f"更新WBI密钥失败: {str(e)}")

    def _get_wbi_sign(self, params: dict) -> dict:
        """生成WBI签名参数"""
        try:
            # 如果已有密钥则不再重复获取
            if not self.wbi_keys:
                self._refresh_wbi_keys()

            # 生成签名参数的核心逻辑
            mixin_key = ''.join(self.wbi_keys)
            sorted_params = dict(sorted(params.items()))
            query = '&'.join([f'{k}={v}' for k, v in sorted_params.items()])
            wts = str(int(time.time()))

            # 计算w_rid签名
            sign_str = f"{query}&wts={wts}&w_sk={mixin_key}"
            w_rid = hashlib.md5(sign_str.encode()).hexdigest()

            return {
                "wts": wts,
                "w_rid": w_rid
            }
        except Exception as e:
            print(f"生成签名失败: {str(e)}")
            return {}

    def get_aid_by_bvid(self, bvid: str) -> int:
        """通过bvid获取视频aid"""
        try:
            resp = self.session.get(
                "https://api.bilibili.com/x/web-interface/view",
                params={"bvid": bvid},
                headers=self.headers,
                cookies=self.cookies,
                timeout=5
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("code") == 0:
                return data["data"]["aid"]
            print(f"获取aid失败: {data.get('message')}")
        except Exception as e:
            print(f"获取aid异常: {str(e)}")
        return 0

    def fetch_subtitles(self, aid: int, cid: int) -> List[Dict]:
        """核心获取字幕方法"""
        params = {
            "aid": aid,
            "cid": cid,
            "web_location": 1550101,
            "spmid": "from_webpage"
        }
        signed_params = self._get_wbi_sign(params)
        full_params = {**params, **signed_params}  # 正确的位置定义

        try:
            resp = self.session.get(
                "https://api.bilibili.com/x/player/wbi/v2",
                params=full_params,
                headers=self.headers,
                cookies=self.cookies,
                timeout=10
            )
            # 在发送请求前添加
            print("最终请求头:", self.headers)
            print("完整请求参数:", full_params)
            print("最终请求URL:", resp.request.url)  # 添加请求URL打印
            resp.raise_for_status()

            if resp.json().get('code') == 412:
                print("需要更新签名密钥或添加cookies")
                return []

            #print(resp.json())
            return resp.json().get('data', {}).get('subtitle', {}).get('subtitles', [])
        except Exception as e:
            print(f"获取字幕失败: {str(e)}")
            return []

    def get_subtitles(self, bvid: str):
        """单视频调试入口"""
        aid = self.get_aid_by_bvid(bvid)
        cid = get_cid_by_bvid(bvid)
        if not (aid and cid):
            return []

        subtitles = self.fetch_subtitles(aid, cid)
        return [f"https:{sub['subtitle_url']}" for sub in subtitles if sub.get('subtitle_url')]


if __name__ == "__main__":
    downloader = BiliSubtitleDownloader()
    bvid_lst=['BV1Gf4y1y7wc']
    for bvid in bvid_lst:
        subtitle_url_lst = downloader.get_subtitles(bvid)

        for count,subtitle_url in enumerate(subtitle_url_lst):
            download_subtitles(subtitle_url,"subtitles/"+bvid+f'_{count+1}.srt')

