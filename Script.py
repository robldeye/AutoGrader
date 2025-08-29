import pandas as pd
import subprocess
import os

# Files
csv = 'Grades.csv'

# Data Check
try:
    df = pd.read_csv(csv)
except FileNotFoundError:
    print(f"Error: '{csv}' not found in the current directory. Ensure the file is named '{csv}'")
    exit()

if os.path.exists(f'output.pdf'):
    os.remove(f'output.pdf')

# Function for suffixes
def get_suffix(n):
    if 10 <= n % 100 <= 13:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

# LaTeX content
latex_filename = "output.tex"
pdf_filename = "output.pdf"
latex_content = [
    "\\documentclass{article}",
    "\\usepackage{geometry}",
    "\\geometry{a4paper, margin=1in}",
    "\\title{Minimal Working Example}",
    "\\begin{document}",
    "\\maketitle",
    "",
    "\\section*{Placing Participants}",
    ""
]

# Determine general scoring participants
scoring_participants = df[df['Order'] <= 3]

if not scoring_participants.empty:
    for index, row in scoring_participants.iterrows():
        participant_name = row['Student']
        rank = row['Order']
        suffix = get_suffix(rank)
        score = row['Auto']
        latex_content.append(f"\\section*{{{rank}{suffix} Place:}}")
        latex_content.append(f"\\textbf{{{participant_name}}} achieved {rank}{suffix} place with a score of \\textbf{{{score}}}.")
else:
    latex_content.append("No participants found with a score to rank.")

latex_content.append("\\end{document}")

# Write file
with open(latex_filename, 'w') as f:
    f.write("\n".join(latex_content))
print(f"Compiling 'PDF'...")
subprocess.run(['pdflatex', f'output.tex'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Cleanup temp files
for ext in ['.aux', '.log', '.out', '.tex']:
    temp_file_path = f'output{ext}'
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
print(f"Successfully generated '{pdf_filename}' with scoring participants.")