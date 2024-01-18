import json
from datetime import date

import requests

from app import app, session, request, render_template


@app.route('/pos')
def pos_index():
    return render_template("pos.html")


@app.route('/pos/create', methods=['post'])
def createPos():
    global current_sale_detail, current_sale, html
    grand_total = 0
    start_html = (
        "<strong>សរុប: {grand_total}</strong>\n"
        "បានទទួលប្រាក់: <code>{received_amount}</code>\n"
        "📆 <code>{date}</code>\n"
        "<strong>=======================</strong>\n"
    )
    try:
        received_amount = request.form.get('received_amount')
        selected_item = request.form.get('selected_item')
        selected_item_obj = json.loads(selected_item)
        # Insert Data to sale
        result = conn.execute(
            text(f"INSERT INTO sale (date, customer_id, received_amount) VALUES ('2023-12-16', 1, {received_amount})"))
        sale_id = result.lastrowid

        # Insert Data to sale_detail
        for item in selected_item_obj:
            pro_id = item['id']
            qty = item['qty']
            cost = item['cost']
            price = item['price']

            conn.execute(text(f"""
                                    INSERT INTO sale_detail (sale_id, product_id, qty ,cost, price) 
                                    VALUES ({sale_id}, {pro_id}, {qty}, {cost}, {price})
                                    """))
            conn.commit()

            current_sale = conn.execute(text(f"SELECT * From sale where id = {sale_id}"))
            current_sale_detail = conn.execute(text(
                f"SELECT sale_detail.*, product.name From sale_detail join product on sale_detail.product_id = product.id where sale_id = {sale_id}"))
            conn.commit()

        last_sale = []
        last_sale_detail_obj = []
        num = 0
        for sale_detail in current_sale_detail:
            last_sale_detail_obj.append(
                {
                    'id': sale_detail.id,
                    'product_id': sale_detail.product_id,
                    'product_name': sale_detail.name,
                    'qty': sale_detail.qty,
                    'cost': sale_detail.cost,
                    'price': sale_detail.price,

                }
            )
            num = num + 1
            start_html += f"<code>{num}. {sale_detail.name} {sale_detail.qty}x{sale_detail.price}= {(sale_detail.qty*sale_detail.price)}$</code>\n"
            grand_total += sale_detail.qty*sale_detail.price

        for sale in current_sale:
            last_sale.append(
                {
                    'id': sale.id,
                    'date': sale.date,
                    'customer_id': sale.customer_id,
                    'received_amount': sale.received_amount,
                    'sale_detail': last_sale_detail_obj
                }
            )
            html = start_html.format(
                grand_total=f'{grand_total}$',
                received_amount=received_amount + '$',
                date=date.today()
                ,
            )

        html = requests.utils.quote(html)

        # Send notification to the request leave employee
        bot_token = "6470887996:AAFTkG2tb3LqagB5J9w3lqz4tja6sdwF32k"
        chat_id = "-1002119315723"
        config_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={html}&parse_mode=HTML"
        res = requests.get(config_url)

        return last_sale

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

        return {'error': f"{e}"}, 201
