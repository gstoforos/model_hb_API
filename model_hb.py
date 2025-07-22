import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

def hb_model(gamma, tau0, k, n):
    return tau0 + k * np.power(gamma, n)

def fit_hb_model(shear_rates, shear_stresses, flow_rate, diameter, density):
    shear_rates = np.array(shear_rates)
    shear_stresses = np.array(shear_stresses)

    try:
        # Fit HB model
        popt, _ = curve_fit(hb_model, shear_rates, shear_stresses, bounds=([0, 0, 0], [np.inf, np.inf, 10]))
        tau0, k, n = popt
        predicted = hb_model(shear_rates, tau0, k, n)
        r2 = r2_score(shear_stresses, predicted)
    except Exception:
        tau0 = k = n = r2 = 0.0

    # Apparent viscosity at mean shear rate
    gamma_mean = np.mean(shear_rates)
    tau_mean = hb_model(gamma_mean, tau0, k, n)
    mu_app = tau_mean / gamma_mean if gamma_mean != 0 else 0.0

    # Reynolds number (approximate)
     if flow_rate > 0 and diameter > 0 and density > 0:
      area = np.pi * (diameter ** 2) / 4
        velocity = flow_rate / area
        re = (density * velocity * diameter) / mu_app if mu_app > 0 else 0.0
    else:
re = None

    
    return {
        "tau0": round(tau0, 6),
        "k": round(k, 6),
        "n": round(n, 6),
        "r2": round(r2, 6),
        "mu_app": round(mu_app, 6),
        "re": round(re, 2),
        "equation": f"τ = {round(tau0,2)} + {round(k,2)}·γ̇^{round(n,2)}"
    }
