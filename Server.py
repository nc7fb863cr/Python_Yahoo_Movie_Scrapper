from __init__ import *

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Movie List!</h1>'


@app.route('/get_all_movie')
def get_all():
    print ('開始建構資料')
    result = get_movie()
    print ('總共有{}筆資料'.format(len(result)))

    try:
        return jsonify({
            'data':result, #list
            'status':'成功'
            })
    except:
        return jsonify({
            'data':{},
            'status':'失敗'
            })


@app.route('/get_movie',methods=['GET'])
def get_single():
    index = request.args.get('index')
    print ('開始建構資料')
    try:
        index = int(index)
    except:
        index = 1

    result = get_movie(index)

    if result:
        return jsonify({
            "status":'成功',
            "data" : result #dict
            })

    else:        
        return jsonify({
            "status":'失敗',
            "data" : {}
            })
        
    print ('資料建構成功')

@app.route('/favicon.ico',methods=['GET'])
def icon():
    return send_from_directory('','favicon.jpg')


if __name__=='__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host= '192.168.0.100')
