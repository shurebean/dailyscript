#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日头条热点抓取并发送到群组
使用 /home/toutiaotest/toutiao_scraper.js 进行抓取
"""

import sys
import subprocess
import os
import json
from datetime import datetime

# 群组配置
TARGET_GROUP = os.getenv("FEISHU_NEWS_GROUP_ID", "YOUR_NEWS_GROUP_ID")

def fetch_toutiao_hot():
    """调用 /home/toutiaotest/toutiao_scraper.js 抓取热点数据"""
    scraper_path = "/home/toutiaotest/toutiao_scraper.js"

    try:
        result = subprocess.run(
            ["node", scraper_path],
            cwd="/home/toutiaotest",
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("✅ 抓取脚本执行成功")
            print(result.stdout)

            # 从保存的文件中读取数据
            summary_path = "/home/toutiaotest/news/toutiao-hot.md"
            db_path = "/home/toutiaotest/backend/data/toutiao-news.json"

            # 优先读取数据库 JSON 文件
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data and len(data) > 0:
                        return format_message(data[0])
            
            # 备选：读取摘要文件
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return content[:1000]  # 限制长度

            return "抓取成功，但未能读取保存的数据"
        else:
            print(f"❌ 抓取脚本执行失败: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print("❌ 抓取超时")
        return None
    except Exception as e:
        print(f"❌ 抓取错误: {e}")
        return None

def format_message(data):
    """格式化数据为消息"""
    if not data:
        return "❌ 没有数据"

    timestamp = data.get('timestamp', '')
    news_list = data.get('news', [])
    count = data.get('count', 0)

    try:
        dt_str = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
    except:
        dt_str = timestamp

    message = f"📰 今日热点新闻 ({dt_str})\n\n"

    for i, item in enumerate(news_list[:10], 1):
        title = item.get('title', '')
        source = item.get('source', '未知')

        message += f"{i}. {title}\n"

    return message

def send_to_group(message):
    """发送消息到群组"""
    if not message:
        print("❌ 没有消息可发送")
        return False

    cmd = [
        "message",
        "send",
        "--channel", "feishu",
        "--target", TARGET_GROUP,
        "--message", message
    ]

    try:
        result = subprocess.run(
            ["openclaw"] + cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print(f"✅ 成功发送消息到群组 {TARGET_GROUP}")
            print(result.stdout)
            return True
        else:
            print(f"❌ 发送失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ 发送超时")
        return False
    except Exception as e:
        print(f"❌ 发送错误: {e}")
        return False

if __name__ == "__main__":
    print("📰 开始抓取今日头条热点...")
    print(f"使用脚本: /home/toutiaotest/toutiao_scraper.js\n")

    # 抓取热点数据
    message = fetch_toutiao_hot()

    if message:
        print("\n" + "="*60)
        print("准备发送的消息:")
        print("="*60)
        print(message)
        print("="*60 + "\n")

        # 发送到群组
        success = send_to_group(message)

        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)
