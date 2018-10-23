from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_mapping(
    DEBUG=True,
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///%s/tr.db' % app.instance_path,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)

db = SQLAlchemy(app)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


from rt.views import base
app.register_blueprint(base.bp)
# db.drop_all()
db.create_all()



