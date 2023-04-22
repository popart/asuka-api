from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # do something with the data here
    print(data)
    response = jsonify({"role": "asuka", "content": "Hello, world"})
    return response

if __name__ == '__main__':
    app.run(debug=True)
