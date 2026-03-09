#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小学三年级每日学习朗读内容生成器
"""

import random
import json
from datetime import datetime, timedelta

# 语文学习内容库（人教版小学三年级下册）
CHINESE_CONTENT = {
    "生字": [
        {"字": "燕", "拼音": "yàn", "意思": "鸟类，春天来临的象征", "重点": True},
        {"字": "聚", "拼音": "jù", "意思": "聚集，集合", "重点": True},
        {"字": "增", "拼音": "zēng", "意思": "增加，增添", "重点": True},
               {"字": "掠", "拼音": "lüè", "意思": "轻轻擦过", "重点": False},
        {"字": "沾", "拼音": "zhān", "意思": "浸湿，碰上", "重点": False},
        {"字": "瓣", "拼音": "bàn", "意思": "花瓣", "重点": True},
        {"字": "蓬", "拼音": "péng", "意思": "蓬松，茂盛", "重点": True},
        {"字": "胀", "拼音": "zhàng", "意思": "膨胀，鼓起", "重点": False},
    ],
    "课文": [
        """第1课《燕子》
一身乌黑的羽毛，一对轻快有力的翅膀，加上剪刀似的尾巴，凑成了那样可爱的活泼的小燕子。

二三月的春日里，轻风微微地吹拂着，如毛的细雨由天上洒落着，千万条的柔柳，红的黄的白的花，青的草，绿的叶，都像赶集似的聚拢来，形成了烂漫无比的春天。这时候，那些小燕子，那么伶俐可爱的小燕子，也由南方飞来，加入这光彩夺目的图画中，为春光平添了许多生趣。

小燕子带了它的剪刀似的尾巴，在阳光满地时，斜飞于旷亮无比的天空，叽的一声，已由这里的稻田上，飞到那边的高柳下了。""",
        """第2课《荷花》
清晨，我到公园去玩，一进门就闻到一阵清香。我赶紧往荷花池边跑去。

荷花已经开了不少了。荷叶挨挨挤挤的，像一个个碧绿的大圆盘。白荷花在这些大圆盘之间冒出来。有的才展开两三片花瓣儿。有的花瓣儿全展开了，露出嫩黄色的小莲蓬。有的还是花骨朵儿，看起来饱胀得马上要破裂似的。

这么多的白荷花，一朵有一朵的姿势。看看这一朵，很美；看看那一朵，也很美。如果把眼前的一池荷花看作一大幅活的画，那画家的本领可真了不起。

我忽然觉得自己仿佛就是一朵荷花，穿着雪白的衣裳，站在阳光里。一阵微风吹来，我就翩翩起舞，雪白的衣裳随风飘动。不光是我一朵，一池的荷花都在舞蹈。风过了，我停止舞蹈，静静地站在那儿。蜻蜓飞过来，告诉我清早飞行的快乐。小鱼在脚下游过，告诉我昨夜做的好梦……""",
        """第3课《昆虫备忘录》
我家的小院子里，种了一棵枣树。春天，枣树发芽了。嫩嫩的绿芽儿从树枝上钻出来，给光秃秃的树枝穿上了绿衣服。

夏天，枣树开花了。小小的花朵是黄绿色的，不引人注目，但散发出阵阵清香。我常常站在树下，闻着这淡淡的香味，觉得心里甜甜的。

