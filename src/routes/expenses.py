from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models import Expense, Group, Debt, db
from sqlalchemy.orm import joinedload

bp = Blueprint('expenses', __name__)

@bp.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    groups = current_user.groups
    
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        group_id = request.form['group']
        split_type = request.form['split_type']
        
        # Create expense
        expense = Expense(
            description=description, 
            amount=amount, 
            payer=current_user, 
            group_id=group_id
        )
        
        db.session.add(expense)
        
        # Split logic
        group = Group.query.get(group_id)
        members = group.members
        
        if split_type == 'equal':
            split_amount = amount / len(members)
            for member in members:
                if member != current_user:
                    debt = Debt(
                        amount=split_amount, 
                        debtor=member, 
                        expense=expense
                    )
                    db.session.add(debt)
        
        db.session.commit()
        flash('Expense added successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('expenses/add.html', groups=groups)

@bp.route('/expenses/settle', methods=['GET', 'POST'])
@login_required
def settle_expenses():
    if request.method == 'POST':
        # Logic for settling debts
        pass
    
    # Get all unsettled debts
    unsettled_debts = Debt.query.filter_by(
        debtor=current_user, 
        is_settled=False
    ).options(
        joinedload(Debt.expense)
    ).all()
    
    return render_template('expenses/settle.html', debts=unsettled_debts)

@bp.route('/expenses/history')
@login_required
def expense_history():
    expenses = Expense.query.filter_by(payer=current_user).all()
    return render_template('expenses/history.html', expenses=expenses)
