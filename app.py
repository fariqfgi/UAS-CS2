from flask_restful import Resource, Api
from flask import Flask, Response, request, json, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/Kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


class Mahasiswa(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(10), unique=False, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    alamat= db.Column(db.TEXT)

    def __init__(self, nim, nama, password, alamat):
        self.nim = nim
        self.password = password
        self.nama = nama
        self.alamat = alamat

    @staticmethod
    def get_all_users():
        return Mahasiswa.query.all()

    @staticmethod
    def get_user(nim):
        print(nim)
        return None


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nim', 'password', 'nama', 'alamat')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/mahasiswa/', methods=['POST'])
def add_user():
    nim = request.json['nim']
    password = request.json['password']
    nama = request.json['nama']
    alamat = request.json['alamat']

    new_mhs = Mahasiswa(nim, password, nama, alamat)

    db.session.add(new_mhs)
    db.session.commit()

    return user_schema.jsonify(new_mhs)

@app.route('/mahasiswa/', methods=['GET'])
def get_users():
    all_users = Mahasiswa.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/mahasiswa/<ID>', methods=['GET'])
def get_user(ID):
  mahasiswa = Mahasiswa.query.get(ID)
  return user_schema.jsonify(mahasiswa)

@app.route('/mahasiswa/<ID>', methods=['PUT'])
def update_user(ID):
  mahasiswa = Mahasiswa.query.get(ID)

  nim = request.json['nim']
  password = request.json['password']
  nama = request.json['nama']
  alamat = request.json['alamat']

  mahasiswa.nim = nim
  mahasiswa.password = password
  mahasiswa.nama = nama
  mahasiswa.alamat = alamat

  db.session.commit()

  return user_schema.jsonify(mahasiswa)

@app.route('/mahasiswa/<ID>', methods=['DELETE'])
def delete_product(ID):
  mahasiswa = Mahasiswa.query.get(ID)
  db.session.delete(mahasiswa)
  db.session.commit()

  return user_schema.jsonify(mahasiswa)


#materi pertemuan 12

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    nim = request.json.get('nim', None)
    password = request.json.get('password', None)
    login_user = Mahasiswa.query.filter_by(nim=nim).first()
    print(login_user.nim)
    print(login_user.password)


    if not nim:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if nim != login_user.nim or password != login_user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=nim)
    return jsonify(access_token=access_token), 200


if __name__ == '__main__':
    app.run()
