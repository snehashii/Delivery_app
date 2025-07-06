from extensions import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role')

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(100))
    access_level = db.Column(db.String(50))

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    role = db.relationship('Role')
    permission = db.relationship('Permission')

class UserHierarchy(db.Model):
    __tablename__ = 'user_hierarchy'
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subordinate_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Rider(db.Model):
    __tablename__ = 'riders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    status = db.Column(db.Enum('available', 'busy'), default='available')
    verified = db.Column(db.Boolean, default=False)
    locality = db.Column(db.String(100))

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100))
    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id'), nullable=True)
    status = db.Column(db.Enum('assigned', 'in-progress', 'done', 'outsourced'))
    tracking_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class ThirdPartyService(db.Model):
    __tablename__ = 'third_party_services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact_info = db.Column(db.Text)
    areas_covered = db.Column(db.Text)

class Tracking(db.Model):
    __tablename__ = 'tracking'
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'))
    current_location = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status_update = db.Column(db.Text)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    quantity_available = db.Column(db.Integer)
    location = db.Column(db.String(100))
