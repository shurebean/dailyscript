#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日头条热点抓取并发送到群组
"""

import sys
import subprocess
import os

# 群组配置
TARGET_GROUP = os.getenv("FEISHU_GROUP_ID", "YOUR_GROUP_ID_HERE")

def fetch_toutiao_hot():
    """调用抓取脚本获取热点数据"""
    scraper_path = "/root/.openclaw/workspace/toutiao-hotspots/backend/scraper.py"
    
    try:
        result = subprocess.run(
            ["python3", scraper_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # 从输出中提取消息
            message = None
            for line in result.stdout.split('\n'):
                if line.startswith("MESSAGE_OUTPUT:"):
                    message = line.replace("MESSAGE_OUTPUT:", "")
                    break
            
            return message
        else:
            print(f"❌ 抓取脚本执行失败: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ 抓取超时")
        return None
    except Exception as e:
        print(f"❌ 抓取错误: {e}")
        return None

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
    
    # 抓取热点数据
    message = fetch_toutiao_hot()
    
    if message:
        # 发送到群组
        success = send_to_group(message)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)
