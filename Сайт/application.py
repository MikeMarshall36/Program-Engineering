import time
from main import pdf_to_audio
from flask import *
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////First.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), nullable=False)
    e_mail = db.Column(db.String(64), nullable=False)
    passwd = db.Column(db.String(32), nullable=False)

    def __init__(self, file_id, user_name, passwd, e_mail):
        self.passwd = passwd.strip()
        self.e_mail = e_mail.srtip()
        self.user_name = user_name.strip()
        self.file_id = [File(file_id=file_id)]


class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(32), nullable=False)
    file = db.Column(db.BLOB)

    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.relationship("User", backref=db.backref('file_id', lazy=True))


@application.route('/home', methods=['GET'])
@application.route('/', methods=['GET'])
@application.route('/main', methods=['GET'])
@application.route('/main_page', methods=['GET'])
def home():
    return render_template('main.html')


@application.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@application.route('/help', methods=['GET'])
@application.route('/guide', methods=['GET'])
@application.route('/instruction', methods=['GET'])
def guide():
    return render_template('guide.html')


@application.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')


@application.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@application.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        print(file.filename)
        inputFile = (f'./{file.filename}')
        pdf_to_audio(inputFile)
        file_name = str(file.filename).split('.')
        time.sleep(5)
        return send_file(f'files/{file_name[0]}.mp3', as_attachment=True)
    if request.method == 'GET':
        return render_template('uploader.html')


if __name__ == '__main__':
    application.run(debug=False)
