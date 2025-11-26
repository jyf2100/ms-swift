#!/bin/bash
# SWIFT Web UI 启动脚本

# 切换到项目目录
cd /mnt/disk01/workspaces/worksummary/ms-swift

# 启动SWIFT Web UI服务
echo "正在启动SWIFT Web UI服务..."
echo "修复的菜单联动功能已应用"

# 使用可用的命令启动服务
if command -v swift &> /dev/null; then
    swift web-ui --server_port 8080 --server_name 0.0.0.0 --lang zh
else
    echo "swift命令不可用，尝试直接运行Python模块"
    python -m swift.cli.main web-ui --server_port 8080 --server_name 0.0.0.0 --lang zh
fi

echo "服务已启动，请访问 http://<服务器IP>:8080"
echo "菜单联动功能修复说明："
echo "- 点击主菜单项（如'模型训练'）可展开/收起子菜单"
echo "- 箭头图标会旋转显示展开/收起状态"
echo "- 子菜单项点击可切换到对应功能标签页"