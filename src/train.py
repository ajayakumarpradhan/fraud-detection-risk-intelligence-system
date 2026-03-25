import os
import argparse
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, f1_score, auc, classification_report
import joblib

def engineer_features(df):
    """Derive smart transactional features."""
    df = df.copy()
    # Balance inconsistencies
    df['errorBalanceOrig'] = df['newbalanceOrig'] + df['amount'] - df['oldbalanceOrg']
    df['errorBalanceDest'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']
    
    # Time based feature: 1 step = 1 hour
    df['hour_of_day'] = df['step'] % 24
    
    # Drop irrelevant or identifying columns
    df.drop(columns=['nameOrig', 'nameDest', 'isFlaggedFraud'], inplace=True, errors='ignore')
    
    # Encode 'type' using one-hot encoding
    df = pd.get_dummies(df, columns=['type'], drop_first=True)
    return df

def main(data_path, out_dir, sample_frac=0.1):
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    if sample_frac < 1.0:
        print(f"Sampling {sample_frac*100}% of non-fraud cases...")
        fraud = df[df['isFraud'] == 1]
        non_fraud = df[df['isFraud'] == 0].sample(frac=sample_frac, random_state=42)
        df = pd.concat([fraud, non_fraud]).reset_index(drop=True)

    print("Engineering features...")
    df = engineer_features(df)
    
    X = df.drop(columns=['isFraud'])
    y = df['isFraud']
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    neg_count = (y_train == 0).sum()
    pos_count = (y_train == 1).sum()
    scale_pos_weight = neg_count / pos_count
    
    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric='aucpr',
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    import warnings
    warnings.filterwarnings("ignore")
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
    print(f"PR-AUC: {auc(recall, precision):.4f}")
    
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
    print(f"Optimal Threshold chosen: {best_threshold:.4f}")
    
    os.makedirs(out_dir, exist_ok=True)
    model.save_model(os.path.join(out_dir, 'xgboost_fraud_model.json'))
    joblib.dump(list(X.columns), os.path.join(out_dir, 'feature_columns.pkl'))
    with open(os.path.join(out_dir, 'threshold.txt'), 'w') as f:
        f.write(str(best_threshold))
        
    print(f"Artifacts saved to {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default=r"C:\Users\ajaya\Downloads\fraud detection\Fraud.csv")
    parser.add_argument("--out", type=str, default=r"C:\Users\ajaya\.gemini\antigravity\scratch\fraud_detection\models")
    parser.add_argument("--sample", type=float, default=0.1)
    args = parser.parse_args()
    main(args.data, args.out, args.sample)
