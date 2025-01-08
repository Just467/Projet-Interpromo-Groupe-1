import camelot
import pdfplumber
import pandas as pd

def delete_first_occurrences(s, substrings):
    for substring in substrings:
        index = s.find(substring)
        s = s[:index] + s[index + len(substring):]
    return s

def find_all_largest_common_substrings(s1, s2):
    common_substrings = []
    if len(s1)>len(s2):
        shortest_s, longest_s, len_shortest = s2, s1, len(s2)
    else:
        shortest_s, longest_s, len_shortest = s1, s2, len(s1)
    for len_substring in range(len_shortest-1, 1, -1):
        for index_substring in range(1+len_shortest-len_substring):
            substring = shortest_s[index_substring:index_substring+len_substring]
            if len(substring) < len_substring:
                break
            if substring in longest_s:
                common_substrings.append(substring)
                longest_s = delete_first_occurrences(longest_s, [substring])
                shortest_s = delete_first_occurrences(shortest_s, [substring])
    return common_substrings

page_number = 17
with pdfplumber.open(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf") as pdf:
    settings = {}
    page = pdf.pages[page_number]
    pdfplumber_df = pd.DataFrame(page.extract_table(settings))
stream_tables = camelot.read_pdf(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf", flavor="stream", pages=f'{page_number+1}')
stream_df = stream_tables[0].df

pdfplumber_df = pdfplumber_df.head(10)
#print(f"Stream tables\n{stream_df}\n\n\n")
#print(f"Pdfplumber tables\n{pdfplumber_df}\n\n\n")

str_cat_rows = []
for index, row in pdfplumber_df.iterrows():
    str_cat_rows.append(row.astype(str).str.cat(sep=''))
str_cat_rows = str_cat_rows[:10]

str_cat_columns = []
for column_name in stream_df:
    str_cat_columns.append(stream_df[column_name].astype(str).str.cat(sep=''))


merged_table = []
for index_row, row in enumerate(str_cat_rows):
    merged_row = []
    for index_col, column in enumerate(str_cat_columns):
        common_strings = find_all_largest_common_substrings(row, column)
        print(f"{row}\n{column}\n{common_strings}\n\n\n")
        if common_strings:
            str_cat_rows[index_row] = delete_first_occurrences(row, common_strings)
            merged_row.append(common_strings)
        else:
            merged_row.append(None)
    merged_table.append(merged_row)

print(pd.DataFrame(merged_table))