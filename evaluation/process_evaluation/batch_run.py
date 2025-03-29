import os
import time
import pandas as pd
from main import run_agent_with_logname

# 等待 PDF 文件生成
def wait_for_pdf(pdf_filename, folder="generated_files", timeout=10, check_interval=1):
    pdf_path = os.path.join(folder, pdf_filename)
    waited = 0
    while waited < timeout:
        if os.path.exists(pdf_path):
            print(f"✅ PDF found: {pdf_path}")
            return True
        time.sleep(check_interval)
        waited += check_interval
    print(f"❌ Timeout: PDF {pdf_filename} not found in {folder} after {timeout} seconds.")
    return False

# 主批处理逻辑（新增 end_row）
def batch_process_from_csv(csv_path, start_row=0, end_row=None):
    df = pd.read_csv(csv_path, header=None)

    # 获取第一列的所有非空值，从 start_row 到 end_row（不包括 end_row）
    target_list = df.iloc[start_row:end_row, 0].dropna().tolist()

    for log_name in target_list:
        log_name = log_name.strip()
        print(f"\n\n======== Running for {log_name} ========")
        run_agent_with_logname(log_name)

        # 等待 PDF 文件生成
        pdf_filename = f"{log_name}.pdf"
        wait_for_pdf(pdf_filename, folder="generated_files")

# 执行入口
if __name__ == "__main__":
    # 举个例子：从第 37 行到第 50 行（不含第 50 行）
    batch_process_from_csv("DocsName.csv", start_row=50, end_row=100)
