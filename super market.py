import smtplib
from email.message import EmailMessage
from product_data import products  # Assuming products are imported from product_data.py

def show_products(products):
    for category, product_list in products.items():
        print(f"Products available for {category}:")
        for idx, product in enumerate(product_list, start=1):
            print(f"{idx}. {product['name']} - ${product['price']} (Stock: {product['stock']})")
        print()  # Add a blank line between categories

def select_product(products, category, index):
    if category in products and 0 <= index < len(products[category]):
        selected_product = products[category][index]
        if selected_product['stock'] > 0:
            print(f"You have selected: {selected_product['name']} - ${selected_product['price']}")
            return selected_product
        else:
            print("Sorry, this product is out of stock.")
    else:
        print("Invalid selection.")

def calculate_bill(selected_products):
    total = 0.0
    for product in selected_products:
        total += product['price']
    
    # Calculate GST (assume 18%)
    gst_amount = total * 0.18
    total_with_gst = total + gst_amount
    
    return total_with_gst

def send_email(customer_email, bill_amount):
    # Construct email message
    msg = EmailMessage()
    msg.set_content(f"Your total bill amount is: ${bill_amount:.2f} (including GST)")
    msg['Subject'] = 'Your Supermarket Bill'
    msg['From'] = 'palanisamyhema4@gmail.com'
    msg['To'] = customer_email
    
    # Send email (simulated)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.login('palanisamyhema4@gmail.com', 'jsiu mvxj oyyk mady')
            smtp.send_message(msg)
        print(f"Bill sent to {customer_email}.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main program
if __name__ == "__main__":
    show_products(products)
    
    selected_products = []
    while True:
        try:
            category = input("Enter the category you want to explore (kids/girls/boys), or 'done' to finish: ").lower()
            
            if category == 'done':
                break
            
            if category not in products:
                print("Invalid category. Please enter 'kids', 'girls', or 'boys'.")
                continue
            
            show_products({category: products[category]})
            index = int(input(f"Select a product number (1-{len(products[category])}): ")) - 1
            
            if 0 <= index < len(products[category]):
                selected_products.append(products[category][index])
                print(f"Added {products[category][index]['name']} to your cart.")
            else:
                print("Invalid product number. Please try again.")
        
        except ValueError:
            print("Invalid input. Please enter a valid product number.")
    
    if selected_products:
        total_bill = calculate_bill(selected_products)
        print(f"Total bill amount (including GST): ${total_bill:.2f}")
        
        customer_email = input("Enter your email address to receive the bill: ")
        send_email(customer_email, total_bill)
    else:
        print("No products selected. Exiting.")
