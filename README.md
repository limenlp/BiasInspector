# BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents

[![arXiv](https://img.shields.io/badge/arXiv-2504.04855-b31b1b.svg)](https://arxiv.org/abs/2504.04855)

This repository contains the implementation, evaluation scripts, and experimental data for our paper:  
**"BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents"**  
by Haoxuan Li, Mingyu Derek Ma, Jen-tse Huang, Zhaotian Weng, Wei Wang, and Jieyu Zhao.

We propose a comprehensive LLM-based agent framework for detecting distributional and correlational bias in structured datasets.  
Our approach integrates multi-agent collaboration, ReAct reasoning, and self-reflection to achieve both accuracy and interpretability.

## 📄 Citation

If you find this work helpful, please consider citing our paper:

**BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents**  
Haoxuan Li, Mingyu Derek Ma, Jen-tse Huang, Zhaotian Weng, Wei Wang, Jieyu Zhao  
arXiv: [2504.04855](https://arxiv.org/abs/2504.04855)

```bibtex
@misc{li2025biasinspectordetectingbiasstructured,
      title={BIASINSPECTOR: Detecting Bias in Structured Data through LLM Agents}, 
      author={Haoxuan Li and Mingyu Derek Ma and Jen-tse Huang and Zhaotian Weng and Wei Wang and Jieyu Zhao},
      year={2025},
      eprint={2504.04855},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2504.04855}, 
}
```

## 📬 Contact
For questions or collaboration opportunities, please contact:
Haoxuan Li – lihaoxua@usc.edu


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
