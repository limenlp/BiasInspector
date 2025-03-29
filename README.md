# BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents

This repository contains the anonymized implementation, evaluation scripts, and experimental data for our paper titled:  
**"BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents"**.

## 📁 Repository Structure

submission/
│
├── agents/                          
│   ├── bias_inspector_multi/         # Multi-Agent framework
│   ├── bias_inspector_single/        # Single-Agent framework
│   ├── react_agent/                  # ReAct-based Agent
│   └── self_reflection_agent/        # Self-reflection Agent
│
├── evaluation/
│   ├── result_evaluation/            # Evaluation of final bias detection results
│   └── process_evaluation/           # Evaluation of reasoning steps and tool usage
│
├── data/
│   ├── dataset&taskset/                      # Structured data used in experiments
│   ├── eval_results/                 # CSV files containing evaluation results
│   └── logs/                         # Execution logs per agent and model
│
└── README.md                         # Project documentation


## 📂 Data & Experimental Logs

All data used for experiments are located under the `data/` directory:

- `dataset/`: Structured datasets used for bias detection experiments.
- `eval_results/`: CSV files storing final evaluation metrics.
- `logs/`: Log files generated during agent execution across different LLMs (GPT-4o and Llama 3.3 70B).  
  Each file is named to reflect the agent and model used.

## 🚫 Anonymity Notice

This repository has been anonymized in accordance with double-blind review requirements. 

For any questions or clarifications, please refer to the anonymous submission portal using the submission ID provided.