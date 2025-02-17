from flask import render_template
from app.main import main
from app.main.models import Inventory


@main.route('/', methods=['GET'])
def home():
    inventory_list = Inventory.query.all()

    return render_template('show_inventory.html', inventory=inventory_list, page_title='Home')