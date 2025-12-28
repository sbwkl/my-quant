import pandas as pd
import os
import sys
from pathlib import Path
import glob

# 只支持合并 choice 导出的 xlsx 文件和 yfinance 下载的 csv 文件
def main(folder_path, target_filename):

    target_path = Path(target_filename)
    
    target_file = target_path.stem
    target_extension  = target_path.suffix

    # 查找所有符合条件的Excel文件
    file_pattern = f'{target_file}.*'
    print(folder_path, file_pattern)
    excel_files = list(Path(folder_path).resolve().glob(file_pattern))

    # 排除目标输出文件（如果已存在）
    output_filename = target_file + target_extension
    excel_files = [f for f in excel_files if f.name != output_filename]

    print(f"找到 {len(excel_files)} 个文件:")
    for file in excel_files:
        print(f"  - {file.name}")

    if len(excel_files) == 0:
        print("未找到符合条件的文件！")
    else:
        read_method = globals()[f'read_{target_extension[1:]}']
        merge_method = globals()[f'merge_{target_extension[1:]}']
        # 读取所有文件并存储到列表
        df_list = []
        for file in excel_files:
            df = read_method(file)
            print(f"读取 {file.name}: {len(df)} 行")
            df_list.append(df)
        
        # 导出到新的Excel文件
        output_path = f'{folder_path}/../{output_filename}'
        
        # 合并所有数据框
        df_merged = merge_method(df_list, output_path)
        
        print(f"去重后行数: {len(df_merged)}")
        print(f"\n合并完成！已生成文件: {output_path}")
 
def read_xlsx(file):
    return pd.read_excel(file)

def merge_xlsx(df_list, output_path):
    df_combined = pd.concat(df_list, ignore_index=True)
    print(f"\n合并后总行数: {len(df_combined)}")
    df_merged = df_combined.drop_duplicates(subset=['交易时间'], keep='first')
    df_merged = df_merged.sort_values(by='交易时间').reset_index(drop=True)
    df_merged.to_excel(output_path, index=False)
    return df_merged

def read_csv(file):
    return pd.read_csv(file, header=[0, 1], index_col=[0])

def merge_csv(df_list, output_path):
    df_combined = pd.concat(df_list, axis=0, join='outer')
    print(f"\n合并后总行数: {len(df_combined)}")
    df_merged = df_combined.loc[~df_combined.index.duplicated(keep='first')]
    # df_merged = df_merged.sort_index()
    df_merged.to_csv(output_path)
    return df_merged
 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python merge_excel.py <folder_path> <file_prefix>")
        print("示例: python merge_excel.py . K线导出_AG0_5分钟线数据")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    file_prefix = sys.argv[2]
    
    main(folder_path, file_prefix)