def extract_json(result: str) -> str:
    """
    从文本中提取 JSON 字符串（Python 原生兼容版）
    支持嵌套 JSON（对象包含数组），优先提取完整外层对象，保留 hotelList 等字段
    解决：unknown extension ?R 报错 + 嵌套JSON截断问题
    """
    import re
    import json

    # 空值判断
    if not result or not isinstance(result, str):
        return "{}"
    text = result.strip()

    # 策略1：本身就是合法JSON，直接返回
    try:
        json.loads(text)
        return text
    except:
        pass

    # ===================== 核心：Python 原生提取完整 JSON 对象/数组 =====================
    def extract_brackets(s, start_char, end_char):
        """栈方法提取最外层完整的 {} 或 []，支持嵌套，Python 通用"""
        stack = []
        start_idx = -1
        for idx, char in enumerate(s):
            if char == start_char:
                stack.append(char)
                if start_idx == -1:
                    start_idx = idx
            elif char == end_char and stack:
                stack.pop()
                if not stack:
                    return s[start_idx:idx+1].strip()
        return None

    # 策略2：优先提取完整 JSON 对象 { }（保留 hotelList，你的核心需求）
    obj_str = extract_brackets(text, '{', '}')
    if obj_str:
        try:
            json.loads(obj_str)
            return obj_str
        except:
            pass

    # 策略3：提取完整 JSON 数组 [ ]
    arr_str = extract_brackets(text, '[', ']')
    if arr_str:
        try:
            json.loads(arr_str)
            return arr_str
        except:
            pass

    # 兜底返回空对象
    return "{}"

if __name__ == '__main__':
    test_json = '{"weatherList":[{"cityName":"成都市","latitude":"","longitude":"","date":"2026-04-30","weather":"阴","temperature":"23℃","tips":"天气阴沉，气温适宜，建议携带薄外套，注意保湿补水，可安排户外游览活动"},{"cityName":"成都市","latitude":"","longitude":"","date":"2026-05-01","weather":"阴","temperature":"20℃","tips":"气温稍降，建议添加外套注意保暖，携带雨具以防小雨，室内活动为宜"}]}'
    print(extract_json(test_json))