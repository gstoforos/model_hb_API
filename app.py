from flask import Flask, request, jsonify
from flask_cors import CORS
from model_hb import fit_herschel_bulkley

app = Flask(__name__)
CORS(app)

@app.route('/fit', methods=['POST'])
def fit():
    try:
        data = request.get_json()
        shear_rates = data.get("shear_rates", [])
        shear_stresses = data.get("shear_stresses", [])
        flow_rate = data.get("flow_rate", 1.0)
        diameter = data.get("diameter", 1.0)
        density = data.get("density", 1.0)
        re_critical = data.get("re_critical", 4000)

        result = fit_herschel_bulkley(
            shear_rates, shear_stresses,
            flow_rate, diameter, density,
            re_critical
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
