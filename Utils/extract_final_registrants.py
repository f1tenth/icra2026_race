import pandas as pd
import re

def clean_email(raw_email):
    """
    Clean the raw email string to extract only the valid email address.
    This function removes extra characters such as parentheses or commas.
    """
    if not isinstance(raw_email, str):
        return ""
    raw_email = raw_email.strip()
    # Regex to capture a standard email address format.
    match = re.search(r'([\w\.-]+@[\w\.-]+\.\w+)', raw_email)
    return match.group(1) if match else raw_email

# Step 1: Read the Excel file.
# Assumption: Header is at row 2 (header=1) and the relevant columns are from B to G.
df = pd.read_excel(
    "Video Demo Checklist.xlsx",
    sheet_name="Data",
    header=1,
    usecols="B:G"
)

# Expected columns in order:
# "Team Name", "Full Name", "Email Adress", "Team Names", "Video Demo Submitted?", "Affiliation"

# Step 2: Filter rows with "Video Demo Submitted?" checked.
df_submitted = df[df["Video Demo Submitted?"] == True].copy()

# Step 3: Collect name/email pairs in a list.
rows_to_save = []

for _, row in df_submitted.iterrows():
    # --- Primary registrant ---
    primary_full_name = row["Full Name"]
    primary_raw_email = row["Email Adress"]
    primary_email = clean_email(primary_raw_email)
    
    if pd.notna(primary_full_name) and primary_email:
        rows_to_save.append({
            "Name": primary_full_name.strip(),
            "Email": primary_email
        })
    
    # --- Process additional team members ---
    team_members = row["Team Names"]
    if pd.notna(team_members):
        # Remove any leading label like "Team Members:".
        match = re.search(r":\s*(.+)", team_members)
        if match:
            team_members = match.group(1).strip()
        
        # Extract emails from the text using a capturing group.
        emails_in_text = re.findall(r'([\w\.-]+@[\w\.-]+\.\w+)', team_members)
        
        # Remove email addresses to leave behind the names.
        names_text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '', team_members)
        # Remove any content enclosed in parentheses.
        names_text = re.sub(r'\([^)]*\)', '', names_text)
        # Remove enumeration patterns like "1)" or "2)".
        names_text = re.sub(r'\s*\d+\)\s*', '', names_text)
        
        # Split the names; if commas are used, split by comma,
        # otherwise assume names are separated by whitespace in pairs.
        if ',' in names_text:
            names_extracted = [name.strip() for name in names_text.split(",") if name.strip()]
        else:
            words = names_text.strip().split()
            names_extracted = [
                " ".join(words[i:i+2]).strip() 
                for i in range(0, len(words), 2) if len(words[i:i+2]) == 2
            ]
        
        # Optional: Warn if the number of names and emails differ.
        if len(names_extracted) != len(emails_in_text):
            print(f"Warning: For team '{row['Team Name']}', extracted {len(names_extracted)} names and {len(emails_in_text)} emails.")
        
        # Pair each extracted name with its corresponding cleaned email.
        for i, name in enumerate(names_extracted):
            email_candidate = emails_in_text[i] if i < len(emails_in_text) else ""
            cleaned_email = clean_email(email_candidate)
            if name:
                rows_to_save.append({
                    "Name": name,
                    "Email": cleaned_email
                })

# Step 4: Create a DataFrame from the collected rows and save to a new Excel file.
final_df = pd.DataFrame(rows_to_save, columns=["Name", "Email"])
final_df.to_excel("RegisteredList.xlsx", index=False)

print("Successfully created RegisteredList.xlsx with Name and Email columns.")
