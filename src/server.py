import json
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def return_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)

def abort(msg: str, status_code: int):
    return return_json({
        'success': False,
        'data': [],
        'msg': msg
    }), status_code

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test():
    print('req', request.__dict__)
    print('files', request.files)
    print('json', request.get_json(silent=True))
    print('args', request.args)
    print('form', request.form)

    return return_json({
        'reg': str(request.__dict__),
        'files': str(request.files),
        'json': str(request.get_json(silent=True)),
        'args': str(request.args),
        'form': str(request.form)
    })

@app.route('/minimize')
@app.route('/maximize')
@app.route('/close')
def window_titlebar():
    print(request.url)
    return return_json({
        'success': True
    })


if __name__ == '__main__':
    app.run(port=5010)