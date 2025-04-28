import requests
import json
import os  # 新增导入


def download_subtitles(subtitle_url, output_filename):
    if not subtitle_url.startswith("http"):  # 检查URL是否正确
        print(f"无效的URL: {subtitle_url}")
        return

    print(f"开始下载字幕，字幕ID: {subtitle_url}")  # Debugging print
    # 请求字幕API
    response = requests.get(subtitle_url)

    if response.status_code == 200:
        subtitle_data = response.json()

        # 检查返回的数据结构，并从 'body' 中提取字幕内容
        if 'body' in subtitle_data:
            subtitle_content = ""
            for item in subtitle_data['body']:
                # 组织每条字幕的时间戳和内容
                start_time = item['from']
                end_time = item['to']
                content = item['content']
                subtitle_content += f"{start_time} --> {end_time}\n{content}\n\n"


            # 将字幕内容保存为SRT文件
            with open(output_filename, 'w', encoding='utf-8') as file:
                file.write(subtitle_content)

            print(f"字幕已保存到 {output_filename}")  # Debugging print
        else:
            print("无法获取字幕内容，返回的数据没有 'body' 字段。")  # Debugging print
    else:
        print(f"无法下载字幕，状态码: {response.status_code}")  # Debugging print


if __name__ == "__main__":
    # 输入从开发者工具中获取的API URL
    subtitle_url = 'https://aisubtitle.hdslb.com/bfs/ai_subtitle/prod/11398079853941428321253033075f8d8849dc01218ff70352f8b79960?auth_key=1743350977-b4ea6538be8a481ca6ed301328dcd6a2-0-e36446fee26147372a9b1f0afeb41e58'

    # 检查URL是否为空
    if not subtitle_url:
        print("错误：未提供有效的字幕API URL。")
    else:
        # 下载字幕
        download_subtitles(subtitle_url, "subtitles/test")
        print('字幕下载已完成')