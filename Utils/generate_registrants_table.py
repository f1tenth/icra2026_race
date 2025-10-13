import pandas as pd
import re

# Read the Excel file, using the "Data" sheet.
df = pd.read_excel("Video Demo Checklist.xlsx", sheet_name="Data")
# Re-read the Excel file to correctly parse the table.
# The header is in row 2 (header=1) and data starts from row 3 in Excel.
# Only columns from B onward are read.
df = pd.read_excel("Video Demo Checklist.xlsx", sheet_name="Data", header=1, usecols="B:F")

# Filter rows where "Video Demo Submitted?" is ticked.
submitted_teams = df[df["Video Demo Submitted?"] == True]

# Start building the HTML table.
html_table = """
<table>
    <thead>
        <tr>
            <th style="text-align: left">TEAM NAME</th>
            <th style="text-align: left">AFFILIATION</th>
            <th style="text-align: left">TEAM MEMBERS</th>
        </tr>
    </thead>
    <tbody>
"""

# Loop over the filtered teams and add a table row for each.
for _, row in submitted_teams.iterrows():
    team_name = row["Team Name"]
    affiliation = row["Affiliation"]
    team_members = row["Team Names"]

    if pd.isna(team_members):
        team_members = "N/A"
    match = re.search(r":\s*(.+)", team_members)
    if match:
        team_members = match.group(1).strip()
    
    # Remove plain email addresses (e.g., someone@example.com)
    team_members = re.sub(r'\S+@\S+', '', team_members)
    
    # Remove emails enclosed in parentheses (e.g., (someone@example.com))
    team_members = re.sub(r'\([^)]*\S+@\S+[^)]*\)', '', team_members)
    
    # Remove enumerations like "1)" at the beginning of the string
    team_members = re.sub(r'^\s*\d+\)\s*', '', team_members)
    
    # Split the team_members string into individual names
    names = team_members.strip().split()
    members = [" ".join(names[i:i+2]) for i in range(0, len(names), 2)]
    team_members = "<br>".join(members)

    html_table += f"""
        <tr>
            <td style="text-align: left">{team_name}</td>
            <td style="text-align: left">{affiliation}</td>
            <td style="text-align: left">{team_members}</td>
        </tr>
    """

# Close the table.
html_table += """
    </tbody>
</table>
"""

# Write the HTML table to a text file.
with open("registrants_table.html", "w", encoding="utf-8") as f:
    f.write(html_table)

print("HTML table generated and saved to registrants_table.html.")