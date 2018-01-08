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
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    posts = db.relationship('Posts', backref='owner')

    def __init__(self, username, password)
        self.username = username
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


@app.route('/blog', methods=['POST','GET'])
def index():
    posts = []
    post_id = request.args.get('id')

    if post_id:
        posts = Posts.query.filter_by(id=post_id).all()
        return render_template('blog-posts.html', posts=posts,
        post_id = post_id)
    else:
        posts = Posts.query.all()
        return render_template('blog-posts.html',posts = posts)
    
@app.route('/newpost', methods=['POST','GET'])
def add_post():

    
    title_error = ""
    blog_post_error = ""


    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_post = request.form['blog-post']
        new_post = Posts(blog_title, blog_post)

        if len(blog_title) == 0:
            title_error = "Please enter a title"

        if len(blog_post) == 0:
            blog_post_error = "Please write a blog post"

        if not title_error and not blog_post_error:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_post.id))

    return render_template('add-post.html', title_error = title_error,
            blog_post_error = blog_post_error)




if __name__ == '__main__':
    app.run()