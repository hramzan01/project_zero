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
'''
@app.route("/")
def home():
    return render_template("index.html", content="Testing", x=4)

@app.route("/")
def home():
    return render_template("index.html", content={"a":2, "b":"hello"})
'''


#Creating a html Base Template
'''
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_2.html")


if __name__ == "__main__":
    app.run(debug=True)
'''


#POST & GET form data
'''
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index_2.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
'''

#Setting up a temporary session to store username and login
'''
from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # This makes the session permanent
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
'''