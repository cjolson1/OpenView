import os
from flask import Flask, request, jsonify, render_template
from flask_restful import reqparse, abort, Api, Resource
from data import get_category_data, data_frame, pass_data_frame, get_company_data

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
    companies = sorted(set([(data_frame['id'][i], data_frame['name'][i]) for i in range(len(data_frame['id']))] + [(pass_data_frame['id'][i], pass_data_frame['name'][i]) for i in range(len(pass_data_frame['id']))]), key=lambda point: point[1])
    return render_template('home.html', companies=companies)

@app.route('/api/category/<type>/', methods=['GET'])
def category_data_retrieve(type):
    if request.method == 'GET':
        start_time = request.args.get('start_date')
        end_time = request.args.get('end_date')
        ret = get_category_data(type, start_time, end_time)
        # print ret
        return jsonify(ret)

@app.route('/api/company/<id>/', methods=['GET'])
def company_data_retrieve(id):
    if request.method == 'GET':
        ret = get_company_data(id)
        # print ret
        return jsonify(ret)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)