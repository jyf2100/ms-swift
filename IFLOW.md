# IFLOW Context for MS-SWIFT Project

## 项目概述

MS-SWIFT (Scalable lightWeight Infrastructure for Fine-Tuning) 是一个由 ModelScope 社区提供的官方框架，专门用于大语言模型和多模态大模型的微调和部署。该项目支持 600 多个大模型和 300 多个多模态大模型的训练（预训练、微调、人类对齐）、推理、评估、量化和部署。

### 核心特性

- **模型支持**: 支持 600+ 纯文本大模型、300+ 多模态大模型，涵盖从训练到部署的整个流程
- **数据集类型**: 内置 150+ 预训练、微调、人类对齐、多模态数据集，支持自定义数据集
- **硬件支持**: 兼容 CPU、RTX 系列、T4/V100、A10/A100/H100、Ascend NPU、MPS 等
- **轻量级训练**: 支持 LoRA、QLoRA、DoRA、LoRA+、ReFT、RS-LoRA、LlamaPro、Adapter、GaLore、Q-Galore、LISA、UnSloth、Liger-Kernel 等轻量级微调方法
- **分布式训练**: 支持分布式数据并行 (DDP)、device_map 简单模型并行、DeepSpeed ZeRO2/ZeRO3、FSDP、Megatron 等分布式训练技术
- **量化训练**: 支持 BNB、AWQ、GPTQ、AQLM、HQQ、EETQ 等量化模型训练
- **RLHF 训练**: 支持 DPO、GRPO、RM、PPO、GKD、KTO、CPO、SimPO、ORPO 等人类对齐训练方法
- **多模态训练**: 支持图像、视频、音频等不同模态的训练，支持 VQA、captioning、OCR、grounding 等任务
- **推理加速**: 支持 PyTorch、vLLM、SGLang、LmDeploy 等推理加速引擎
- **模型评估**: 使用 EvalScope 作为评估后端，支持 100+ 数据集的评估

## 项目结构

```
/mnt/disk01/workspaces/worksummary/ms-swift/
├── examples/           # 示例脚本
├── swift/             # 核心源代码
│   ├── llm/           # 大语言模型相关
│   ├── megatron/      # Megatron 相关
│   ├── ui/            # UI 相关
│   ├── utils/         # 工具函数
│   └── ...
├── docs/              # 文档
├── tests/             # 测试文件
├── requirements/      # 依赖文件
├── README.md          # 项目说明
└── ...
```

## 核心模块

### Swift 模块 (`swift/__init__.py`)
- 提供了模型微调的核心组件，包括各种 Tuner (LoRA, AdaLora, LoHa, OFT 等)
- 包含训练器 (Trainer, Seq2SeqTrainer) 和训练参数 (TrainingArguments)
- 提供了便捷的接口用于加载和使用微调模型

### 依赖 (`requirements/framework.txt`)
- 核心依赖包括 transformers, peft, trl, torch 等
- 支持的版本范围: transformers>=4.33,<4.58, peft>=0.11,<0.19, trl>=0.15,<0.25

## 构建和运行

### 安装
```bash
pip install ms-swift -U
```

或从源码安装:
```bash
git clone https://github.com/modelscope/ms-swift.git
cd ms-swift
pip install -e .
```

### 使用示例

#### 微调 (SFT)
```bash
CUDA_VISIBLE_DEVICES=0 swift sft \
    --model Qwen/Qwen2.5-7B-Instruct \
    --train_type lora \
    --dataset 'AI-ModelScope/alpaca-gpt4-data-zh#500' \
    --num_train_epochs 1 \
    --output_dir output
```

#### 推理
```bash
CUDA_VISIBLE_DEVICES=0 swift infer \
    --model Qwen/Qwen2.5-7B-Instruct \
    --stream true \
    --infer_backend pt \
    --max_new_tokens 2048
```

#### 部署
```bash
CUDA_VISIBLE_DEVICES=0 swift deploy \
    --model Qwen/Qwen2.5-7B-Instruct \
    --infer_backend vllm
```

### Web UI
```bash
SWIFT_UI_LANG=en swift web-ui
```

## 开发约定

1. **Python 版本**: 推荐使用 Python 3.10 或 3.11 (支持 >=3.9)
2. **框架依赖**: 
   - PyTorch >= 2.0 (推荐 2.8.0)
   - Transformers >= 4.33 (推荐 4.57.1)
   - ModelsSope >= 1.23
3. **命令行接口**: 使用 `swift` 命令行工具进行训练、推理、部署等操作
4. **模型支持**: 支持 HuggingFace 和 ModelScope 的模型和数据集
5. **训练方法**: 支持全参数微调、LoRA、QLoRA 等多种训练方法

## 主要功能

- **训练**: 支持预训练、指令监督微调、DPO、GRPO、奖励模型、PPO、GKD、KTO、CPO、SimPO、ORPO 等多种训练方法
- **推理**: 支持原生 PyTorch、vLLM、SGLang、LmDeploy 等推理后端
- **评估**: 使用 EvalScope 进行模型评估
- **量化**: 支持 AWQ、GPTQ、FP8、BNB 等量化方法
- **UI**: 基于 Gradio 的 Web UI 界面

该项目是一个功能全面的大模型微调和部署框架，支持多种模型架构、训练方法和硬件平台。