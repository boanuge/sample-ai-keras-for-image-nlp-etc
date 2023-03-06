from flask import Flask
#from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return "AI-Service Server"

@app.route('/image/<fileName>')
def gcooter(fileName):

    print(fileName)

    return f'AI-Service : Detecting @ {fileName}'

if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5555, debug=True)
