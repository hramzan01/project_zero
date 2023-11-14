#Creating basic webpage

'''
from flask import Flask

app = Flask(__name__)

# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
	return "Hello! this is the main page <h1>HELLO</h1>" 

if __name__ == "__main__":
    app.run()
'''


#Dynamic URL's

'''
from flask import Flask

app = Flask(__name__)

# Defining the home page of our site
@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

if __name__ == "__main__":
    app.run()
'''

#Redirects
'''
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/admin")
def admin():
	return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
'''

#Redirecting continued
'''
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
	return "Hello! This is the home page <h1>HELLO</h1>"

@app.route("/<name>")
def user(name):
	return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))

if __name__ == "__main__":
	app.run()
'''

# Rendering HTML
'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
	app.run()
'''

#Dynamic HTML
'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content="Something random to test the dynamic variable")

if __name__ == "__main__":
	app.run()
'''

#Templates continued
#You can place python expressions inside html with{% %}.

'''
Passing Multiple Values
Just a quick note here to let you know that you can pass multiple values to your HTML files by defining more keyword arguments in your render_template function or by passing in things like dicts or lists.
'''

#@app.route("/")
#def home():
#    return render_template("index.html", content="Testing", x=4)

#@app.route("/")
#def home():
#    return render_template("index.html", content={"a":2, "b":"hello"})

