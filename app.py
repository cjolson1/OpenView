import os
from flask import Flask, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
from data import get_data

app = Flask(__name__)
api = Api(app)

class DataRetrieval(Resource):
    def get(self, type, start_time, end_time):
        data, layout, note = get_data(type, start_time, end_time)
        return jsonify({
            'layout': layout,
            'data': data,
            'note': note
        })


api.add_resource(Resource, '/api/<type>/<start_time>/<end_time>')

@app.route('/')
def display():
    return render_template('home.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)