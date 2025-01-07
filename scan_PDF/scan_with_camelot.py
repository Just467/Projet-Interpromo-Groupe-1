import camelot
tables = camelot.read_pdf(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf", pages='18', flavor='stream')
print(tables[0].df)