"""
太极关系图 (Taiji Relationship)

定义九宫格之间的关系：
- 汇报关系
- 调度关系
- 协作关系
- 五行相生
- 五行相克
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set


class Element(Enum):
    """五行"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


class RelationType(Enum):
    """关系类型"""
    REPORTS_TO = "汇报"
    DISPATCHES = "调度"
    COLLABORATES = "协作"
    GENERATES = "相生"
    CONTROLS = "相克"


@dataclass
class Palace:
    """宫位定义"""
    palace_id: int
    name: str
    element: Element
    role: str
    default_permission: int
    reports_to: int = 5
    generates: List[int] = None
    controlled_by: List[int] = None
    
    def __post_init__(self):
        if self.generates is None:
            self.generates = []
        if self.controlled_by is None:
            self.controlled_by = []


# 九宫定义
PALACES: Dict[int, Palace] = {
    1: Palace(1, "数据采集宫", Element.EARTH, "worker", 3, 5, [7], [3]),
    2: Palace(2, "产品质量宫", Element.METAL, "worker", 2, 5, [], []),
    3: Palace(3, "技术团队宫", Element.WOOD, "worker", 2, 5, [6], [7]),
    4: Palace(4, "品牌战略宫", Element.WATER, "worker", 2, 5, [3], [1]),
    5: Palace(5, "中央控制宫", Element.EARTH, "commander", 3, 0, [], []),
    6: Palace(6, "物联监控宫", Element.FIRE, "worker", 4, 5, [1], []),
    7: Palace(7, "法务框架宫", Element.METAL, "validator", 1, 5, [4], [6]),
    8: Palace(8, "营销客服宫", Element.WOOD, "worker", 2, 5, [], []),
    9: Palace(9, "行业生态宫", Element.EARTH, "worker", 3, 5, [], []),
}

# Scene 协作关系
SCENE_COLLABORATION: Dict[str, List[int]] = {
    "scene:download": [1, 7],
    "scene:scrape": [1, 3, 7],
    "scene:transcribe": [1, 3, 7],
    "scene:quality_check": [1, 2, 7],
    "scene:code": [3, 7],
    "scene:debug": [3, 7],
    "scene:brand_position": [1, 4, 7],
    "scene:competitive": [1, 4, 7],
    "scene:monitor": [6, 9],
    "scene:backup": [6, 7],
    "scene:content_create": [4, 8, 7],
    "scene:research": [1, 9, 7],
}


class RelationshipGraph:
    """太极关系图查询"""
    
    def __init__(self):
        self.palaces = PALACES
        self.scenes = SCENE_COLLABORATION
    
    def get_palace(self, palace_id: int) -> Optional[Palace]:
        return self.palaces.get(palace_id)
    
    def get_all_palaces(self) -> Dict[int, Palace]:
        return self.palaces
    
    def get_reports_to(self, palace_id: int) -> int:
        palace = self.palaces.get(palace_id)
        return palace.reports_to if palace else 5
    
    def get_reports_from(self, palace_id: int) -> List[int]:
        return [p for p, palace in self.palaces.items() 
                if palace.reports_to == palace_id]
    
    def get_collaborators(self, scene: str) -> List[int]:
        return self.scenes.get(scene, [5])
    
    def get_palace_scenes(self, palace_id: int) -> List[str]:
        return [scene for scene, palaces in self.scenes.items()
                if palace_id in palaces]
    
    def get_collaboration_partners(self, palace_id: int) -> Set[int]:
        partners = set()
        for palaces in self.scenes.values():
            if palace_id in palaces:
                partners.update(palaces)
        partners.discard(palace_id)
        return partners
    
    def get_generators(self, palace_id: int) -> List[int]:
        palace = self.palaces.get(palace_id)
        return palace.generates if palace else []
    
    def get_generated_by(self, palace_id: int) -> List[int]:
        return [p for p, palace in self.palaces.items()
                if palace_id in palace.generates]
    
    def get_controllers(self, palace_id: int) -> List[int]:
        palace = self.palaces.get(palace_id)
        return palace.controlled_by if palace else []
    
    def get_controlled_by(self, palace_id: int) -> List[int]:
        return [p for p, palace in self.palaces.items()
                if palace_id in palace.controlled_by]
    
    def get_all_relations(self, palace_id: int) -> Dict[str, List[int]]:
        return {
            "reports_to": [self.get_reports_to(palace_id)],
            "reports_from": self.get_reports_from(palace_id),
            "generates": self.get_generators(palace_id),
            "generated_by": self.get_generated_by(palace_id),
            "controlled_by": self.get_controlled_by(palace_id),
            "controllers": self.get_controllers(palace_id),
            "collaborators": list(self.get_collaboration_partners(palace_id))
        }
    
    def visualize(self) -> str:
        return """
┌─────────┬─────────┬─────────┐
│ 4-品牌   │ 9-行业   │ 2-产品   │
│ (水)    │ (土)    │ (金)    │
├─────────┼─────────┼─────────┤
│ 3-技术   │ 5-米珞   │ 7-法务   │
│ (木)    │ (土)    │ (金)    │
├─────────┼─────────┼─────────┤
│ 8-营销   │ 1-采集   │ 6-监控   │
│ (木)    │ (土)    │ (火)    │
└─────────┴─────────┴─────────┘

五行相生: 木→火→土→金→水→木
五行相克: 木→土→水→火→金→木
"""


# 使用示例
if __name__ == "__main__":
    graph = RelationshipGraph()
    print(graph.visualize())
    
    print("\n1宫关系:")
    print(f"  汇报给: {graph.get_reports_to(1)}宫")
    print(f"  相生: {graph.get_generators(1)}")
    print(f"  被谁克: {graph.get_controlled_by(1)}")
    print(f"  协作伙伴: {graph.get_collaboration_partners(1)}")
    
    print("\n场景协作:")
    print(f"  视频转录: {graph.get_collaborators('scene:transcribe')}")