秋天，枣树结果了。枣子先是青绿色的，慢慢地变成半红半绿的，最后变成红彤彤的，像一个个小灯笼挂在枝头上。我摘下一颗枣子，咬一口，又甜又脆，真好吃！"""
    ],
    "重点词语": [
        {"词": "乌黑", "意思": "形容颜色很黑", "重点": True},
        {"词": "轻快", "意思": "动作敏捷、轻松", "重点": True},
        {"词": "凑成", "意思": "拼凑而成", "重点": False},
        {"词": "烂漫", "意思": "颜色鲜明美丽", "重点": True},
        {"词": "光彩夺目", "意思": "形容鲜艳耀眼", "重点": True},
        {"词": "赶集", "意思": "到集市上买卖货物", "重点": False},
        {"词": "挨挨挤挤", "意思": "形容非常拥挤", "重点": True},
        {"词": "翩翩起舞", "意思": "形容轻快地跳舞", "重点": True},
        {"词": "清香", "意思": "清淡的香味", "重点": True},
        {"词": "饱胀", "意思": "形容果实饱满鼓起", "重点": True},
    ]
}

# 英语学习内容库（外研社小学三年级下册）
ENGLISH_CONTENT = {
    "单词": [
        {"word": "subject", "phonetic": "[ˈsʌbdʒɪkt]", "chinese": "学科", "重点": True},
        {"word": "Chinese", "phonetic": "[ˌtʃaɪˈniːz]", "chinese": "语文", "重点": True},
        {"word": "Maths", "phonetic": "[mæθs]", "chinese": "数学", "重点": True},
        {"word": "English", "phonetic": "[ˈɪŋɡlɪʃ]", "chinese": "英语", "重点": True},
        {"word": "PE", "phonetic": "[piː iː]", "chinese": "体育", "重点": False},
        {"word": "Music", "phonetic": "[ˈmjuːzɪk]", "chinese": "音乐", "重点": False},
        {"word": "Art", "phonetic": "[ɑːt]", "chinese": "美术", "重点": False},
        {"word": "Science", "phonetic": "[ˈsaɪəns]", "chinese": "科学", "重点": True},
        {"word": "favourite", "phonetic": "[ˈfeɪvərɪt]", "chinese": "最喜欢的", "重点": True},
        {"word": "smart", "phonetic": "[smɑːt]", "chinese": "聪明的", "重点": True},
        {"word": "hard-working", "phonetic": "[hɑːd ˈwɜːkɪŋ]", "chinese": "努力的", "重点": True},
        {"word": "week", "phonetic": "[wiːk]", "chinese": "周，星期", "重点": True},
        {"word": "Monday", "phonetic": "[ˈmʌndeɪ]", "chinese": "星期一", "重点": True},
        {"word": "Tuesday", "phonetic": "[ˈtjuːzdeɪ]", "chinese": "星期二", "重点": True},
        {"word": "Wednesday", "phonetic": "[ˈwenzdeɪ]", "chinese": "星期三", "重点": False},
        {"word": "Thursday", "phonetic": "[ˈθɜːzdeɪ]", "chinese": "星期四", "重点": False},
        {"word": "Friday", "phonetic": "[ˈfraɪdeɪ]", "chinese": "星期五", "重点": False},
    ],
    "句型": [
        {
            "english": "What's your favourite subject?",
            "chinese": "你最喜欢的学科是什么？",
            "重点": True
        },
        {
            "english": "My favourite subject is Maths.",
            "chinese": "我最喜欢的学科是数学。",
            "重点": True
        },
        {
            "english": "What do you have on Monday?",
            "chinese": "星期一你有什么课？",
            "重点": True
        },
        {
            "english": "I have Chinese, Maths and English.",
            "chinese": "我有语文、数学和英语课。",
            "重点": True
        },
        {
            "english": "Do you like Music?",
            "chinese": "你喜欢音乐课吗？",
            "重点": True
        },
        {
            "english": "Yes, I do. It's fun!",
            "chinese": "是的，喜欢。很有趣！",
            "重点": True
        },
        {
            "english": "How many subjects do you have?",
            "chinese": "你有多少门学科？",
            "重点": False
        },
        {
            "english": "I have six subjects.",
            "chinese": "我有六门学科。",
            "重点": False
        }
    ],
    "日常对话": [
        {
            "A": "Hello, Sam! How are you?",
            "A中文": "你好，Sam！你好吗？",
            "B": "I'm fine, thank you. And you?",
            "B中文": "我很好，谢谢。你呢？",
            "重点": True
        },
        {
            "A": "What's your favourite subject?",
            "A中文": "你最喜欢的学科是什么？",
            "B": "My favourite subject is English. I like reading.",
            "B中文": "我最喜欢的学科是英语。我喜欢阅读。",
            "重点": True
        },
        {
            "A": "What do you have today?",
            "A中文": "今天你有什么课？",
            "B": "I have Chinese, Maths and PE in the morning.",
            "B中文": "上午我有语文、数学和体育课。",
            "重点": True
        },
        {
            "A": "Are you good at Maths?",
            "A中文": "你擅长数学吗？",
            "B": "Yes, I am. I think Maths is interesting.",
            "B中文": "是的，我擅长。我觉得数学很有趣。",
            "重点": True
        }
    ]
}

def repeat_if_important(text, is_important):
    """重要内容重复3次"""
    if is_important:
        return f"{text}\n（重点！请重复三遍）\n{text}\n{text}\n{text}"
    return text

def generate_daily_reading():
    """生成今日朗读内容"""
    today = datetime.now().strftime("%Y年%m月%d日")
    day_of_week = datetime.now().strftime("%A")
    
    # 随机选择内容
    chinese_text = random.choice(CHINESE_CONTENT["课文"])
    char_list = random.sample(CHINESE_CONTENT["生字"], min(3, len(CHINESE_CONTENT["生字"])))
    word_list = random.sample(CHINESE_CONTENT["重点词语"], min(2, len(CHINESE_CONTENT["重点词语"])))
    
    eng_words = random.sample(ENGLISH_CONTENT["单词"], min(4, len(ENGLISH_CONTENT["单词"])))
    eng_sentences = random.sample(ENGLISH_CONTENT["句型"], min(3, len(ENGLISH_CONTENT["句型"])))
    eng_dialog = random.choice(ENGLISH_CONTENT["日常对话"])
    
    # 生成朗读文本
    reading_text = f"""📚 小学三年级下册 - {today} {day_of_week}

