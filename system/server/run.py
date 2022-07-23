from src import app
from flask_cors import CORS

CORS(app, supports_credentials=True)
# app.run(host='127.0.0.1', port=5000, use_reloader=True, debug=True)
# app.run(host='127.0.0.1', port=5050, use_reloader=True, debug=True)
# app.run(host='127.0.0.1', port=5055, use_reloader=True, debug=True)
app.run(host='10.192.9.11', port=5055, use_reloader=True, debug=True)
