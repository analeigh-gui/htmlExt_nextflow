import pandas as pd
from bs4 import BeautifulSoup
import io
import re
import os
import sys

def extract_tables_with_titles(soup):
    tables_with_titles = []
    for i, table in enumerate(soup.find_all("table")):
        title = None
        previous_h3 = table.find_previous("h3")
        if previous_h3:
            title = previous_h3.get_text(strip=True)
        elif table.find("caption"):
            title = table.find("caption").get_text(strip=True)
        else:
            title = f"Table_{i + 1}"
        try:
            df = pd.read_html(str(table))[0]
            tables_with_titles.append((title, df))
        except ValueError:
            continue
    return tables_with_titles

def main(html_path, assay_type="UnknownAssay", source="UnknownSource"):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Extract run_name from JavaScript in the HTML
    script_tag = soup.find("script", text=re.compile(r"run_name\s*=\s*\["))
    if script_tag:
        match = re.search(r"run_name\s*=\s*\['(.*?)'\];", script_tag.string)
        run_name = match.group(1) if match else "UnknownRunName"
    else:
        run_name = "UnknownRunName"

    # Extract pipeline version from HTML
    pipeline_version = "UnknownVersion"
    version_regex = re.compile(r"Pipeline Version[:\s]*([vV]?[\d\.]+[\w\-]*)")
    for string in soup.stripped_strings:
        version_match = version_regex.search(string)
        if version_match:
            pipeline_version = version_match.group(1)
            break

    base_name = os.path.splitext(os.path.basename(html_path))[0]
    output_excel = f"{base_name}.xlsx"

    tables_with_titles = extract_tables_with_titles(soup)

    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        for idx, (title, df) in enumerate(tables_with_titles):
            sheet_name = title[:31].replace("/", "_").replace("\\", "_")
            df.insert(0, "source", source)
            df.insert(1, "assayType", assay_type)
            df.insert(2, "runName", run_name)
            df.insert(3, "pipelineVersion", pipeline_version)
            
            # Apply filter to ALL sheets, not just the first one
            df = df[df.iloc[:, 4:].apply(lambda x: x.notna() & (x.astype(str).str.strip() != ''), axis=1).any(axis=1)]
            
            df.to_excel(writer, index=False, sheet_name=sheet_name)

if __name__ == "__main__":
    html_path = sys.argv[1]
    assay_type = sys.argv[2] if len(sys.argv) > 2 else "UnknownAssay"
    source = sys.argv[3] if len(sys.argv) > 3 else "UnknownSource"
    main(html_path, assay_type, source)