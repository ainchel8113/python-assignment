from flask import Flask, request, redirect, render_template
import random
import string

app = Flask(__name__)

# Store mapping: short_code -> original_url
url_map = {}

def generate_short_code(length=6):
    """Generate a random short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["long_url"]

        # Generate unique short code
        code = generate_short_code()
        while code in url_map:
            code = generate_short_code()

        # Store the mapping
        url_map[code] = long_url

        short_url = request.host_url + code
        return render_template("index.html", short_url=short_url)

    return render_template("index.html", short_url=None)

@app.route("/<code>")
def redirect_to_url(code):
    if code in url_map:
        return redirect(url_map[code])
    return "Invalid short URL", 404

if __name__ == "__main__":
    app.run(debug=True)
