import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import pairwise_distances
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt


# Create real data
np.random.seed(42)
real_data = pd.DataFrame({
    'age': np.random.randint(20, 60, 100),
    'income': np.random.normal(60000, 15000, 100).astype(int),
    'city': np.random.choice(['Dallas', 'Austin', 'Houston'], 100)
})


# Create synthetic data (statistically similar but not identical)
synthetic_data = pd.DataFrame({
    'age': np.random.randint(20, 60, 100),
    'income': np.random.normal(61000, 15500, 100).astype(int),
    'city': np.random.choice(['Dallas', 'Austin', 'Houston'], 100)
})

print(real_data.head())
print(synthetic_data.head())

le = LabelEncoder()
for col in ['city']:
    real_data[col] = le.fit_transform(real_data[col])
    synthetic_data[col] = le.transform(synthetic_data[col])

# Compute Euclidean distance between all pairs
dist_matrix = pairwise_distances(synthetic_data, real_data, metric='euclidean')

# Find minimum distance for each synthetic record
min_distances = dist_matrix.min(axis=1)

# Compute summary stats
print("Average DCR:", np.mean(min_distances))
print("Minimum DCR:", np.min(min_distances))

if np.min(min_distances) < 0.5:
    print("⚠️ Potential data plagiarism detected!")
else:
    print("✅ Synthetic data appears safe and unique.")

plt.figure(figsize=(10,4))
plt.hist(real_data['income'], bins=20, alpha=0.6, label='Real')
plt.hist(synthetic_data['income'], bins=20, alpha=0.6, label='Synthetic')
plt.title('Distribution Comparison')
plt.xlabel('Income')
plt.ylabel('Frequency')
plt.legend()
plt.show()