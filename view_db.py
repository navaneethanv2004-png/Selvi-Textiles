from pymongo import MongoClient

def view_database():
    try:
        # Connect to local MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["selvi_textiles"]
        contacts = db["contacts"]
        inquiries = db["inquiries"]
        
        print("="*60)
        print("                 SELVI TEXTILES DATABASE               ")
        print("="*60)
        
        print("\n[✔] 1. INQUIRIES & QUOTE REQUESTS:")
        print("-" * 60)
        inquiry_data = list(inquiries.find())
        if not inquiry_data:
            print("   (No inquiries found.)")
        else:
            for item in inquiry_data:
                print(f"👉 Date: {item.get('submitted_at')}")
                print(f"   Name: {item.get('name')}")
                print(f"   Phone: {item.get('phone')}")
                print(f"   Product: {item.get('product')}")
                print(f"   Quantity: {item.get('quantity')}")
                print(f"   Message: {item.get('message')}")
                print("-" * 30)
                
        print("\n[✔] 2. CONTACT MESSAGES:")
        print("-" * 60)
        contact_data = list(contacts.find())
        if not contact_data:
            print("   (No contact messages found.)")
        else:
            for item in contact_data:
                print(f"👉 Date: {item.get('submitted_at')}")
                print(f"   Name: {item.get('name')}")
                print(f"   Email: {item.get('email')}")
                print(f"   Subject: {item.get('subject')}")
                print(f"   Message: {item.get('message')}")
                print("-" * 30)

        print("="*60)
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

if __name__ == '__main__':
    view_database()
