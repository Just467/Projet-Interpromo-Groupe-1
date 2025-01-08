import camelot
import pdfplumber
import pandas as pd
import regex as re

page_number = 17

with pdfplumber.open(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf") as pdf:
    settings = {}
    page = pdf.pages[page_number]
    pdfplumber_df = pd.DataFrame(page.extract_table(settings))

stream_tables = camelot.read_pdf(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf", flavor="stream", pages=f'{page_number+1}')
stream_df = stream_tables[0].df

#print(f"Stream tables\n{stream_df}\n\n\n")
#print(f"Pdfplumber tables\n{pdfplumber_df}\n\n\n")

def find_all_largest_common_substrings(s1, s2):
    substrings = [s1[i:j] for i in range(len(s1)) for j in range(i + 1, len(s1) + 1)]
    substrings.sort(key=len, reverse=True)

    max_length = 0
    largest_common_substrings = set()

    for substring in substrings:
        if len(substring) < max_length:
            break

        if re.search(re.escape(substring), s2):
            if len(substring) > max_length:
                max_length = len(substring)
                largest_common_substrings = {substring}
            else:
                largest_common_substrings.add(substring)

    return list(largest_common_substrings)

def delete_first_occurrences(s, substrings):
    for sub in substrings:
        index = s.find(sub)
        if index != -1:
            s = s[:index] + s[index + len(sub):]
    return s

str_cat_rows = []
for index, row in pdfplumber_df.iterrows():
    str_cat_rows.append(row.astype(str).str.cat(sep=''))

str_cat_columns = []
for column_name in stream_df:
    str_cat_columns.append(stream_df[column_name].astype(str).str.cat(sep=''))

merged_table = []
i = 0
for index_row, row in enumerate(str_cat_rows):
    i+=1
    print(i)
    merged_row = []
    for index_col, column in enumerate(str_cat_columns):
        print(row)
        print()
        print(column)
        print()
        common_strings = find_all_largest_common_substrings(row, column)
        print(common_strings)
        print("\n\n\n")
        if common_strings:
            str_cat_rows[index_row] = delete_first_occurrences(row, common_strings)
            merged_row.append(common_strings)
        else:
            merged_row.append(None)
    merged_table.append(merged_row)
    if i == 10:
        break

print(pd.DataFrame(merged_table))
