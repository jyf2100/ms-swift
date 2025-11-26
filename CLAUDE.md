# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.


## Project Overview

MS-Swift (Scalable lightWeight Infrastructure for Fine-Tuning) is a comprehensive framework for fine-tuning and deploying large language models (LLMs) and multi-modal models. It supports 600+ LLMs and 300+ multi-modal models, providing complete training-to-deployment pipelines.

## Common Development Commands

### Installation and Setup
```bash
# Install from source
pip install -e .

# Install with all optional dependencies
bash requirements/install_all.sh

# Build wheel package
python setup.py sdist bdist_wheel
```

### Testing and Quality
```bash
# Run tests (limited CI scripts available)
make test

# Linting (basic setup exists, scripts may need implementation)
make linter

# Build documentation
make docs
# or
bash .dev_scripts/build_docs.sh
```

### Running Swift Commands
The main CLI entry point is through the `swift` command:

```bash
# Training commands
swift sft --model <model_id> --dataset <dataset_id> --train_type lora
swift pt --model <model_id> --dataset <dataset_id>
swift rlhf --rlhf_type dpo --model <model_id> --dataset <dataset_id>

# Inference and deployment
swift infer --model <model_id>
swift deploy --model <model_id> --infer_backend vllm
swift eval --model <model_id> --eval_dataset ARC_c

# Web UI
SWIFT_UI_LANG=en swift web-ui
```

### Megatron Support
For Megatron parallel training, use the `megatron` command:
```bash
megatron pt --model <model_id> --dataset <dataset_id>
```

## Architecture Overview

### Core Package Structure

- **`swift/cli/`**: Command-line interface implementations for all Swift operations
  - `main.py`: Main CLI dispatcher with route mapping
  - Individual command modules: `sft.py`, `infer.py`, `deploy.py`, etc.
  - `_megatron/`: Megatron-specific CLI commands

- **`swift/llm/`**: Core LLM functionality
  - `model/`: Model handling and registration
  - `dataset/`: Dataset loading and processing
  - `template/`: Model templates and prompt formatting
  - `train/`: Training utilities
  - `infer/`: Inference engines (PT, vLLM, SGLang, LMDeploy)
  - `eval/`: Evaluation backends (EvalScope integration)
  - `export/`: Model export and quantization
  - `app/`: API server functionality

- **`swift/tuners/`**: Model fine-tuning techniques
  - `lora.py`: LoRA and QLoRA implementations
  - `adapter.py`: Adapter tuning methods
  - `peft.py`: PEFT (Parameter Efficient Fine-Tuning) integration
  - `restuning.py`: ReFT (Representation Fine-Tuning)
  - `prompt.py`: Prompt tuning methods

- **`swift/trainers/`**: Training orchestration
  - `trainers.py`: Core trainer implementations
  - `mixin.py`: Training utilities and mixins
  - `rlhf_trainer/`: RLHF-specific trainers (DPO, GRPO, PPO, etc.)
  - `optimizers/`: Custom optimizer implementations

- **`swift/megatron/`**: Megatron parallel training integration
  - Megatron-specific training configurations and distributed training

- **`swift/ui/`**: Gradio-based Web UI
  - `app.py`: Main Web UI application
  - Training, inference, and deployment interfaces

- **`swift/utils/`**: Shared utilities
  - Configuration management, logging, import utilities

### Key Design Patterns

1. **Unified CLI Interface**: All operations accessible through the `swift` command with consistent parameter patterns
2. **Plugin Architecture**: Extensible model and dataset registration system
3. **Template System**: Model-specific prompt templates and formatting
4. **Backend Abstraction**: Support for multiple inference engines (PyTorch, vLLM, SGLang, LMDeploy)
5. **Training Abstraction**: Unified training interface supporting various fine-tuning methods

### Model and Dataset Support

- **Models**: Supports 600+ LLMs (Qwen, Llama, InternLM, GLM, Mistral, etc.) and 300+ multi-modal models
- **Datasets**: 150+ pre-training, fine-tuning, and RLHF datasets
- **Custom Extensions**: Support for custom models and datasets through registration system

### Training Methods

- **Fine-tuning**: LoRA, QLoRA, AdaLoRA, DoRA, Adapter, etc.
- **RLHF**: DPO, GRPO, PPO, KTO, CPO, SimPO, ORPO
- **Pre-training**: Full parameter training with streaming support
- **Multi-modal**: VQA, captioning, OCR, grounding tasks

### Distributed Training

- **Data Parallel**: DDP support
- **Model Parallel**: Megatron integration
- **Hybrid Parallel**: DeepSpeed ZeRO2/ZeRO3, FSDP
- **Sequence Parallel**: Support for long sequences

## Development Guidelines

### Adding New Models
1. Register models in the appropriate model registry
2. Create template files for prompt formatting
3. Add model-specific configurations
4. Test with supported training methods

### Adding New Training Methods
1. Implement tuner class in `swift/tuners/`
2. Register in the mapping system
3. Add CLI argument support
4. Update trainer configurations

### Testing
- Limited test infrastructure currently exists
- Focus on integration testing with actual model training
- Web UI testing through browser interaction

### Documentation
- Sphinx-based documentation in `docs/`
- API documentation auto-generated from docstrings
- Build with `make docs` or `bash .dev_scripts/build_docs.sh`

## Entry Points

- **CLI**: `swift=swift.cli.main:cli_main`
- **Megatron CLI**: `megatron=swift.cli._megatron.main:cli_main`
- **Python API**: Import from `swift` package directly

## Configuration

- **Requirements**: Managed in `requirements/` directory with separate files for different components
- **Version**: Defined in `swift/version.py`
- **Optional Dependencies**: Available via extras_require in setup.py (eval, ray, swanlab)