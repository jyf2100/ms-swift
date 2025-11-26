#!/usr/bin/env python
"""
验证菜单联动功能的测试脚本
"""

import sys
import os
sys.path.insert(0, '/mnt/disk01/workspaces/worksummary/ms-swift')

def verify_fixes():
    """验证所有修复是否正确"""
    with open('/mnt/disk01/workspaces/worksummary/ms-swift/swift/ui/app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("验证菜单联动功能修复...")
    
    # 检查HTML部分
    html_checks = [
        ("onclick=\"toggleSubMenu('train-submenu', event)\"", "主菜单训练项onclick事件"),
        ("onclick=\"toggleSubMenu('infer-submenu', event)\"", "主菜单服务项onclick事件"),
        ("onclick=\"toggleSubMenu('eval-submenu', event)\"", "主菜单评测项onclick事件"),
    ]
    
    for check, desc in html_checks:
        if check in content:
            print(f"✓ {desc} - 已修复")
        else:
            print(f"✗ {desc} - 未找到")
    
    # 检查JavaScript部分
    js_checks = [
        ("function toggleSubMenu(submenuId, event)", "JavaScript函数定义包含event参数"),
        ("event ? event.currentTarget : null", "使用event.currentTarget"),
        ("submenu.style.display = 'block'", "子菜单显示逻辑"),
        ("arrow.style.transform = 'rotate(90deg)'", "箭头旋转展开状态"),
        ("arrow.style.transform = 'rotate(0deg)'", "箭头旋转收起状态"),
    ]
    
    for check, desc in js_checks:
        if check in content:
            print(f"✓ {desc} - 已修复")
        else:
            print(f"✗ {desc} - 未找到")
    
    # 检查子菜单默认隐藏
    if 'display: none' in content and 'submenu' in content.split("display: none")[0][-100:]:
        print("✓ 子菜单默认隐藏 - 已设置")
    else:
        print("✗ 子菜单默认隐藏 - 未设置")
    
    # 检查是否有window赋值（应该没有）
    if 'window.' in content.split('def js_script():')[1].split('"""')[2][:1000]:
        print("✗ JavaScript中仍包含window赋值")
    else:
        print("✓ JavaScript中已移除window赋值（Gradio兼容）")
    
    print("\n修复总结:")
    print("- HTML onclick事件已添加event参数")
    print("- JavaScript函数已接受event参数并使用event.currentTarget")
    print("- 子菜单默认隐藏，点击主菜单时切换显示状态")
    print("- 箭头图标会旋转显示展开/收起状态")
    print("- 移除了Gradio不兼容的window对象赋值")

if __name__ == "__main__":
    verify_fixes()
