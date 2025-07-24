from flask import request, jsonify
import numpy as np
from scipy.optimize import curve_fit

def hb_model(gamma, tau0, k, n):
    return tau0 + k * gamma ** n

def fit_herschel_bulkley():
    data = request.get_json()

    shear_rates = np.array(data["shear_rates"])
    shear_stresses = np.array(data["shear_stresses"])
    flow_rate = float(data.get("flow_rate", 1))
    diameter = float(data.get("diameter", 1))
    density = float(data.get("density", 1))
    Re_critical = float(data.get("re_critical", 4000))

    try:
        popt, _ = curve_fit(hb_model, shear_rates, shear_stresses, bounds=(0, np.inf))
        tau0, k, n = popt
        predictions = hb_model(shear_rates, *popt)

        ss_res = np.sum((shear_stresses - predictions) ** 2)
        ss_tot = np.sum((shear_stresses - np.mean(shear_stresses)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0

        gamma_mean = np.mean(shear_rates)
        mu_app = tau0 / gamma_mean + k * gamma_mean ** (n - 1) if gamma_mean > 0 else k

        # Correct HB Reynolds number
        v = (4 * flow_rate) / (np.pi * diameter**2)
        re = (density * v**(2 - n) * diameter**n) / (k * 8**(n - 1)) if k > 0 else 0

        # Correct HB q_critical
        if (2 - n) != 0 and k > 0:
            q_critical = (np.pi * diameter**2 / 4) * ((Re_critical * k * 8**(n - 1)) / (density * diameter**n))**(1 / (2 - n))
        else:
            q_critical = None

        return jsonify({
            "model": "Herschel–Bulkley",
            "tau0": tau0,
            "k": k,
            "n": n,
            "r2": r2,
            "mu_app": mu_app,
            "re": re,
            "re_critical": Re_critical,
            "q_critical": q_critical,
            "equation": f"τ = {tau0:.3f} + {k:.3f}·γ̇^{n:.3f}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
