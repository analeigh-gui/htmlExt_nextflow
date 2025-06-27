import pandas as pd
from pathlib import Path
import sys
import glob

def merge_excels(master_path: Path,
                  other_paths: list[Path],
                  copy_new_sheets: bool = True,
                  dedupe: bool = False,
                  dedupe_subset: list[str] | None = None,
                  output_path: Path | None = None) -> Path:
    output_path = output_path or master_path.with_stem(f"merged_{master_path.stem}")
    
    # 1. Read master sheets
    master_sheets = pd.read_excel(master_path, sheet_name=None, engine="openpyxl")
    
    # 2. Walk through secondary files
    for src in other_paths:
        wb = pd.read_excel(src, sheet_name=None, engine="openpyxl")
        for sheet_name, df_other in wb.items():
            if sheet_name in master_sheets:
                df_master = master_sheets[sheet_name]
                
                # Align columns
                all_cols = df_master.columns.union(df_other.columns)
                df_master = df_master.reindex(columns=all_cols)
                df_other = df_other.reindex(columns=all_cols)
                
                merged = pd.concat([df_master, df_other], ignore_index=True, sort=False)
                
                if dedupe:
                    merged = merged.drop_duplicates(subset=dedupe_subset).reset_index(drop=True)
                
                master_sheets[sheet_name] = merged
            else:
                if copy_new_sheets:
                    master_sheets[sheet_name] = df_other
    
    # 3. Write output workbook
    with pd.ExcelWriter(output_path, engine="openpyxl", mode="w") as writer:
        for sheet_name, df in master_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output_path

if __name__ == "__main__":
    # Get all Excel files in current directory
    excel_files = list(Path(".").glob("*.xlsx"))
    
    if len(excel_files) < 2:
        print("Need at least 2 Excel files to merge")
        sys.exit(1)
    
    # Use first file as master, rest as others
    master = excel_files[0]
    others = excel_files[1:]
    
    output_file = Path("merged_results.xlsx")
    
    merged_path = merge_excels(master, others,
                               copy_new_sheets=True,
                               dedupe=False,
                               dedupe_subset=None,
                               output_path=output_file)
    
    print(f"Merged workbook saved to: {merged_path}")