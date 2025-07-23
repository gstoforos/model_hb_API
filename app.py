from flask import Flask
from flask_cors import CORS
from model_hb import fit_herschel_bulkley

app = Flask(__name__)
CORS(app)

@app.route('/fit', methods=['POST'])
def run_fit():
    return fit_herschel_bulkley()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
