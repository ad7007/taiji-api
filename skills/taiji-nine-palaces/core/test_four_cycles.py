#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""四循环系统测试脚本"""

from nine_palaces_cycles import NinePalacesCycles
from palace_constants import get_palace_name, get_palace_element, get_all_palaces


def test_basic():
    print("=" * 70)
    print("【测试 1: 基础配置】")
    print("=" * 70)
    
    print(f"\n相生循环：{NinePalacesCycles.GENERATION_CYCLE}")
    print(f"相克循环：{NinePalacesCycles.RESTRAINT_CYCLE}")
    print(f"159 中轴：{NinePalacesCycles.CENTRAL_AXIS}")
    print(f"258 三角：{NinePalacesCycles.TRIANGLE_SUPPORT}")
    print(f"绝对核心：{NinePalacesCycles.CORE_PALACE}宫")
    
    assert NinePalacesCycles.is_core_palace(5)
    assert NinePalacesCycles.is_dual_cycle_palace(5)
    print("\n✅ 5 号宫的双重身份验证通过")


def test_roles():
    print("\n" + "=" * 70)
    print("【测试 2: 宫位角色】")
    print("=" * 70)
    
    palaces = get_all_palaces()
    
    print(f"\n{'宫位':<12} {'名称':<15} {'五行':<4} {'角色':<20}")
    print("-" * 55)
    
    for palace in palaces:
        pos = palace['position']
        name = palace['name']
        element = palace['element']
        role = NinePalacesCycles.get_cycle_role(pos)
        
        print(f"{pos:<12} {name:<15} {element:<4} {role:<20}")


def test_integrity():
    print("\n" + "=" * 70)
    print("【测试 3: 循环完整性】")
    print("=" * 70)
    
    gen_path = NinePalacesCycles.get_generation_path()
    print(f"\n相生循环路径：{gen_path}")
    
    print("\n相生关系验证:")
    for i in range(len(gen_path)):
        current_pos = gen_path[i]
        next_pos = gen_path[(i + 1) % len(gen_path)]
        
        current_elem = get_palace_element(current_pos)
        next_elem = get_palace_element(next_pos)
        
        expected = NinePalacesCycles.GENERATION_CYCLE[current_elem]
        
        status = "✓" if expected == next_elem else "✗"
        print(f"  {status} {get_palace_name(current_pos)}({current_elem}) → {get_palace_name(next_pos)}({next_elem})")
    
    restraint_pairs = NinePalacesCycles.get_restraint_pairs()
    print(f"\n相克配对：{len(restraint_pairs)} 对")
    print("\n相克关系:")
    for r, e in restraint_pairs[:5]:
        print(f"  {get_palace_name(r)} ╳ {get_palace_name(e)}")
    
    print("\n159 中轴:")
    for pos in NinePalacesCycles.get_central_axis_path():
        elem = get_palace_element(pos)
        role = NinePalacesCycles.get_cycle_role(pos)
        print(f"  {get_palace_name(pos)} - {elem} - {role}")
    
    print("\n258 三角:")
    for pos in NinePalacesCycles.get_triangle_support_path():
        elem = get_palace_element(pos)
        role = NinePalacesCycles.get_cycle_role(pos)
        print(f"  {get_palace_name(pos)} - {elem} - {role}")


def test_visualization():
    print("\n" + "=" * 70)
    print("【测试 4: 可视化】")
    print("=" * 70)
    print(NinePalacesCycles.visualize_four_cycles())


def test_statistics():
    print("\n" + "=" * 70)
    print("【测试 5: 统计】")
    print("=" * 70)
    
    stats = NinePalacesCycles.get_statistics()
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("      九宫格四循环系统 - 完整测试")
    print("=" * 70)
    
    try:
        test_basic()
        test_roles()
        test_integrity()
        test_visualization()
        test_statistics()
        
        print("\n" + "=" * 70)
        print("✅ 所有测试通过！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
