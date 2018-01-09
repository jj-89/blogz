from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '7v5XIQL9aFad7d'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Posts', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Posts(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - Validate registration

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/blog')
        else:
            flash("User already exists",'error')


    return render_template('register.html')

@app.route('/login', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/blog')
        else:
            flash("Email and password do not match, or the user does not exist", 'error') 

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

@app.route('/blog', methods=['POST','GET'])
def index():
    logged = True

    owner = User.query.filter_by(email=session['email']).first()

    posts = []
    post_id = request.args.get('id')

    if post_id:
        posts = Posts.query.filter_by(id=post_id).all()
        return render_template('blog-posts.html',title = 'Blogz!', posts=posts,
        post_id = post_id,logged=logged)
    else:
        posts = Posts.query.filter_by(owner=owner).all()
        return render_template('blog-posts.html',title = 'Blogz!',posts = posts,logged=logged,owner=owner)
    
@app.route('/newpost', methods=['POST','GET'])
def add_post():
    logged = True

    title_error = ""
    blog_post_error = ""


    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_post = request.form['blog-post']
        owner = User.query.filter_by(email=session['email']).first()
        new_post = Posts(blog_title, blog_post,owner)

        if len(blog_title) == 0:
            title_error = "Please enter a title"

        if len(blog_post) == 0:
            blog_post_error = "Please write a blog post"

        if not title_error and not blog_post_error:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_post.id))

    return render_template('add-post.html', title_error = title_error,
            blog_post_error = blog_post_error, logged=logged)




if __name__ == '__main__':
    app.run()