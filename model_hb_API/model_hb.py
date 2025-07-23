import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import math

def hb_model(gamma, tau0, k, n):
    return tau0 + k * np.power(gamma, n)

def fit_hb_model(data):
    shear_rates = np.array(data.get("shear_rates", []))
    shear_stresses = np.array(data.get("shear_stresses", []))

    flow_rate = float(data.get("flow_rate", 1))
    diameter = float(data.get("diameter", 1))
    density = float(data.get("density", 1))

    try:
        popt, _ = curve_fit(hb_model, shear_rates, shear_stresses, bounds=([0, 0, 0], [np.inf, np.inf, 10]))
        tau0, k, n = popt
        predicted = hb_model(shear_rates, tau0, k, n)
        r2 = r2_score(shear_stresses, predicted)
    except Exception:
        tau0 = k = n = r2 = 0.0

    gamma_mean = np.mean(shear_rates)
    try:
        tau_mean = hb_model(gamma_mean, tau0, k, n)
    except:
        tau_mean = 0.0

    mu_app = tau_mean / gamma_mean if gamma_mean != 0 else 0.0

    if flow_rate > 0 and diameter > 0 and density > 0 and mu_app > 0:
        Q = flow_rate
        D = diameter
        rho = density
        Re = (4 * rho * Q) / (np.pi * D * mu_app)
    else:
        Re = 0.0

    for val in [tau0, k, n, r2, mu_app, Re]:
        if math.isnan(val) or math.isinf(val):
            val = 0.0

    return {
        "tau0": round(tau0, 6),
        "k": round(k, 6),
        "n": round(n, 6),
        "r2": round(r2, 6),
        "mu_app": round(mu_app, 6),
        "re": round(Re, 2),
        "equation": f"τ = {round(tau0, 2)} + {round(k, 2)}·γ̇^{round(n, 2)}"
    }
