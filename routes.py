from bottle import Bottle, route, run, jinja2_template as template, static_file, request,redirect
from bottle import response
from models import session, Books
from sqlalchemy import text
from utils.util import Utils
import logging

app = Bottle()

@app.get('/static/<filePath:path>')
def index(filePath):
    return static_file(filePath, root='./static')

@app.route('/', method='GET')
def index():
    redirect('/list')

@app.route('/add', method=['GET', 'POST'])
def add():
    view = ""
    registId = ""
    form = {}
    kind = "Registration"
    if request.method == 'GET':
        logging.info('Came to GET in /add')

        if request.query.get('id') is not None:
            book = session.query(Books).filter(Books.id_==request.query.get('id')).first()
            form['name'] = book.name
            form['volume'] = book.volume
            form['author'] = book.author
            form['publisher'] = book.publisher
            form['memo'] = book.memo
            registId = book.id_

            kind = "Edit"

        return template('add.html'
                , form = form
                , kind=kind
                , registId=registId)
    elif request.method == 'POST':
        logging.info('Came to POST in /add')
        form['name'] = request.forms.decode().get('name')
        form['volume'] = request.forms.decode().get('volume')
        form['author'] = request.forms.decode().get('author')
        form['publisher'] = request.forms.decode().get('publisher')
        form['memo'] = request.forms.decode().get('memo')
        registId = ""
        if request.forms.decode().get('id') is not None:
            registId = request.forms.decode().get('id')

        errorMsg = Utils.validate(data=form)
        print(errorMsg)
        if request.forms.get('next') == 'back':
            return template('add.html'
                    , form=form
                    , kind=kind
                    , registId=registId)

        if errorMsg == []:
            headers = ['Book Title', 'Volumes',' Authors',' Publishers',' Memo']
            return template('confirm.html'
                    , form=form
                    , headers=headers
                    , registId=registId)
        else:
            return template('add.html'
                    , error=errorMsg
                    , kind=kind
                    , form=form
                    , registId=registId)

@app.route('/regist', method='POST')
def regist():

    name = request.forms.decode().get('name');
    volume = request.forms.decode().get('volume');
    author = request.forms.decode().get('author');
    publisher = request.forms.decode().get('publisher');
    memo = request.forms.decode().get('memo');
    registId = request.forms.decode().get('id')

    if request.forms.get('next') == 'back':
        response.status = 307
        response.set_header("Location", '/add')
        return response
    else:
        if registId is not None:
            books = session.query(Books).filter(Books.id_==registId).first()
            books.name = name
            books.volume = volume
            books.author = author
            books.publisher = publisher
            books.memo = memo
            session.commit()
            session.close()
        else:
            logging.info('Adding a new book')
            books = Books(
                    name = name,
                    volume = volume,
                    author = author,
                    publisher = publisher,
                    memo = memo)
            session.add(books) 
            session.commit()
            session.close()
        redirect('/list')

@app.route('/list')
def passList():
    bookList = session.query(Books.name, Books.volume, Books.author, Books.publisher, Books.memo, Books.id_)\
            .filter(Books.delFlg == 0).all()
    headers = ['Title', 'Volume number', 'Author', 'Publishing house', 'Note', 'Operation']
    return template('list.html', bookList=bookList, headers=headers)

@app.route('/delete/<dataId>')
def delete(dataId):
    book = session.query(Books).filter(Books.id_==dataId).first()
    book.delFlg = 1
    session.commit()
    session.close()
    redirect('/list')

