from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Lease( db.Model, SerializerMixin ):
    __tablename__ = 'leases'
    id = db.Column( db.Integer, primary_key = True )
    rent = db.Column( db.Float )
    apartment_id = db.Column( db.Integer, db.ForeignKey( 'apartments.id' ) )
    tenant_id = db.Column( db.Integer, db.ForeignKey( 'tenants.id' ) )

class Apartment( db.Model, SerializerMixin ):
    __tablename__ = 'apartments' 
    id = db.Column( db.Integer, primary_key = True )
    number = db.Column( db.String )

    leases = db.relationship( 'Lease', backref = 'apartment' )
    tenants = association_proxy( 'leases', 'tenant' )



class Tenant( db.Model, SerializerMixin ):
    __tablename__ = 'tenants'

    serialize_rules = ( '-leases.tenant', '-leases.apartment' )

    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String, nullable = False )
    age = db.Column( db.Integer, db.CheckConstraint( 'age >= 18' ), 
                     nullable = False  )
    leases = db.relationship( 'Lease', backref = 'tenant' )

    apartments = association_proxy( 'leases', 'apartment' )
    # @property      # <----- another way to get the apartment out of the lease
    # def apartments( self ):
    #     return [ l.apartment for l in self.leases ]
   

    __table_args__ = (
        db.CheckConstraint( 'age >= 18' ),
    )
