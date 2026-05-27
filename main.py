# Imports------------------

import pandas as pd
import requests
import mysql.connector
import datetime

from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)


# Function--------------------

def fetch_and_store():

    # FETCH DATA FROM API
    url = "https://fakestoreapi.com/products"

    response = requests.get(url)

    data = response.json()

    # CONVERT TO DATAFRAME
    df = pd.DataFrame(data)

    # CONVERT RATING DICTIONARY TO FLOAT
    df['rating'] = df['rating'].apply(lambda x: x['rate'])

    # SQL CONNECTION
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nihal@123",
        database="product"
    )

    mycursor = con.cursor()

    # INSERT DATA INTO SQL
    for i, j in df.iterrows():

        id = j['id']
        title = j['title']
        price = j['price']
        category = j['category']
        image = j['image']
        fetched_time = datetime.datetime.now()

        mycursor.execute("""

            INSERT IGNORE INTO product_info
            (id, title, category, price, fetched_time)

            VALUES (%s, %s, %s, %s, %s)

        """, (id, title, category, price, fetched_time))

        con.commit()

        query = """

          SELECT price
          FROM product_info
          WHERE title = %s
          ORDER BY fetched_time DESC
          LIMIT 2

        """

        mycursor.execute(query, (title,))

        result = mycursor.fetchall()

        if len(result) >= 2:

            latest_price = float(result[0][0])
            old_price = float(result[1][0])

        if latest_price < old_price:

            alert = "Price Dropped"

        elif latest_price > old_price:

            alert = "Price Increased"

        else:

            alert = "No Price Change"

        print("\n======================")
        print("Product :", title)
        print("Old Price :", old_price)
        print("Latest Price :", latest_price)
        print("Alert :", alert)
        print("======================")

    mycursor.close()
    con.close()

# ========================== SCHEDULER ==========================

scheduler = BackgroundScheduler()

# AUTO FETCH EVERY 1 HOUR
scheduler.add_job(fetch_and_store, 'interval', hours=1)

scheduler.start()

# ========================== HOME PAGE ==========================

@app.route('/')
def page():

    return render_template("page.html")


# ========================== CHECK BUTTON ROUTE ==========================

@app.route('/check_price')
def check_price():

    fetch_and_store()




#Product Image
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    data = response.json()
    product_image = ""
    product = request.args.get('product')
    for item in data:

        if item['title'] == product:
            product_image = item['image']
            break




    #Product description
    product_descriptions = {
        "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops":
            "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",

        "Mens Casual Premium Slim Fit T-Shirts ":
            "Slim-fitting style, contrast raglan long sleeve, three-button henley placket, light weight & soft fabric for breathable and comfortable wearing.",

        "Mens Cotton Jacket":
            "great outerwear jackets for Spring/Autumn/Winter, suitable for many occasions, such as working, hiking, camping, mountain/rock climbing, cycling, traveling or other outdoors.",

        "Mens Casual Slim Fit":
            "The color could be slightly different between on the screen and in practice.",

        "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet":
            "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl.",

        "Solid Gold Petite Micropave ":
            "Satisfaction Guaranteed. Return or exchange any order within 30 days.",

        "White Gold Plated Princess":
            "Classic Created Wedding Engagement Solitaire Diamond Promise Ring for Her.",

        "Pierced Owl Rose Gold Plated Stainless Steel Double":
            "Rose Gold Plated Double Flared Tunnel Plug Earrings. Made of 316L Stainless Steel",

        "WD 2TB Elements Portable External Hard Drive - USB 3.0 ":
            "USB 3.0 and USB 2.0 Compatibility Fast data transfers Improve PC Performance High Capacity.",

        "SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s":
            "Easy upgrade for faster boot up, shutdown, application load and response.",

        "Silicon Power 256GB SSD 3D NAND A55 SLC Cache Performance Boost SATA III 2.5":
            "3D NAND flash are applied to deliver high transfer speeds.",

        "WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive":
            "Expand your PS4 gaming experience, Play anywhere Fast and easy, setup.",

        "Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin":
            "21.5 inches Full HD widescreen IPS display and Radeon FreeSync technology.",

        "Samsung 49-Inch CHG90 144Hz Curved Gaming Monitor (LC49HG90DMNXZA) – Super Ultrawide Screen QLED ":
            "49 INCH SUPER ULTRAWIDE CURVED GAMING MONITOR with dual 27 inch screen side by side.",

        "BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats":
            "Note:The Jackets is US standard size, Please choose size as your usual wear.",

        "Lock and Love Women's Removable Hooded Faux Leather Moto Biker Jacket":
            "Faux leather material for style and comfort.",

        "Rain Jacket Women Windbreaker Striped Climbing Raincoats":
            "Lightweight perfect for trip or casual wear.",

        "MBJ Women's Solid Short Sleeve Boat Neck V ":
            "Lightweight fabric with great stretch for comfort.",

        "Opna Women's Short Sleeve Moisture":
            "Lightweight, roomy and highly breathable with moisture wicking fabric.",

        "DANVOUY Womens T Shirt Casual Cotton Short":
            "Casual, Short Sleeve, Letter Print, V-Neck, Fashion Tees."
    }
    description = product_descriptions.get(product, "No Description Available")


    con = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="nihal@123",
        database="product"
    )

    mycursor = con.cursor()

    query = """

        SELECT price
        FROM product_info
        WHERE title = %s
        ORDER BY fetched_time DESC
        LIMIT 2

    """

    mycursor.execute(query, (product,))

    result = mycursor.fetchall()

    latest_price = float(result[0][0])

    old_price = float(result[1][0])

    if latest_price < old_price:

        alert = "Price Dropped"

    elif latest_price > old_price:

        alert = "Price Increased"

    else:

        alert = "No Price Change"


    return render_template(

        "page.html",

        product=product,
        old_price=old_price,
        latest_price=latest_price,
        alert=alert,
        description = description,
        image = product_image

    )


# ========================== RUN APP ==========================

if __name__ == '__main__':

    app.run(debug=True)
