import pandas as pd
import os

# Load the cleaned CSV
df = pd.read_csv("josaa_data.csv")

def get_colleges_by_rank_and_gender(rank, gender):
    rank = int(rank)
    gender = gender.lower()

    if gender == 'male':
        eligible = df[
            (df['Seat Type'].str.lower() == 'open') &
            (df['Gender'].str.lower() == 'gender-neutral') &
            (df['Closing Rank'].fillna(999999).astype(int) >= rank)
        ]
    elif gender == 'female':
        eligible = df[
            (df['Seat Type'].str.lower() == 'open') &
            (
                (df['Gender'].str.lower() == 'gender-neutral') |
                (df['Gender'].str.lower().str.contains('female-only'))
            ) &
            (df['Closing Rank'].fillna(999999).astype(int) >= rank)
        ]
    else:
        print("❌ Invalid gender entered. Please type 'male' or 'female'.")
        return pd.DataFrame()

    return eligible[['Institute Name', 'Academic Program', 'Gender', 'Closing Rank']]

# Example usage
user_rank = input("Enter your JEE (CRL) rank: ")
user_gender = input("Enter your gender (male/female): ")

results = get_colleges_by_rank_and_gender(user_rank, user_gender)

if not results.empty:
    print("\n🎓 You may be eligible for the following programs:")
    print(results.to_string(index=False))

    # Export to files
    output_folder = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(output_folder, "eligible_colleges.csv")
    excel_path = os.path.join(output_folder, "eligible_colleges.xlsx")

    results.to_csv(csv_path, index=False)
    results.to_excel(excel_path, index=False)

    print(f"\n✅ Exported results to:\n- {csv_path}\n- {excel_path}")
else:
    print("\n❌ No programs found for your rank and gender preference.")
