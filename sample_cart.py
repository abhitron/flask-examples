from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import sqlite3

app = Flask(__name__)
api = Api(app)

cart={
        1:{
            'LG':{'quantity':1,'price':9000},
            'Nexus' : {'quantity':2, 'price':20000}
             },
        2 :{
            'Moto':{'quantity':1,'price':6999},
            'Mi' : {'quantity':2, 'price':23999}
             }
      }

parser = reqparse.RequestParser()
parser.add_argument('product')
parser.add_argument('quantity',type=int)
parser.add_argument('price',type=int)

def abort_if_object_doesnt_exist(key,data):
    if key not in data:
        abort(404, message="Object {0} doesn't exist".format(key))

class SampleCart(Resource):

    def get(self,user_id,product):
        abort_if_object_doesnt_exist(user_id,cart)
        abort_if_object_doesnt_exist(product,cart[user_id])
        return cart[user_id][product]

    def put(self,user_id,product):
        args = parser.parse_args()
        product_desc = {'quantity' : args['quantity'],'price' : args['price']}
        cart[user_id][product]= product_desc
        return product, 201

    def delete(self,user_id,product):
        abort_if_object_doesnt_exist(user_id,cart)
        abort_if_object_doesnt_exist(product,cart[user_id])
        del cart[user_id][product]
        return '',204


class WholeCart(Resource):

    def get(self,user_id):
        abort_if_object_doesnt_exist(user_id,cart)
        return cart[user_id]

    def post(self,user_id):
        args=parser.parse_args()
        abort_if_object_doesnt_exist(user_id,cart)
        cart[user_id].setdefault(args['product'])
        cart[user_id][args['product']]={'quantity' : args['quantity'],'price':args['price']}
        return cart[user_id],201

    
api.add_resource(SampleCart,'/v1.0/<int:user_id>/<string:product>')
api.add_resource(WholeCart,'/v1.0/<int:user_id>')

if __name__=='__main__':
    app.run()
