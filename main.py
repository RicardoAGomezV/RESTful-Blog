import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, String, Text
from wtforms import Form,  StringField, SubmitField, validators
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField

app = Flask(__name__)

# Initialise the CKEditor so that we can use it in make_post.html
ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'

# configure the SQLite database, relative to the app instance folder
db = SQLAlchemy(model_class=Base)

# initialize the app with the extension
db.init_app(app)


# Create the  table in the database
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    

# Create the database tables within the app context    
with app.app_context():
    db.create_all()
    

#NOTE: ADDING THE FIRTS DATA TO THE DB 
# new_post = BlogPost(
#     title="Example Post",
#     subtitle='Check out my example',
#     date=datetime.datetime(2023, 7, 18).strftime("%Y, %B, %d"),
#     body='''<p>Just some content</p>

# <p>&quot;Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.&quot;</p>

# <p>&nbsp;</p>

# <p>&nbsp;</p>
# ''',
#     author='Magan Cambell',
#     img_url="https://imgs.search.brave.com/BW__i2u-_aUDX7WcqOc0ZZIrdXUDN73s-jcnwRqSN8k/rs:fit:1024:704:1/g:ce/aHR0cHM6Ly9zdGF0/aWMwMS5ueXQuY29t/L2ltYWdlcy8yMDEx/LzAxLzE0L2FydHMv/MTRNT1ZJTkctc3Bh/bi9NT1ZJTkctanVt/Ym8uanBn"
# )

# second_post = BlogPost(
#     title="Lego is fun",
#     subtitle='Lego is awsome',
#     date=datetime.datetime(2024, 3, 19).strftime("%Y, %B, %d"),
#     body='''<p><strong>Lego</strong> (<a href="https://en.wikipedia.org/wiki/Help:IPA/English">/ˈlɛɡoʊ/</a> <a href="https://en.wikipedia.org/wiki/Help:Pronunciation_respelling_key"><em>LEG-oh</em></a>, <small>Danish:&nbsp;</small><a href="https://en.wikipedia.org/wiki/Help:IPA/Danish">[ˈle̝ːko]</a>;<a href="https://en.wikipedia.org/wiki/Lego#cite_note-1">[1]</a> stylized as <strong>LEGO</strong>) is a line of plastic <a href="https://en.wikipedia.org/wiki/Construction_toy">construction toys</a> that are manufactured by <a href="https://en.wikipedia.org/wiki/The_Lego_Group">the Lego Group</a>, a privately held company based in <a href="https://en.wikipedia.org/wiki/Billund,_Denmark">Billund</a>, <a href="https://en.wikipedia.org/wiki/Denmark">Denmark</a>. Lego consists of variously colored <a href="https://en.wikipedia.org/wiki/Interchangeable_parts">interlocking</a> plastic bricks made of <a href="https://en.wikipedia.org/wiki/Acrylonitrile_butadiene_styrene">acrylonitrile butadiene styrene</a> that accompany an array of <a href="https://en.wikipedia.org/wiki/Gear">gears</a>, figurines called <a href="https://en.wikipedia.org/wiki/Lego_minifigure">minifigures</a>, and various other parts. Lego pieces can be assembled and connected in many ways to construct objects, including vehicles, buildings, and working robots. Anything constructed can be taken apart again, and the pieces reused to make new things.</p>

# <p>The Lego Group began manufacturing the interlocking toy bricks in 1949. <a href="https://en.wikipedia.org/wiki/List_of_Lego_films_and_TV_series">Films</a>, <a href="https://en.wikipedia.org/wiki/List_of_Lego_video_games">games</a> competitions, and eight <a href="https://en.wikipedia.org/wiki/Legoland">Legoland</a> <a href="https://en.wikipedia.org/wiki/Amusement_park">amusement parks</a> have been developed under the brand. As of July&nbsp;2015, 600&nbsp;billion Lego parts had been produced.</p>
# ''',
#     author='Arav Pant',
#     img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Lego_Color_Bricks.jpg/2560px-Lego_Color_Bricks.jpg"
# )    

# third_post = BlogPost(
#     title="Python Trivia",
#     subtitle='Where did the name come from?',
#     date=datetime.datetime(2023, 3, 20).strftime("%Y, %B, %d"),
#     body='''<p><strong>Monty Python</strong> (also collectively known as <strong>the Pythons</strong>) were a British <a href="https://en.wikipedia.org/wiki/Comedy_troupe">comedy troupe</a> formed in 1969 consisting of <a href="https://en.wikipedia.org/wiki/Graham_Chapman">Graham Chapman</a>, <a href="https://en.wikipedia.org/wiki/John_Cleese">John Cleese</a>, <a href="https://en.wikipedia.org/wiki/Terry_Gilliam">Terry Gilliam</a>, <a href="https://en.wikipedia.org/wiki/Eric_Idle">Eric Idle</a>, <a href="https://en.wikipedia.org/wiki/Terry_Jones">Terry Jones</a>, and <a href="https://en.wikipedia.org/wiki/Michael_Palin">Michael Palin</a>. The group came to prominence for the <a href="https://en.wikipedia.org/wiki/Sketch_comedy">sketch comedy</a> series <em><a href="https://en.wikipedia.org/wiki/Monty_Python%27s_Flying_Circus">Monty Python&#39;s Flying Circus</a></em> (1969&ndash;1974). Their work then developed into a larger collection that included live shows, films, albums, books, and musicals; their influence on comedy has been compared to <a href="https://en.wikipedia.org/wiki/The_Beatles">the Beatles</a>&#39; influence on music. Their sketch show has been called &quot;an important moment in the evolution of television comedy&quot;</p>
# ''',
#     author='Jack Bauer',
#     img_url="https://upload.wikimedia.org/wikipedia/commons/4/47/Monty_Python_Live_02-07-14_12_46_43_%2814415411808%29.jpg"
# )    