━━━━━━━━━━━━━━━━━━
📖 语文学习
━━━━━━━━━━━━━━━━━━

🌟 今日生字
"""
    
    for char in char_list:
        reading_text += f"\n{char['字']}（{char['拼音']}）- {char['意思']}"
        if char['重点']:
            reading_text += " 【重点】"
    
    reading_text += f"""

📝 今日重点词语
"""
    
    for word in word_list:
        reading_text += f"\n• {word['词']} - {word['意思']}"
        if word['重点']:
            reading_text += " 【重点！请重复三遍】"
    
    reading_text += f"""

📖 课文朗读
{chinese_text}

━━━━━━━━━━━━━━━━━━
🌍 英语学习
━━━━━━━━━━━━━━━━━━

🔤 今日单词
"""
    
    for word in eng_words:
        reading_text += f"\n• {word['word']} {word['phonetic']} - {word['chinese']}"
        if word['重点']:
            reading_text += " 【重点！】"
    
    reading_text += f"""

💬 今日句型
"""
    
    for sent in eng_sentences:
        reading_text += f"\n• {sent['english']} - {sent['chinese']}"
        if sent['重点']:
            reading_text += " 【重点！请重复三遍】"
    
    reading_text += f"""

🗣️ 日常对话
A: {eng_dialog['A']} ({eng_dialog['A中文']})
B: {eng_dialog['B']} ({eng_dialog['B中文']})
"""
    
    if eng_dialog['重点']:
        reading_text += "【重点对话！请练习三遍】"
    
    reading_text += f"""

━━━━━━━━━━━━━━━━━━
💪 学习小贴士
━━━━━━━━━━━━━━━━━━

1. 朗读时要声音洪亮，吐字清晰
2. 遇到重点内容，请慢速朗读并重复三遍
3. 英语单词要注意发音准确
4. 理解课文内容，不要死记硬背
5. 每天坚持，积少成多！

加油！今天也要认真读书哦！🎉
"""
    
    return reading_text

if __name__ == "__main__":
    content = generate_daily_reading()
    print(content)
    
    # 保存到文件
    with open("/root/.openclaw/workspace/daily_reading.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("\n✅ 朗读内容已保存到 daily_reading.txt")
