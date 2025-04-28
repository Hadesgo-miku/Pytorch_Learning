import requests

def get_cid_by_bvid(bvid):
    """
    根据B站视频的bvid获取对应的cid。
    """
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    try:
        # 发送带请求头的GET请求
        response = requests.get(url, headers=headers)
        # 检查响应状态码
        response.raise_for_status()
        # 解析JSON数据
        data = response.json()
        # 检查返回的数据结构是否包含所需信息
        if data.get('code') == 0 and 'data' in data:
            # 优先检查直接cid字段
            if 'cid' in data['data']:
                return data['data']['cid']
            # 如果没有直接cid字段，检查分页信息
            elif 'pages' in data['data'] and len(data['data']['pages']) > 0:
                return data['data']['pages'][0]['cid']
            else:
                print("响应中未找到cid或分页信息")
                return None
        else:
            print(f"API返回错误: {data.get('message')}")
            return None
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except ValueError as e:
        print(f"解析JSON数据时出错: {e}")
        return None

# 示例使用
if __name__ == "__main__":
    bvid = "BV1VhoRY8E23"
    cid = get_cid_by_bvid(bvid)
    if cid:
        print(f"视频 {bvid} 的 cid 是: {cid}")
    else:
        print("无法获取到 cid。")