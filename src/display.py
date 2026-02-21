#!/usr/bin/env python3
"""
早霞晚霞预测系统 - 前端展示模块
"""

from .predictor import SunriseGlowPredictor

# 默认地点
LOCATIONS = {
    "oakville": {
        "name": "Oakville",
        "latitude": 43.45,
        "longitude": -79.68,
        "timezone": "America/Toronto"
    },
    "beijing": {
        "name": "北京",
        "latitude": 39.90,
        "longitude": 116.40,
        "timezone": "Asia/Shanghai"
    },
    "shanghai": {
        "name": "上海",
        "latitude": 31.23,
        "longitude": 121.47,
        "timezone": "Asia/Shanghai"
    }
}


def predict_location(location_name: str, date: str = None) -> str:
    """
    预测指定地点的霞光
    
    Args:
        location_name: 地点名称（支持 oakville, beijing, shanghai 或城市名）
        date: 日期 (YYYY-MM-DD)
        
    Returns:
        str: 人类可读的预测结果
    """
    predictor = SunriseGlowPredictor()
    
    # 查找地点
    location_key = location_name.lower()
    if location_key in LOCATIONS:
        location = LOCATIONS[location_key]
    else:
        # 尝试使用坐标
        location = {
            "name": location_name,
            "latitude": 43.45,  # 默认
            "longitude": -79.68,
            "timezone": "America/Toronto"
        }
    
    result = predictor.predict(location, date)
    return predictor.to_human_readable(result)


def predict_multiple(locations: list, date: str = None) -> str:
    """
    预测多个地点
    
    Args:
        locations: 地点名称列表
        date: 日期
        
    Returns:
        str: 多地点对比结果
    """
    predictor = SunriseGlowPredictor()
    
    results = []
    for loc_name in locations:
        location_key = loc_name.lower()
        if location_key in LOCATIONS:
            location = LOCATIONS[location_key]
        else:
            location = {
                "name": loc_name,
                "latitude": 43.45,
                "longitude": -79.68,
                "timezone": "America/Toronto"
            }
        
        result = predictor.predict(location, date)
        results.append(result)
    
    # 构建对比输出
    lines = ["=" * 55]
    
    for r in results:
        lines.extend([
            f"📍 {r['location']} - {r['date']}",
            f"🌅 早霞：{r['sunrise_glow']['score']}/10 {r['sunrise_glow']['stars']} {r['sunrise_glow']['color']}",
            f"🌄 晚霞：{r['sunset_glow']['score']}/10 {r['sunset_glow']['stars']} {r['sunset_glow']['color']}",
            ""
        ])
    
    lines.append("=" * 55)
    
    return "\n".join(lines)


def main():
    """测试"""
    print(predict_location("oakville", "2026-02-20"))
    print("")
    print(predict_multiple(["oakville", "beijing"], "2026-02-20"))


if __name__ == "__main__":
    main()
