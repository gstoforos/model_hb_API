from flask import Flask, request, jsonify
from model_hb import fit_herschel_bulkley

app = Flask(__name__)

@app.route('/fit', methods=['POST'])
def fit():
    try:
        data = request.get_json()  # ✅ This line is MISSING in your code!

        shear_rates = data['shear_rates']
        shear_stresses = data['shear_stresses']
        flow_rate = data['flow_rate']
        diameter = data['diameter']
        density = data['density']

        result = fit_herschel_bulkley(
            shear_rates, shear_stresses, flow_rate, diameter, density
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




