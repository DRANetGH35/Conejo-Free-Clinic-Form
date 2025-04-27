from app import create_app


app = create_app()

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
    #                              host='192.168.86.53'