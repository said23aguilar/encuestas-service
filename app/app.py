# app.py# Required Imports
import os
from flask import Flask, request, jsonify
from controllers.predios_controllers import predio_blue_print
from controllers.encuestados_controllers import encuestados_blue_print

app = Flask(__name__)

app.register_blueprint(predio_blue_print)
app.register_blueprint(encuestados_blue_print)

port = int(os.environ.get('PORT', 8080))

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', debug=True, port=port)