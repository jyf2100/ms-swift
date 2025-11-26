项目规则

1. 任何代码修改（含 UI/样式/脚本）完成后，必须立即重启服务以确保变更生效。
2. 重启方式：
   - 停止当前进程
   - 使用如下命令启动：
     env http_proxy=http://172.32.147.190:7890 \
         https_proxy=http://172.32.147.190:7890 \
         NO_PROXY=127.0.0.1,localhost,::1 \
         no_proxy=127.0.0.1,localhost,::1 \
         swift web-ui --server_port 7860 --server_name 0.0.0.0 --lang zh
3. 若验证不通过或出现异常，应立即回退本次修改。
4. 统一使用本文件所述代理与启动参数，保持一致性。
