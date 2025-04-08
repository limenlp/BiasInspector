# BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents

This repository contains the implementation, evaluation scripts, and experimental data for our paper titled:  
**"BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents"**.

## 📁 Repository Structure

- `submission/`
  - `agents/`
    - `bias_inspector_multi/` – Multi-agent framework for bias detection
    - `bias_inspector_single/` – Single-agent framework implementation
    - `react_agent/` – ReAct-based agent with tool usage
    - `self_reflection_agent/` – Self-reflective agent for iterative reasoning
  - `evaluation/`
    - `result_evaluation/` – Scripts for evaluating final detection results
    - `process_evaluation/` – Scripts for analyzing reasoning steps and tool usage
  - `data/`
    - `dataset_and_taskset/` – Structured datasets and defined bias detection tasks
    - `eval_results/` – Evaluation metrics in CSV format
    - `logs/` – Execution logs per agent and model variant
  - `README.md` – Project documentation


## 📂 Data & Experimental Logs

All data used for experiments are located under the `data/` directory:

- `dataset/`: Structured datasets used for bias detection experiments.
- `eval_results/`: CSV files storing final evaluation metrics.
- `logs/`: Log files generated during agent execution across different LLMs (GPT-4o and Llama 3.3 70B).  
  Each file is named to reflect the agent and model used.
