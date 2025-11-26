#!/bin/bash
# SWIFT Web UI 启动脚本 - 修复菜单联动版本

echo "==========================================="
echo "SWIFT Web UI 启动脚本"
echo "菜单联动功能已修复"
echo "==========================================="

# 切换到项目目录
cd /mnt/disk01/workspaces/worksummary/ms-swift

echo "检查修复状态..."
if grep -q "toggleSubMenu('train-submenu', event)" swift/ui/app.py; then
    echo "✓ HTML onclick事件修复已应用"
else
    echo "✗ HTML onclick事件修复未找到"
fi

if grep -q "function toggleSubMenu(submenuId, event)" swift/ui/app.py; then
    echo "✓ JavaScript函数修复已应用"
else
    echo "✗ JavaScript函数修复未找到"
fi

if grep -q "display: none" swift/ui/app.py; then
    echo "✓ 子菜单默认隐藏已设置"
else
    echo "✗ 子菜单默认隐藏未设置"
fi

echo ""
echo "启动SWIFT Web UI服务..."
echo "访问地址: http://<服务器IP>:7860"
echo ""
echo "菜单功能说明:"
echo "- 主菜单项（模型训练/模型服务/评测与演示）默认不展开"
echo "- 点击主菜单项会展开/收起对应的子菜单"
echo "- 箭头图标会旋转显示展开/收起状态"
echo "- 子菜单项可切换到对应功能标签页"
echo ""
echo "启动命令: swift web-ui --server_port 7860 --server_name 0.0.0.0 --lang zh"

# 启动服务
swift web-ui --server_port 7860 --server_name 0.0.0.0 --lang zh