from typing import Dict, List, Any


class PalaceConfig:
    """
    宫位配置类
    管理九宫格的配置信息
    """
    
    def __init__(self):
        """
        初始化宫位配置
        """
        self.palaces = self._initialize_palaces()
    
    def _initialize_palaces(self) -> Dict[int, Dict[str, Any]]:
        """
        初始化宫位配置
        
        Returns:
            宫位配置字典
        """
        return {
            1: {
                "name": "数据采集",
                "element": "水",
                "description": "负责数据收集和处理",
                "priority": 3
            },
            2: {
                "name": "产品质量",
                "element": "木",
                "description": "负责产品质量控制和管理",
                "priority": 2
            },
            3: {
                "name": "技术团队",
                "element": "火",
                "description": "负责技术开发和创新",
                "priority": 1
            },
            4: {
                "name": "品牌战略",
                "element": "土",
                "description": "负责品牌建设和战略规划",
                "priority": 4
            },
            5: {
                "name": "中央控制",
                "element": "金",
                "description": "负责系统整体协调和控制",
                "priority": 0
            },
            6: {
                "name": "物联监控",
                "element": "水",
                "description": "负责物联网设备监控和管理",
                "priority": 5
            },
            7: {
                "name": "法务框架",
                "element": "木",
                "description": "负责法律事务和框架建设",
                "priority": 6
            },
            8: {
                "name": "市场营销",
                "element": "火",
                "description": "负责市场营销和推广",
                "priority": 7
            },
            9: {
                "name": "行业生态",
                "element": "土",
                "description": "负责行业生态建设和合作",
                "priority": 8
            }
        }
    
    def get_palace(self, palace_id: int) -> Dict[str, Any]:
        """
        获取宫位配置
        
        Args:
            palace_id: 宫位ID
        
        Returns:
            宫位配置
        """
        return self.palaces.get(palace_id, {})
    
    def get_all_palaces(self) -> Dict[int, Dict[str, Any]]:
        """
        获取所有宫位配置
        
        Returns:
            所有宫位配置
        """
        return self.palaces.copy()
    
    def get_palace_name(self, palace_id: int) -> str:
        """
        获取宫位名称
        
        Args:
            palace_id: 宫位ID
        
        Returns:
            宫位名称
        """
        palace = self.get_palace(palace_id)
        return palace.get("name", f"宫位{palace_id}")
    
    def get_palace_element(self, palace_id: int) -> str:
        """
        获取宫位元素
        
        Args:
            palace_id: 宫位ID
        
        Returns:
            宫位元素
        """
        palace = self.get_palace(palace_id)
        return palace.get("element", "")
    
    def get_priority_order(self) -> List[int]:
        """
        获取宫位优先级排序
        
        Returns:
            宫位ID列表，按优先级排序
        """
        return sorted(self.palaces.keys(), key=lambda x: self.palaces[x].get("priority", 999))


# 全局宫位配置实例
palace_config = PalaceConfig()
