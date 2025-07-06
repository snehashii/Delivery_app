CREATE DATABASE delivery_app;
USE delivery_app;

-- USER & AUTHORIZATION TABLES

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);
CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    page_name VARCHAR(100),
    access_level VARCHAR(50) -- e.g. read, write
);
CREATE TABLE role_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT,
    permission_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (permission_id) REFERENCES permissions(id)
);
CREATE TABLE user_hierarchy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    manager_id INT,
    subordinate_id INT,
    FOREIGN KEY (manager_id) REFERENCES users(id),
    FOREIGN KEY (subordinate_id) REFERENCES users(id)
);

-- DELIVERY SYSTEM TABLES

CREATE TABLE riders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    status ENUM('available', 'busy') DEFAULT 'available',
    verified BOOLEAN DEFAULT FALSE,
    locality VARCHAR(100)
);

CREATE TABLE deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(100),
    rider_id INT,
    status ENUM('assigned', 'in-progress', 'done', 'outsourced'),
    tracking_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rider_id) REFERENCES riders(id)
);

CREATE TABLE third_party_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact_info TEXT,
    areas_covered TEXT
);

CREATE TABLE tracking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    delivery_id INT,
    current_location VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_update TEXT,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(id)
);

CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    quantity_available INT,
    location VARCHAR(100)
);

INSERT INTO roles (name, description) VALUES
('Admin', 'Has full access'),
('Manager', 'Can manage deliveries and riders'),
('Rider', 'Handles delivery tasks');

SELECT * FROM roles;

INSERT INTO users (name, email, password, role_id) VALUES
('Sneha Sharma', 'sneha@example.com', 'admin123', 1),  -- Admin
('Raj Manager', 'raj@example.com', 'manager123', 2),   -- Manager
('Ravi Rider', 'ravi@example.com', 'rider123', 3);     -- Rider

SELECT * FROM users;

INSERT INTO permissions (page_name, access_level) VALUES
('roles', 'read-write'),
('users', 'read-write'),
('deliveries', 'read'),
('riders', 'read-write'),
('inventory', 'read-write');

SELECT * FROM permissions;

-- Assign all permissions to Admin
INSERT INTO role_permissions (role_id, permission_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),

-- Manager has limited access
(2, 2), (2, 3), (2, 4),

-- Rider only reads deliveries
(3, 3);

SELECT * FROM role_permissions;

-- Manager is supervising Rider
INSERT INTO user_hierarchy (manager_id, subordinate_id) VALUES
(5, 6);

INSERT INTO riders (name, phone, status, verified, locality) VALUES
('Ravi Rider', '9998887776', 'available', TRUE, 'South Delhi'),
('Pooja Singh', '8887776665', 'busy', FALSE, 'North Delhi');

INSERT INTO deliveries (order_id, rider_id, status, tracking_id) VALUES
('ORD001', 1, 'assigned', 'TRK001'),
('ORD002', 2, 'in-progress', 'TRK002');

INSERT INTO third_party_services (name, contact_info, areas_covered) VALUES
('DHL Logistics', '9876543210, dhl@example.com', 'Pan India'),
('BlueDart', '9123456789, bluedart@example.com', 'Metro Cities');

INSERT INTO tracking (delivery_id, current_location, status_update) VALUES
(1, 'Warehouse - South Delhi', 'Package picked up'),
(2, 'On the way to destination', 'In transit');

INSERT INTO inventory (item_name, quantity_available, location) VALUES
('T-Shirts', 100, 'Warehouse A'),
('Mobile Phones', 50, 'Warehouse B');

-- Admin: All
INSERT INTO role_permissions (role_id, permission_id) 
SELECT 1, id FROM permissions;

-- Manager: Only Users & Deliveries
INSERT INTO role_permissions (role_id, permission_id)
SELECT 2, id FROM permissions WHERE page_name IN ('Users', 'Deliveries');

-- Rider: Only Tracking
INSERT INTO role_permissions (role_id, permission_id)
SELECT 3, id FROM permissions WHERE page_name = 'Tracking';
