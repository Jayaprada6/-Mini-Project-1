import pandas as pd

#read JSON
file_path = "data/trends_20260410.json"
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

#EDA checklist

#removing duplicates
df = df.drop_duplicates(subset='post_id')
print(f"After removing duplicates: {len(df)}")

#remove missing values
df = df.dropna(subset=['post_id', 'title', 'score'])
print(f"After removing nulls: {len(df)}")

#check data type
df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].astype(int)

#remove less scores
df = df[df['score'] >= 5]
print(f"After removing low scores: {len(df)}")

#remove whitespace
df['title'] = df['title'].str.strip()

#save to CSV
output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")


print("\nStories per category:")
category_counts = df['category'].value_counts()

for category, count in category_counts.items():
    print(f"{category} {count}")
