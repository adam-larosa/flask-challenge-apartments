from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from models import db, Tenant

import ipdb

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )
api = Api( app )



class Tenants( Resource ):
    def get( self ):
        tenants_list = []
        for t in Tenant.query.all():
            t_dict = {
                'id': t.id,
                'name': t.name,
                'age': t.age
            }
            tenants_list.append( t_dict )
        return make_response( tenants_list, 200 )

    def post( self ):
        data = request.get_json()
        new_tenant = Tenant( name = data['name'], age = data['age'] )
        try:
            db.session.add( new_tenant )
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response( {'error': 'validation errors'}, 422 )
        return make_response( new_tenant.to_dict(), 201 )

api.add_resource( Tenants, '/tenants' )


class TenantsById( Resource ):

    def get( self, id ):
        t = Tenant.query.filter_by( id = id ).first()
        if t == None:
            return make_response( { 'msg': 'Tenant not found' }, 404 )
        return make_response( t.to_dict(), 200 )

    def patch( self, id ):
        t = Tenant.query.filter_by( id = id ).first()
        if t == None:
            return make_response( { 'msg': 'Tenant not found' }, 404 )
        data = request.get_json()
        for key in data.keys():
            setattr( t, key, data[key] )
        db.session.add( t )
        db.session.commit()
        return make_response( t.to_dict(), 200 )

    def delete( self, id ):
        t = Tenant.query.filter_by( id = id ).first()
        if t == None:
            return make_response( { 'msg': 'Tenant not found' }, 404 )
        db.session.delete( t )
        db.session.commit()
        return make_response( {'msg': 'success'}, 200 )

api.add_resource( TenantsById, '/tenants/<int:id>')



if __name__ == '__main__':
    app.run( port = 3000, debug = True )