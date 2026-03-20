#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中宫配置工具 - 配置其他 8 个宫位
Central Palace Configuration Tool
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/taiji-nine-palaces')

from taiji_client import TaijiClient, display_palaces, display_balance

def configure_all_palaces():
    """配置所有宫位到合理负载"""
    client = TaijiClient()
    
    # 九宫格标准配置（中宫指挥 8 宫）
    palace_configs = [
        # 数据采集层
        {"palace_id": 1, "load": 0.6, "desc": "数据采集 - 基础数据收集"},
        
        # 产品质量层
        {"palace_id": 2, "load": 0.7, "desc": "产品质量 - 需求与质量把控"},
        
        # 技术团队层
        {"palace_id": 3, "load": 0.8, "desc": "技术团队 - 核心开发力量"},
        
        # 品牌战略层
        {"palace_id": 4, "load": 0.7, "desc": "品牌战略 - 市场定位与规划"},
        
        # 中央控制（中宫）- 保持当前
        {"palace_id": 5, "load": 0.75, "desc": "中央控制 - 中宫枢纽"},
        
        # 物联监控层
        {"palace_id": 6, "load": 0.6, "desc": "物联监控 - 设备监控与告警"},
        
        # 法务框架层
        {"palace_id": 7, "load": 0.5, "desc": "法务框架 - 合规与风控"},
        
        # 营销客服层
        {"palace_id": 8, "load": 0.6, "desc": "营销客服 - 客户与销售"},
        
        # 行业生态层
        {"palace_id": 9, "load": 0.5, "desc": "行业生态 - 外部合作与生态"},
    ]
    
    print("=== 中宫配置其他 8 宫 ===\n")
    
    # 批量更新
    palaces_data = [{"palace_id": p["palace_id"], "load": p["load"]} for p in palace_configs]
    result = client.batch_update_palaces(palaces_data)
    
    if result.get("success"):
        print("✅ 批量配置成功！\n")
    else:
        print(f"❌ 配置失败：{result.get('error')}\n")
    
    # 显示配置结果
    palaces = client.get_all_palaces()
    print(display_palaces(palaces))
    print()
    
    # 显示平衡状态
    balance = client.get_balance_status()
    print(display_balance({"balance": balance}))
    
    # 显示配置详情
    print("\n=== 配置详情 ===")
    for config in palace_configs:
        status = "✅" if config["load"] > 0 else "⏸️"
        print(f"{status} {config['desc']}: {config['load']*100:.0f}%")
    
    return result


def quick_balance():
    """快速平衡 - 自动调整失衡的宫位"""
    client = TaijiClient()
    
    print("=== 快速平衡检查 ===\n")
    
    # 获取当前平衡状态
    balance_data = client.get_balance_status()
    imbalanced = []
    
    for pair, value in balance_data.get("balance", {}).items():
        if value < 0.7:
            imbalanced.append((pair, value))
    
    if not imbalanced:
        print("✅ 所有阴阳对都处于平衡状态！")
        return
    
    print(f"⚠️ 发现 {len(imbalanced)} 个失衡的阴阳对：\n")
    
    for pair, value in imbalanced:
        print(f"  - {pair}: {value:.2f} (需要调整)")
    
    # 自动调整建议
    print("\n=== 调整建议 ===")
    print("运行以下命令手动调整，或调用 auto_balance() 自动调整")
    
    for pair, value in imbalanced:
        if pair == "team_process":
            print(f"  ./taiji.sh load 4 0.7  # 调整 4-品牌战略")
        elif pair == "tech_quality":
            print(f"  ./taiji.sh load 3 0.7  # 调整 3-技术团队")
            print(f"  ./taiji.sh load 6 0.7  # 调整 6-物联监控")
        elif pair == "product_data":
            print(f"  ./taiji.sh load 2 0.7  # 调整 2-产品质量")
            print(f"  ./taiji.sh load 1 0.7  # 调整 1-数据采集")
        elif pair == "monitor_eco":
            print(f"  ./taiji.sh load 7 0.7  # 调整 7-法务框架")
            print(f"  ./taiji.sh load 9 0.7  # 调整 9-行业生态")


def auto_balance():
    """自动平衡 - 调用 API 自动调整"""
    client = TaijiClient()
    
    print("=== 自动平衡调整 ===\n")
    
    result = client.adjust_balance()
    print(f"调整结果：{result}")
    
    # 显示调整后状态
    balance = client.get_balance_status()
    print(display_balance({"balance": balance}))


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "configure":
            configure_all_palaces()
        elif command == "balance":
            quick_balance()
        elif command == "auto":
            auto_balance()
        else:
            print("用法：python configure_palaces.py [configure|balance|auto]")
    else:
        # 默认执行配置
        configure_all_palaces()
