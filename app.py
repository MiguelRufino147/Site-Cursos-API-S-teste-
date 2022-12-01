from flask import Flask,render_template,request,redirect,url_for,flash
import urllib.request,json
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super secret key"


app.app_context().push()
db=SQLAlchemy(app)



frutas=[]
registros=[]

class cursos(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    nome= db.Column(db.String(50))
    descricao= db.Column(db.String(100))
    ch= db.Column(db.Integer)

    def __init__(self,nome,descricao,ch):
        self.nome=nome
        self.descricao=descricao
        self.ch=ch


@app.route('/',methods=["GET","POST"])
def ola():
    #frutas=['morango','pera','maça']
    if request.method=="POST":
        if request.form.get("fruta"):
            frutas.append(request.form.get("fruta"))
    return render_template('index.html',frutas=frutas)

@app.route('/sobre',methods=["GET","POST"])
def sobre():
    #notas={'Fulano':5.4,'beltrano':9.4}
    if request.method=="POST":
        if request.form.get('aluno') and request.form.get('nota'):
            registros.append({'aluno': request.form.get('aluno'), 'nota': request.form.get('nota')})
    return render_template('sobre.html',registros=registros)

@app.route('/filmes/<propriedade>')
def filmes(propriedade):
    if propriedade == 'populares':
        url="https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=17f02c1520cd11a5f8ace7b980a23fab"
    elif propriedade == 'kids':
        url="https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=17f02c1520cd11a5f8ace7b980a23fab"

    resposta=urllib.request.urlopen(url)
    dados=resposta.read()
    jsondata=json.loads(dados)
    return render_template("filmes.html",filmes=jsondata['results']) 

@app.route('/cursos')
def lista_cursos():
    return render_template("cursos.html",cursos=cursos.query.all())

@app.route('/cursos/add',methods=['GET','POST'])
def add_cursos():
    nome=request.form.get('nomecurso')
    descricao=request.form.get('descricao')
    ch=request.form.get('cargahoraria')
    if request.method=='POST':
        if not nome or not descricao or not ch:
            flash("Preencha todos os campos","error")
        else:
            curso=cursos(nome,descricao,ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))
    return render_template("add_cursos.html")

@app.route('/<int:id>/atualiza_curso',methods=['GET','POST'])
def atualiza_curso(id):
    curso=cursos.query.filter_by(id=id).first()
    if request.method=='POST':
        nome=request.form['nomecurso']
        descricao=request.form['descricao']
        ch=request.form['cargahoraria']

        cursos.query.filter_by(id=id).update({'nome':nome,'descricao':descricao,'ch':ch})
        db.session.commit()
        return redirect(url_for('lista_cursos'))



    return render_template ('atualiza_curso.html',curso=curso)

@app.route('/<int:id>/excluir_curso')
def exclui_curso(id):
    curso=cursos.query.filter_by(id=id).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('lista_cursos'))


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)