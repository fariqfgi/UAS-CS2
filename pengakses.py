from app import *

# materi pertemuan 13 dan 14
@app.route('/getuser', methods=['GET'])
@jwt_required
def getuser():
    all_users = Mahasiswa.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result), 200

@app.route('/getuser/<ID>', methods=['GET'])
@jwt_required
def getuser(ID):
    mahasiswa = Mahasiswa.query.get(ID)
    return user_schema.jsonify(mahasiswa)

if __name__ == '__main__':
    app.run()