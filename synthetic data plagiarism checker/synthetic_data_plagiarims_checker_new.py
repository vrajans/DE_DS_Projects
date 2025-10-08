import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import pairwise_distances
from fuzzywuzzy import fuzz

class SyntheticDataPlagiarismChecker:
    def __init__(self, real_df, synthetic_df):
        self.real_df = real_df.copy()
        self.synthetic_df = synthetic_df.copy()
        self.encoded = False

    def encode_categorical(self):
        le = LabelEncoder()
        for col in self.synthetic_df.select_dtypes(include='object').columns:
            self.real_df[col] = le.fit_transform(self.real_df[col])
            self.synthetic_df[col] = le.transform(self.synthetic_df[col])
        self.encoded = True

    def exact_duplicate_check(self):
        duplicates = self.synthetic_df.merge(self.real_df, how='inner')
        return duplicates

    def numerical_distance_check(self):
        if not self.encoded:
            self.encode_categorical()
        dist_matrix = pairwise_distances(self.synthetic_df, self.real_df, metric='euclidean')
        min_distances = dist_matrix.min(axis=1)
        return min_distances

    def fuzzy_text_check(self, col, threshold=90):
        high_sim = []
        for syn_val in self.synthetic_df[col]:
            for real_val in self.real_df[col]:
                if fuzz.ratio(str(syn_val), str(real_val)) > threshold:
                    high_sim.append((syn_val, real_val))
        return high_sim

    def risk_report(self):
        duplicates = self.exact_duplicate_check()
        min_distances = self.numerical_distance_check()
        report = {
            "num_exact_duplicates": len(duplicates),
            "min_distance": np.min(min_distances),
            "avg_distance": np.mean(min_distances)
        }
        return report