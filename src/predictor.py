#!/usr/bin/env python3
"""
早霞晚霞预测系统 - 核心预测模块
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# API 配置
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
SUNRISE_SUNSET_URL = "https://api.sunrise-sunset.org/json"


class SunriseGlowPredictor:
    """早霞晚霞预测器"""
    
    def __init__(self):
        self.cache = {}
    
    def get_weather_data(self, lat: float, lng: float, timezone: str = "America/New_York") -> dict:
        """获取天气数据"""
        params = {
            "latitude": lat,
            "longitude": lng,
            "hourly": ",".join([
                "cloudcover_1000hPa",    # 低云
                "cloudcover_850hPa",     # 中云
                "cloudcover_500hPa",    # 高云
                "relative_humidity_2m", # 湿度
                "surface_pressure",      # 气压
                "wind_speed_10m",       # 风速
                "temperature_2m"         # 温度
            ]),
            "timezone": timezone,
            "forecast_days": 2
        }
        
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_sun_times(self, lat: float, lng: float, date: str) -> dict:
        """获取日出日落时间"""
        params = {
            "lat": lat,
            "lng": lng,
            "date": date
        }
        
        response = requests.get(SUNRISE_SUNSET_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def calculate_glow_score(
        self,
        cloud_low: float,
        cloud_mid: float,
        cloud_high: float,
        humidity: float,
        pressure: float
    ) -> dict:
        """
        计算霞光评分（基于专业摄影师经验）
        
        评分标准：
        - 高云（6000m+）反射最佳 → 加分
        - 中云（2000-6000m）散射 → 加分
        - 低云（0-2000m）遮挡 → 扣分
        """
        
        # 云层评分 (60%)
        high_bonus = min(cloud_high * 0.08, 4)  # 高云加分
        mid_bonus = min(cloud_mid * 0.06, 3)   # 中云加分
        low_penalty = min(cloud_low * 0.05, 3)  # 低云扣分
        cloud_score = high_bonus + mid_bonus - low_penalty
        
        # 湿度评分 (15%)
        if 60 <= humidity <= 80:
            hum_score = 2
        elif 40 <= humidity:
            hum_score = 1
        else:
            hum_score = 0.5
        
        # 气压评分 (15%)
        if 1010 <= pressure <= 1020:
            press_score = 1.5
        else:
            press_score = 0.5
        
        # 综合评分
        total = cloud_score * 0.6 + hum_score * 0.15 + press_score * 0.15
        score = round(min(max(total * 1.2, 1), 10), 1)
        
        # 颜色映射
        if score >= 8:
            color = "紫红色"
            stars = "⭐⭐⭐⭐⭐"
        elif score >= 6:
            color = "金红色"
            stars = "⭐⭐⭐⭐"
        elif score >= 4:
            color = "橙红色"
            stars = "⭐⭐⭐"
        elif score >= 2:
            color = "灰白色"
            stars = "⭐⭐"
        else:
            color = "几乎无霞光"
            stars = "⭐"
        
        # 生成原因
        reasons = []
        if cloud_high > 30:
            reasons.append(f"高云 {cloud_high:.0f}%")
        if cloud_mid > 30:
            reasons.append(f"中云 {cloud_mid:.0f}%")
        if cloud_low > 30:
            reasons.append(f"低云 {cloud_low:.0f}%")
        if cloud_low < 15:
            reasons.append("低云少")
        if 60 <= humidity <= 80:
            reasons.append("湿度适中")
        
        return {
            "score": score,
            "color": color,
            "stars": stars,
            "reason": "，".join(reasons) if reasons else "条件一般"
        }
    
    def predict(self, location: dict, date: str = None) -> dict:
        """
        预测指定地点的霞光
        
        Args:
            location: dict with keys: name, latitude, longitude, timezone
            date: 日期 (YYYY-MM-DD)，默认明天
            
        Returns:
            dict: 预测结果
        """
        if date is None:
            date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        lat = location["latitude"]
        lng = location["longitude"]
        tz = location.get("timezone", "America/New_York")
        
        # 获取天气数据
        weather = self.get_weather_data(lat, lng, tz)
        
        # 获取日出日落
        sun_times = self.get_sun_times(lat, lng, date)
        
        # 简化：取预测期间的平均值
        hourly = weather.get("hourly", {})
        
        # 早间 (6-9点) 平均
        morning_data = {
            "cloud_low": sum(hourly.get("cloudcover_1000hPa", [0])[6:10]) / 4,
            "cloud_mid": sum(hourly.get("cloudcover_850hPa", [0])[6:10]) / 4,
            "cloud_high": sum(hourly.get("cloudcover_500hPa", [0])[6:10]) / 4,
            "humidity": sum(hourly.get("relative_humidity_2m", [0])[6:10]) / 4,
            "pressure": sum(hourly.get("surface_pressure", [0])[6:10]) / 4,
        }
        
        # 晚间 (17-20点) 平均
        evening_data = {
            "cloud_low": sum(hourly.get("cloudcover_1000hPa", [0])[17:21]) / 4,
            "cloud_mid": sum(hourly.get("cloudcover_850hPa", [0])[17:21]) / 4,
            "cloud_high": sum(hourly.get("cloudcover_500hPa", [0])[17:21]) / 4,
            "humidity": sum(hourly.get("relative_humidity_2m", [0])[17:21]) / 4,
            "pressure": sum(hourly.get("surface_pressure", [0])[17:21]) / 4,
        }
        
        # 计算评分
        sunrise_pred = self.calculate_glow_score(
            morning_data["cloud_low"],
            morning_data["cloud_mid"],
            morning_data["cloud_high"],
            morning_data["humidity"],
            morning_data["pressure"]
        )
        
        sunset_pred = self.calculate_glow_score(
            evening_data["cloud_low"],
            evening_data["cloud_mid"],
            evening_data["cloud_high"],
            evening_data["humidity"],
            evening_data["pressure"]
        )
        
        # 构建结果
        result = {
            "location": location["name"],
            "latitude": lat,
            "longitude": lng,
            "date": date,
            "sun_times": {
                "sunrise": sun_times["results"]["sunrise"],
                "sunset": sun_times["results"]["sunset"]
            },
            "morning_weather": {
                "cloud_low": round(morning_data["cloud_low"], 1),
                "cloud_mid": round(morning_data["cloud_mid"], 1),
                "cloud_high": round(morning_data["cloud_high"], 1),
                "humidity": round(morning_data["humidity"], 1),
                "pressure": round(morning_data["pressure"], 1)
            },
            "evening_weather": {
                "cloud_low": round(evening_data["cloud_low"], 1),
                "cloud_mid": round(evening_data["cloud_mid"], 1),
                "cloud_high": round(evening_data["cloud_high"], 1),
                "humidity": round(evening_data["humidity"], 1),
                "pressure": round(evening_data["pressure"], 1)
            },
            "sunrise_glow": sunrise_pred,
            "sunset_glow": sunset_pred,
            "generated_at": datetime.now().isoformat()
        }
        
        return result
    
    def to_human_readable(self, result: dict) -> str:
        """转换为人类可读格式"""
        lines = [
            "=" * 55,
            f"📍 {result['location']} - {result['date']}",
            "=" * 55,
            "",
            f"🌅 日出：{result['sun_times']['sunrise']}",
            f"🌄 日落：{result['sun_times']['sunset']}",
            "",
            "─" * 55,
            "🌤️ 早间天气",
            f"低云 {result['morning_weather']['cloud_low']}% | 高云 {result['morning_weather']['cloud_high']}% | 湿度 {result['morning_weather']['humidity']}%",
            "",
            f"🌅 早霞预测：{result['sunrise_glow']['score']}/10 {result['sunrise_glow']['stars']}",
            f"颜色：{result['sunrise_glow']['color']}",
            f"原因：{result['sunrise_glow']['reason']}",
            "",
            "─" * 55,
            "🌤️ 晚间天气",
            f"低云 {result['evening_weather']['cloud_low']}% | 高云 {result['evening_weather']['cloud_high']}% | 湿度 {result['evening_weather']['humidity']}%",
            "",
            f"🌄 晚霞预测：{result['sunset_glow']['score']}/10 {result['sunset_glow']['stars']}",
            f"颜色：{result['sunset_glow']['color']}",
            f"原因：{result['sunset_glow']['reason']}",
            "=" * 55,
        ]
        
        return "\n".join(lines)


def main():
    """测试预测"""
    predictor = SunriseGlowPredictor()
    
    # 测试 Oakville
    oakville = {
        "name": "Oakville",
        "latitude": 43.45,
        "longitude": -79.68,
        "timezone": "America/Toronto"
    }
    
    result = predictor.predict(oakville, "2026-02-20")
    print(predictor.to_human_readable(result))


if __name__ == "__main__":
    main()
