#libraries
import pandas as pd
import numpy as np

#load dataset
df = pd.read_csv("data/trends_clean.csv")

#check shape
print("Loaded data:", df.shape)

#view first 5 rows
print("\nFirst 5 rows:")
print(df.head())

#average of score and comments
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()

print("\nAverage score:", int(avg_score))
print("Average comments:", int(avg_comments))

#convert to NumPy array
scores = df['score'].values   

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print("Mean score:", int(mean_score))
print("Median score:", int(median_score))
print("Std deviation:", int(std_score))
print("Max score:", max_score)
print("Min score:", min_score)

#categorise
category_counts = df['category'].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print("\nMost stories in:", top_category, f"({top_count} stories)")


#display the most commented story
max_comments_row = df.loc[df['num_comments'].idxmax()]

print("\nMost commented story:")
print(f"\"{max_comments_row['title']}\" - {max_comments_row['num_comments']} comments")

df['engagement'] = df['num_comments'] / (df['score'] + 1)
df['is_popular'] = df['score'] > avg_score

#save to CSV
df.to_csv("data/trends_analysed.csv", index=False)
print("\nSaved to data/trends_analysed.csv")
