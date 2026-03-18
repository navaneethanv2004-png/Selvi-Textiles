from flask import Flask, render_template, request, redirect, flash, url_for
from pymongo import MongoClient
import datetime

app = Flask(__name__)
app.secret_key = 'selvi_textiles_secret_key'

try:
    # Connect to local MongoDB instance
    client = MongoClient("mongodb://localhost:27017/")
    db = client["selvi_textiles"]
    contacts_collection = db["contacts"]
    inquiries_collection = db["inquiries"]
except Exception as e:
    print("Could not connect to MongoDB:", e)

# Dummy product data
PRODUCTS = [
    {
        "id": 1, 
        "name": "Medical Bandage", 
        "description": "High-quality, durable medical compression bandages for effective wound care and support.", 
        "image": "/static/images/product_1.jpg"
    },
    {
        "id": 2, 
        "name": "Cotton Rolls", 
        "description": "100% pure surgical grade absorbent cotton rolls for hospital, clinical, and personal use.", 
        "image": "/static/images/product_2.jpg"
    },
    {
        "id": 3, 
        "name": "Roller Bandage", 
        "description": "Sterile, non-fraying, and flexible roller bandages ensuring secure and comfortable dressing.", 
        "image": "/static/images/product_3.jpg"
    },
    {
        "id": 4, 
        "name": "Gamjee Roll", 
        "description": "Premium absorbent gauze roll, highly breathable and suitable for various medical applications.", 
        "image": "/static/images/product_4.jpg"
    },
    {
        "id": 5, 
        "name": "Gauze Swab", 
        "description": "Medical-grade sterile gauze swabs designed for precision clinical procedures and hygiene.", 
        "image": "/static/images/gauze_swab.png"
    },
    {
        "id": 6, 
        "name": "Surgical Masks", 
        "description": "3-ply protective medical masks designed for daily clinic use and preventing airborne contamination.", 
        "image": "/static/images/product_6.jpeg"
    },
    {
        "id": 7, 
        "name": "Dressing Pad | Mopping Pad", 
        "description": "Premium absorbent sterile dressing and mopping pads for effective wound care, surgical procedures, and optimal medical hygiene.", 
        "image": "/static/images/product_7.jpg"
    },
    {
        "id": 8, 
        "name": "Surgical Gown", 
        "description": "Standard sterile surgical gown for professional use in operating rooms, providing a high level of fluid resistance and comfort.", 
        "image": "/static/images/product_8.jpg"
    },
    {
        "id": 9, 
        "name": "Surgical Cap", 
        "description": "Lightweight and breathable medical surgical cap designed for full hair coverage and hygiene in clinical environments.", 
        "image": "/static/images/product_9.jpg"
    },
    {
        "id": 10, 
        "name": "Medical Nitrile Gloves", 
        "description": "Durable and puncture-resistant medical-grade nitrile gloves, providing superior protection and tactile sensitivity for clinical use.", 
        "image": "/static/images/product_10.jpg"
    }
]

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/products')
def products():
    return render_template('products.html', title='Our Products', products=PRODUCTS)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        # Store in DB
        contact_data = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "submitted_at": datetime.datetime.now()
        }
        try:
            contacts_collection.insert_one(contact_data)
            flash(f"Thank you, {name}. Your message has been saved in our database and sent to our team.", "success")
        except Exception as e:
            flash("An error occurred while saving your message. Please try again later.", "error")
            print("DB Error:", e)
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us')

@app.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    product_name = request.args.get('product', '')
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        product = request.form.get('product')
        quantity = request.form.get('quantity')
        message = request.form.get('message')
        # Store in DB
        inquiry_data = {
            "name": name,
            "phone": phone,
            "product": product,
            "quantity": quantity,
            "message": message,
            "submitted_at": datetime.datetime.now()
        }
        try:
            inquiries_collection.insert_one(inquiry_data)
            flash(f"Your quote request for {product} has been securely saved to our MongoDB database! We will contact you soon.", "success")
        except Exception as e:
            flash("An error occurred while submitting your quote request.", "error")
            print("DB Error:", e)
        return redirect(url_for('products'))
    return render_template('inquiry.html', title='Request Quote', product_name=product_name, products=PRODUCTS)

@app.route('/admin')
def admin():
    try:
        contacts = list(contacts_collection.find().sort("submitted_at", -1))
        inquiries = list(inquiries_collection.find().sort("submitted_at", -1))
    except Exception as e:
        contacts = []
        inquiries = []
        flash("Could not fetch data from MongoDB.", "error")
        print("Fetch Error:", e)
    return render_template('admin.html', title='Admin Dashboard', contacts=contacts, inquiries=inquiries)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
