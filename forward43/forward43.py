"""Main module."""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():         # TODO: Replace with real code
    return 'TEST - Run main module'
    
if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
