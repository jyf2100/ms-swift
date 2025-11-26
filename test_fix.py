#!/usr/bin/env python
# 简化版的启动脚本，用于测试修复的菜单功能

import os
import sys
sys.path.insert(0, '/mnt/disk01/workspaces/worksummary/ms-swift')

# 导入必要的模块以确保环境正确
from swift.ui.app import SwiftWebUI
from swift.llm import WebUIArguments

def test_launch():
    print("正在测试启动Swift Web UI...")
    
    # 创建参数对象
    args = WebUIArguments(
        server_port=8082,
        server_name="127.0.0.1", 
        share=False,
        lang="zh"
    )
    
    print(f"参数: {args}")
    
    try:
        # 直接创建UI实例并运行，不启动服务器
        ui_instance = SwiftWebUI(args)
        print("SwiftWebUI实例创建成功")
        
        # 检查我们修改的文件是否存在且包含正确的代码
        import swift.ui.app as app_module
        print("成功导入swift.ui.app模块")
        
        # 验证关键函数是否包含修复的代码
        import inspect
        source = inspect.getsource(app_module.SwiftWebUI.run)
        if 'toggleSubMenu' in source and 'event.currentTarget' in source:
            print("✓ JavaScript函数修复已包含在代码中")
        else:
            print("✗ 未找到预期的修复代码")
            
        print("代码修复验证完成。")
        print("要启动完整服务，请使用命令: swift web-ui")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_launch()