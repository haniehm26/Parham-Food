from app import app
import sys

path = '/home/haniehm26/mysite'
if path not in sys.path:
   sys.path.insert(0, path)

if __name__ == '__main__':
    # this is used to run the flask app
    app.run(debug=True, port=3333)