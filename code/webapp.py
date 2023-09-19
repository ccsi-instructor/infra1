
from flask import Flask

app = Flask(__name__)

@app.route('/webapp', methods=['GET'])
def webapp():
    
    return 'We have to learn docker somewhere.', 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80, threaded=True)
