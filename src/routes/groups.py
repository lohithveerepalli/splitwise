from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models import Group, User, db

bp = Blueprint('groups', __name__)

@bp.route('/groups')
@login_required
def list_groups():
    groups = current_user.groups
    return render_template('groups/list.html', groups=groups)

@bp.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        # Create new group
        new_group = Group(name=name, description=description)
        new_group.members.append(current_user)
        
        db.session.add(new_group)
        db.session.commit()
        
        flash('Group created successfully!')
        return redirect(url_for('groups.list_groups'))
    
    return render_template('groups/create.html')

@bp.route('/groups/<int:group_id>/add_member', methods=['GET', 'POST'])
@login_required
def add_member(group_id):
    group = Group.query.get_or_404(group_id)
    
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        
        if user:
            if user in group.members:
                flash('User is already a member of this group')
            else:
                group.members.append(user)
                db.session.commit()
                flash('Member added successfully!')
        else:
            flash('User not found')
        
        return redirect(url_for('groups.group_details', group_id=group_id))
    
    return render_template('groups/add_member.html', group=group)

@bp.route('/groups/<int:group_id>')
@login_required
def group_details(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('groups/details.html', group=group)
