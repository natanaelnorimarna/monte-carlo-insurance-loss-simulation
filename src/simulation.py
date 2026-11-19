"""
simulation.py
Fungsi-fungsi inti untuk Monte Carlo Aggregate Loss Model:
    S = X_1 + X_2 + ... + X_N,  N ~ Poisson(lam),  X_i ~ Lognormal(mu, sigma)
"""
import numpy as np


def simulate_aggregate_loss(lam=4.0, mu=10.0, sigma=0.8, n_sims=10_000, seed=42):
    """Simulasikan total kerugian tahunan (S) sebanyak n_sims kali.

    Mengembalikan (S, N): array total kerugian dan array jumlah klaim per simulasi.
    """
    rng = np.random.default_rng(seed)
    n_claims = rng.poisson(lam, size=n_sims)                 # frekuensi tiap tahun
    severities = rng.lognormal(mu, sigma, size=n_claims.sum())  # semua besar klaim
    year_id = np.repeat(np.arange(n_sims), n_claims)         # klaim milik tahun ke-berapa
    totals = np.bincount(year_id, weights=severities, minlength=n_sims)
    return totals, n_claims


def theoretical_moments(lam=4.0, mu=10.0, sigma=0.8):
    """Mean dan variansi S secara analitik (compound Poisson)."""
    mean_x = np.exp(mu + sigma**2 / 2)
    ex2 = np.exp(2 * mu + 2 * sigma**2)       # E[X^2] untuk Lognormal
    mean_s = lam * mean_x                     # E[S] = lam * E[X]
    var_s = lam * ex2                         # Var(S) = lam * E[X^2]
    return {"E[X]": mean_x, "E[S]": mean_s, "Var(S)": var_s, "SD(S)": np.sqrt(var_s)}


def value_at_risk(losses, level=0.95):
    """VaR: kuantil ke-level dari distribusi kerugian."""
    return float(np.quantile(losses, level))


def tail_value_at_risk(losses, level=0.95):
    """TVaR: rata-rata kerugian yang melampaui atau sama dengan VaR."""
    var = value_at_risk(losses, level)
    return float(losses[losses >= var].mean())


def running_mean(losses):
    """Rata-rata kumulatif untuk analisis konvergensi."""
    return np.cumsum(losses) / np.arange(1, len(losses) + 1)
