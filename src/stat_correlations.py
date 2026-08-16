import pandas as pd
from scipy.stats import pearsonr, spearmanr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "processed" / "state_correlations.csv"
OUT = ROOT / "reports" / "stats_summary.txt"

def main():
    df = pd.read_csv(CSV)
    
    # We want correlations for confidential_share vs corruption and pibe
    # Drop NaNs just in case, though we know there are none
    df = df.dropna(subset=['confidential_share', 'corruption_prevalence_2025_per100k', 'pibe_per_capita_2024_2018_mxn'])
    
    x1 = df['corruption_prevalence_2025_per100k']
    x2 = df['pibe_per_capita_2024_2018_mxn']
    y = df['confidential_share']
    
    # Calculate correlations
    p1, p1_p = pearsonr(x1, y)
    s1, s1_p = spearmanr(x1, y)
    
    p2, p2_p = pearsonr(x2, y)
    s2, s2_p = spearmanr(x2, y)
    
    summary = (
        "Statistical Correlations: Opacity (Confidential Share) vs. State Factors\n"
        "========================================================================\n\n"
        "1. Corruption Prevalence (ENCIG 2025)\n"
        f"   - Pearson r:  {p1:.4f} (p-value: {p1_p:.4g})\n"
        f"   - Spearman rho: {s1:.4f} (p-value: {s1_p:.4g})\n\n"
        "2. Economic Capacity (PIBE per capita 2024)\n"
        f"   - Pearson r:  {p2:.4f} (p-value: {p2_p:.4g})\n"
        f"   - Spearman rho: {s2:.4f} (p-value: {s2_p:.4g})\n"
    )
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(summary)
    
    print(summary)
    print(f"Saved to {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
