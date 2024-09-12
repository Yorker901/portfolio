from flask import Flask, render_template, request, redirect, flash
from elasticsearch import Elasticsearch
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

# Elasticsearch configuration
# ELASTIC_CLOUD_ID = "ac668387facb455d9201540f7bcdccf3:dXMtY2VudHJhbDEuZ2NwbG91ZC5lcy5pbyQzOThkNTRjMzM2ZWU0NDBjOTBlYzNlY2JiMGI3NDFkYyRkODQ4MTUwNjFjNTQ0MGIwOGJhNzUwMTBkNWMzNzBiZQ=="
# ELASTIC_API_KEY = "bDMyb29aRUJmbEtlQzJiSDlEc0M6U3h1Q2t2UEpUc3lxYnBnWUdXaWl0QQ=="

# Connect to Elasticsearch
es = Elasticsearch(
    cloud_id="ac668387facb455d9201540f7bcdccf3:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDM5OGQ1NGMzMzZlZTQ0MGM5MGVjM2VjYmIwYjc0MWRjJGQ4NDgxNTA2MWM1NDQwYjA4YmE3NTAxMGQ1YzM3MGJl",
    api_key="NG4yOTVwRUJmbEtlQzJiSFgwWHI6eW1lMzU1eHZSWHlsWTc1S2N3REV6dw=="
)



# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle contact form submissions
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Use email as the unique identifier
    doc_id = email

    # Create a document to index into Elasticsearch
    doc = {
        'name': name,
        'email': email,
        'message': message,
        'created_at': datetime.utcnow().isoformat()  # Use 'now' for the current timestamp
    }

    # Index the document into the 'form_info' index
    try:
        es.index(index="form_info", id=doc_id, document=doc)
        flash('Message sent successfully!')
    except Exception as e:
        flash('An error occurred while sending the message.')
        print(f"Error: {e}")

    return redirect('/')

# Route to view all contacts (for testing purposes)
@app.route('/contacts')
def view_contacts():
    try:
        # Fetch all documents from the 'form_info' index
        response = es.search(index="form_info", query={"match_all": {}})
        contacts = [hit['_source'] for hit in response['hits']['hits']]
        return render_template('contacts.html', contacts=contacts)
    except Exception as e:
        flash('An error occurred while fetching contacts.')
        print(f"Error: {e}")
        return redirect('/')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