# with app.app_context():
#     db.session.add(new_post)
#     db.session.add(second_post)
#     db.session.add(third_post)
#     db.session.commit()
        
        
@app.route("/")
def get_all_posts():
    # Get the most recent post
    # orders them by date in descending order, and takes the first result (the most recent).
    most_recent_post = db.session.execute(db.select(BlogPost).order_by(BlogPost.date.desc())).scalars().first()
    
    # Get all posts except the most recent one
    all_posts_except_most_recent = db.session.execute(db.select(BlogPost).where(BlogPost.id != most_recent_post.id).order_by(BlogPost.date.desc())).scalars().all()

    
    # Renders the 'index.html' template and passes the posts
    return render_template('index.html', all_post=all_posts_except_most_recent, most_recent_post=most_recent_post)




# Define a route for displaying a single post, using the post_id parameter to identify the post
@app.route("/post/<post_id>")
def show_post(post_id):
    
    # Retrieve the post from the database using the post_id; if not found, return a 404 error
    post_info = db.get_or_404(BlogPost, post_id)
    
    
    return render_template('post.html', post=post_info)




# Form class for creating a new blog post
class CreatePostForm(FlaskForm):
    
    # Field for the blog post title
    blog_post_title = StringField('Blog Post Title', [validators.Length(min=5, max=35), validators.DataRequired(message="Review is required.")])
    
    # Field for the subtitle of the blog post
    subtitle = StringField('subitle', [validators.Length(min=5, max=35), validators.DataRequired(message="Subtitle is required.")])
    
    # Field for the author's name
    author_name = StringField('Author name', [validators.Length(min=5, max=35), validators.DataRequired(message="Author name is required.")])
    
    # Field for the URL of the blog post's image
    img_url = StringField('Blog Image Url', [validators.Length(min=5), validators.DataRequired(message="A URL for the background image is required."), validators.URL()])
    
    # Field for the body content of the blog post, using CKEditor
    body = CKEditorField("Blog Content", [validators.DataRequired()])   
    # Submit button - Removed for now to prevent accidental form submission
    # submit = SubmitField('Submit')


# Define a route for creating a new post, allowing both GET and POST requests
@app.route("/new_post", methods=['GET', 'POST'])
def new_post():
    # Create an instance of the form for creating a new post
    form = CreatePostForm()
    
    # Check if the form has been submitted and is valid
    if form.validate_on_submit():
        
        # Create a new BlogPost object with data from the form
        new_post = BlogPost(
            title=form.blog_post_title.data,         
            subtitle=form.subtitle.data,             
            date=datetime.datetime.now().strftime("%B %d, %Y"),  
            author=form.author_name.data,           
            img_url=form.img_url.data,              
            body=form.body.data                     
        )
        
        # Add the new post to the database session
        db.session.add(new_post)
        
        # Commit the session to save the new post to the database
        db.session.commit()
        
       
        return redirect(url_for('get_all_posts'))
    
    else:
        
        return render_template('make-post.html', form=form)


# Define a route for editing a post by its ID, allowing both GET and POST requests
@app.route("/edit/<post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    
    # Get the post from the database by its ID; if not found, return a 404 error
    post = db.get_or_404(BlogPost, post_id)
    
    # Create a form pre-populated with the post's existing data
    edit_form = CreatePostForm(
        blog_post_title=post.title,  
        subtitle=post.subtitle,      
        img_url=post.img_url,        
        author_name=post.author,     
        body=post.body               
    )
    
    # Check if the form has been submitted and is valid
    if edit_form.validate_on_submit():
        
        # Update the post's fields with the data from the form
        post.id = post_id                             
        post.title = edit_form.blog_post_title.data  
        post.subtitle = edit_form.subtitle.data       
        post.author = edit_form.author_name.data      
        post.img_url = edit_form.img_url.data         
        post.body = edit_form.body.data               
        
        # Commit the changes to the database
        db.session.commit()
        
        
        return redirect(url_for('get_all_posts'))
    
    else:
        
        return render_template('make-post.html', form=edit_form, edit=True, post=post)




# Route for deleting a post by its ID
@app.route("/delete/<post_id>")
def delete_post(post_id):
    
    # Print the post ID to the console (for debugging purposes)
    print(post_id)
    
    # Get the post from the database by its ID; if not found, return a 404 error
    post = db.get_or_404(BlogPost, post_id)
    
    # Delete the post from the database session
    db.session.delete(post)
    
    
    db.session.commit()
    
    
    return redirect(url_for('get_all_posts'))




if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True, port=5003)