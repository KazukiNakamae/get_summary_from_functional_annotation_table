import pandas as pd
import sys
import re
import operator
from collections import defaultdict

def count_genes(input_file, output_file):
    # CSVファイルを読み込む
    df = pd.read_csv(input_file)
    
    # 各XXX-ENSPID列のカウントを格納する辞書を初期化
    counts = {}
    characterized_counts = defaultdict(lambda: {"Characterized": 0, "Non-characterized": 0, "Less-characterized": 0})
    
    # ENSPID列を自動検出してカウント
    for column in df.columns:
        match = re.match(r'^(.*)-ENSPID$', column)
        if match:
            prefix = match.group(1)
            counts[prefix] = df[column].notna().sum()
            
            gsymbol_col = f"{prefix}-gsymbol"
            gdescription_col = f"{prefix}-gdescription"
            
            if gsymbol_col in df.columns and gdescription_col in df.columns:
                for idx, row in df[df[column].notna()].iterrows():
                    gsymbol = row[gsymbol_col]
                    gdescription = row[gdescription_col]
                    
                    if gsymbol != "non" and gdescription != "non-available":
                        characterized_counts[prefix]["Characterized"] += 1
                    elif gsymbol == "non" and gdescription == "non-available":
                        characterized_counts[prefix]["Non-characterized"] += 1
                    else:
                        characterized_counts[prefix]["Less-characterized"] += 1

    # その他ID列を自動検出してカウント
    for column in df.columns:
        match = re.match(r'^(.*)-ReferenceID$', column)
        if match:
            prefix = match.group(1)
            counts[prefix] = df[column].notna().sum()
            
            gsymbol_col = f"{prefix}-gsymbol"
            gdescription_col = f"{prefix}-gdescription"
            
            if gsymbol_col in df.columns and gdescription_col in df.columns:
                for idx, row in df[df[column].notna()].iterrows():
                    gsymbol = row[gsymbol_col]
                    gdescription = row[gdescription_col]
                    
                    if gsymbol != "non" and gdescription != "non-available":
                        characterized_counts[prefix]["Characterized"] += 1
                    elif gsymbol == "non" and gdescription == "non-available":
                        characterized_counts[prefix]["Non-characterized"] += 1
                    else:
                        characterized_counts[prefix]["Less-characterized"] += 1

    # UniProtKB-IDのカウント
    uniprotkb_count = df['UniProtKB-ID'].notna().sum()

    # UniProtKB-gsymbol列の文字列解析
    os_counts = defaultdict(int)
    os_counts["Others"] = 0
    method = "organism"
    for uniprot_gdescription in df.dropna(subset=['UniProtKB-ID'])['UniProtKB-gdescription']:
        match = re.search(r'OS=(.+)\sOX=.+PE=([1-5])', str(uniprot_gdescription))
        if match:
            if method == "organism":
                os_counts[match.group(1)] += 1
            elif method == "organism_PF":
                # PFごとにカウントする方法（かなり数が多くなってしまい可読性が悪くなるので不採用）
                if match.group(2) == "1":
                    os_counts["PE=1:'Experimental evidence at protein level' [" + match.group(1) + "]"] += 1
                elif match.group(2) == "2":
                    os_counts["PE=2:'Experimental evidence at transcript level' [" + match.group(1) + "]"] += 1
                elif match.group(2) == "3":
                    os_counts["PE=3:'Protein inferred from homology' [" + match.group(1) + "]"] += 1
                elif match.group(2) == "4":
                    os_counts["PE=4:'Protein predicted' [" + match.group(1) + "]"] += 1
                elif match.group(2) == "5":
                    os_counts["PE=5:'Protein uncertain' [" + match.group(1) + "]"] += 1                
        else:
            os_counts["Others"] += 1
    os_counts = dict(sorted(os_counts.items(), key=operator.itemgetter(1), reverse=True))
    temp_count = os_counts.pop("Others")
    os_counts["Others"] = temp_count
    
    # 少なくとも一つのカテゴリに含まれるもののカウント
    ens_columns = [col for col in df.columns if re.match(r'^(.*)-ENSPID$', col)]
    at_least_one_count = df[ens_columns + ['UniProtKB-ID']].notna().any(axis=1).sum()

    # Protein domainに含まれるもののカウント
    protein_domain_count = df[(df[ens_columns + ['UniProtKB-ID']].isna().all(axis=1)) & (df['Pfam-IDs'].notna())].shape[0]

    # Total genes with protein-level annotationのカウント
    total_protein_annotation_count = at_least_one_count + protein_domain_count

    # Hypothetical proteinのカウント
    hypothetical_protein_count = df['Target-pid'].notna().sum() - total_protein_annotation_count

    # Totalのカウント
    total_count = df['Target-pid'].notna().sum()

    # 結果をデータフレームにまとめる
    result_rows = []
    for prefix, count in counts.items():
        result_rows.append(["Protein homologue from tophit", "Ensembl:" + prefix, "", "", count])
        result_rows.append(["", "",f"Characterized", characterized_counts[prefix]["Characterized"], ""])
        result_rows.append(["", "",f"Less-characterized", characterized_counts[prefix]["Less-characterized"], ""])
        result_rows.append(["", "",f"Non-characterized", characterized_counts[prefix]["Non-characterized"], ""])
    
    result_rows.append(["Protein homologue from tophit", "UniProtKB/Swiss-Prot", "", "", uniprotkb_count])
    for os_name, os_name_count in os_counts.items():
        result_rows.append(["", "", os_name, os_name_count, ""])
    
    result_rows.append(["At least one of the above", "", "", "", at_least_one_count])
    result_rows.append(["No protein homologue, but with protein domain", "", "", "", protein_domain_count])
    result_rows.append(["Total genes with protein-level annotation", "", "", "", total_protein_annotation_count])
    result_rows.append(["Hypothetical protein", "", "", "", hypothetical_protein_count])
    result_rows.append(["Total", "", "", "", total_count])

    result_df = pd.DataFrame(result_rows, columns=["Annotation category", "Annotation level", "Details", "Detailed gene count", "Gene count",])

    # 結果をCSVファイルとして保存
    result_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_csv> <output_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    count_genes(input_csv, output_csv)
