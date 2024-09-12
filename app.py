from flask import Flask, render_template, request, redirect, flash
from elasticsearch import Elasticsearch
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file for local development
if os.getenv('RENDER') is None:  # Assume 'RENDER' env variable is set on Render platform
    load_dotenv()
    
# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Connect to Elasticsearch using environment variables
es = Elasticsearch(
    cloud_id=os.environ.get('ELASTIC_CLOUD_ID'),
    api_key=os.environ.get('ELASTIC_API_KEY')
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
