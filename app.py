from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'hehe'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",  # Make sure this is the correct password
    database="portfolio"  # Replace with your database name
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')  # Ensure this is the correct path to your HTML file

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Save the form data to the database
    cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
    db.commit()
    
    flash('Message sent successfully!')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
