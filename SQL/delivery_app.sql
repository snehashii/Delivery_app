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
-- Insert sample roles

INSERT INTO roles (name, description) VALUES 
('Admin', 'Full access'),
('Manager', 'Can manage deliveries'),
('Rider', 'Handles delivery tasks');

-- Insert a test user
INSERT INTO users (name, email, password, role_id) 
VALUES ('Sneha Sharma', 'sneha@example.com', 'hashed_password_here', 2);

