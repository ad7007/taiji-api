#!/usr/bin/env python3
"""
2 宫 - 物联产品核心

职责：
1. 产品管理
2. 功能实现
3. 质量控制
4. 用户反馈
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Product:
    product_id: str
    name: str
    version: str
    status: str
    features: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class Palace2Product:
    """2 宫 - 物联产品"""
    
    def __init__(self):
        self.palace_id = 2
        self.palace_name = "物联产品"
        self.products: Dict[str, Product] = {}
    
    def create_product(self, name: str, version: str = "1.0.0") -> Product:
        """创建产品"""
        product_id = f"prod_{name.lower().replace(' ', '_')}"
        product = Product(
            product_id=product_id,
            name=name,
            version=version,
            status="planning"
        )
        self.products[product_id] = product
        return product
    
    def add_feature(self, product_id: str, feature: str) -> bool:
        """添加功能"""
        product = self.products.get(product_id)
        if product:
            product.features.append(feature)
            return True
        return False
    
    def list_products(self) -> List[Product]:
        return list(self.products.values())
    
    def get_stats(self) -> Dict:
        return {"total": len(self.products)}


# 全局实例
_instance = None

def get_product() -> Palace2Product:
    global _instance
    if _instance is None:
        _instance = Palace2Product()
    return _instance


if __name__ == "__main__":
    p = Palace2Product()
    p.create_product("太极系统", "2.0.0")
    print(f"产品数: {p.get_stats()['total']}")