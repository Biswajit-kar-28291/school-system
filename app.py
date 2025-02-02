from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Dummy users with roles (Replace with a database in production)
users = {
    "admin": ("admin123", "admin"),
    "school": ("school123", "school"),
    "parent": ("parent123", "parent"),
    "student": ("student123", "student")
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        
        # Check if user exists and password is correct
        if username in users and users[username][0] == password:
            correct_role = users[username][1]  # Fetch expected role
            
            if role.lower() == correct_role:  # Check if selected role matches expected role
                session["user"] = username
                session["role"] = role
                return redirect(url_for("dashboard"))
            else:
                return render_template("login.html", error="Invalid role for this user!")
        
        return render_template("login.html", error="Invalid credentials!")
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "role" not in session:
        return redirect(url_for("login"))
    
    role = session["role"]
    return render_template("dashboard.html", role=role)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
