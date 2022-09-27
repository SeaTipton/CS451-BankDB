from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Fund
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        fund = request.form.get('fund')

        if len(fund) < 1:
            flash('fund is too short!', category='error')
        else:
            new_fund = Fund(data=fund, user_id=current_user.id)
            db.session.add(new_fund)
            db.session.commit()
            flash('Fund added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-fund', methods=['POST'])
def delete_fund():
    fund = json.loads(request.data)
    fundId = fund['fundId']
    fund = Fund.query.get(fundId)
    if fund:
        if fund.user_id == current_user.id:
            db.session.delete(fund)
            db.session.commit()

    return jsonify({})
