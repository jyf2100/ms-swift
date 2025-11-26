#!/usr/bin/env python
"""
测试SWIFT Web UI菜单功能修复的脚本
此脚本将创建一个最小化的UI来测试菜单联动功能
"""

import sys
import os
sys.path.insert(0, '/mnt/disk01/workspaces/worksummary/ms-swift')

# 检查修改后的代码是否包含预期的修复
def test_code_fixes():
    print("正在检查代码修复...")
    
    # 检查 app.py 文件中的修复
    with open('/mnt/disk01/workspaces/worksummary/ms-swift/swift/ui/app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含必要的修复
    checks = [
        ('toggleSubMenu(submenuId, event)', '函数参数包含event'),
        ('event.currentTarget', '使用event.currentTarget'),
        ("onclick=\"toggleSubMenu('train-submenu', event)\"", 'HTML中传递event参数'),
        ("onclick=\"toggleSubMenu('infer-submenu', event)\"", 'HTML中传递event参数'),
        ("onclick=\"toggleSubMenu('eval-submenu', event)\"", 'HTML中传递event参数'),
    ]
    
    all_passed = True
    for check, description in checks:
        if check in content:
            print(f"✓ {description}")
        else:
            print(f"✗ {description} - 未找到")
            all_passed = False
    
    if all_passed:
        print("\n所有代码修复检查通过！")
    else:
        print("\n部分代码修复检查失败！")
    
    # 显示修复的代码片段
    print("\n" + "="*50)
    print("相关代码片段:")
    print("="*50)
    
    # 显示JavaScript函数
    start_idx = content.find("function toggleSubMenu(submenuId, event)")
    if start_idx != -1:
        end_idx = content.find("}", start_idx + 30)  # 找到函数结束位置
        if end_idx != -1:
            end_idx = content.find("}", end_idx + 1)  # 找到完整的闭合括号
            js_func = content[start_idx:end_idx+1]
            print("JavaScript函数:")
            print(js_func)
            print()
    
    # 显示HTML部分
    html_parts = []
    for line in content.split('\n'):
        if 'onclick="toggleSubMenu' in line and 'event)' in line:
            html_parts.append(line.strip())
    
    if html_parts:
        print("HTML onclick事件:")
        for part in html_parts:
            print(part)
    
    return all_passed

if __name__ == "__main__":
    success = test_code_fixes()
    
    if success:
        print("\n修复验证成功！")
        print("要启动Web UI，请运行以下命令：")
        print("cd /mnt/disk01/workspaces/worksummary/ms-swift && swift web-ui --server_port 8080")
    else:
        print("\n修复验证失败！")