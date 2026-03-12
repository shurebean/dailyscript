# Daily Scripts - 飞书群组自动任务脚本集

这个仓库包含用于飞书群组的自动化脚本。

## 脚本列表

### 1. send_toutiao_news_to_group.py
**功能**: 抓取今日头条热点新闻并发送到群组

**依赖**:
- Node.js (用于运行 toutiao_scraper.js.js 抓取新闻)
- OpenClaw CLI (用于发送消息)

**环境变量**:
- `FEISHU_NEWS_GROUP_ID`: 飞书群组ID（必填）

**定时任务**:
- 每日 07:00、15:00、23:00 运行

### 2. send_daily_reading_to_group.py
**功能**: 生成小学三年级每日学习朗读内容并发送到群组

**依赖**:
- OpenClaw CLI (用于发送消息)

**环境变量**:
- `FEISHU_READING_GROUP_ID`: 飞书群组ID（必填）

## 环境变量配置

创建 `.env` 文件或在系统环境变量中设置：

```bash
# 头条新闻群组ID
export FEISHU_NEWS_GROUP_ID="oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 每日阅读群组ID
export FEISHU_READING_GROUP_ID="oc_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
```

## 使用方法

### 直接运行

```bash
# 发送头条新闻
python3 send_toutiao_news_to_group.py

# 发送每日阅读
python3 send_daily_reading_to_group.py
```

### 配置 OpenClaw 定时任务

编辑 `/root/.openclaw/cron/jobs.json`:

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "toutiao_news_07:00",
      "name": "今日头条热点推送 07:00",
      "schedule": {
        "kind": "cron",
        "expr": "0 7 * * *",
        "tz": "Asia/Shanghai"
      },
      "command": "python3 /root/.openclaw/workspace/scripts/send_toutiao_news_to_group.py",
      "enabled": true
    },
    {
      "id": "toutiao_news_15:00",
      "name": "今日头条热点推送 15:00",
      "schedule": {
        "kind": "cron",
        "expr": "0 15 * * *",
        "tz": "Asia/Shanghai"
      },
      "command": "python3 /root/.openclaw/workspace/scripts/send_toutiao_news_to_group.py",
      "enabled": true
    },
    {
      "id": "toutiao_news_23:00",
      "name": "今日头条热点推送 23:00",
      "schedule": {
        "kind": "cron",
        "expr": "0 23 * * *",
        "tz": "Asia/Shanghai"
      },
      "command": "python3 /root/.openclaw/workspace/scripts/send_toutiao_news_to_group.py",
      "enabled": true
    },
    {
      "id": "daily_reading",
      "name": "每日阅读推送",
      "schedule": {
        "kind": "cron",
        "expr": "0 8 * * *",
        "tz": "Asia/Shanghai"
      },
      "command": "python3 /root/.openclaw/workspace/scripts/send_daily_reading_to_group.py",
      "enabled": true
    }
  ]
}
```

## 注意事项

1. 确保已安装 OpenClaw 并配置好飞书插件
2. 确保 `/home/toutiaotest/toutiao_scraper.js` 存在且可执行
3. 群组ID可以从飞书群聊链接中获取
4. 不要在代码中硬编码敏感信息（如群组ID），请使用环境变量

## 许可证

MIT
