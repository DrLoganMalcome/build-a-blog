from flask import Flask, request, redirect, render_template
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import cgi
import blogMethods

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogapp:password@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(124))
    text = db.Column(db.String(512))

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return self.title

@app.route("/add", methods=['POST'])
def add_post():
    # look inside the request to figure out what the user typed
    post_title = request.form['title']
    post_text = request.form['text']
    # if the user typed nothing at all, redirect and tell them the error
    if (not post_title) or (post_title.strip() == ""):
        error = "Please specify a title for your post."
        return redirect("/?error=" + error)

    post = Post(post_title,post_text)
    db.session.add(post)
    db.session.commit()
    return redirect('/')


@app.route("/")
def index():
    blog_posts= Post.query.all()
    return render_template('blogPosts.html', blog_posts=blog_posts)

@app.route("/post")
def blog():
    blog_post= Post.query.filter_by(id=request.args['id'])
    return render_template('post.html', blog_post = blog_post)

@app.route("/new")
def new():
    return render_template('newPost.html')

if __name__ == "__main__":
    app.run()