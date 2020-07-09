-- Flask To-Do Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS todos;
-- Add query to drop users table here
DROP TABLE IF EXISTS users;
-- Add query to create users table here
CREATE TABLE users (
  id bigserial PRIMARY KEY,
  email varchar(50) UNIQUE NOT NULL,
  password varchar(200) NOT NULL
);
-- To-Do Items
CREATE TABLE todos (
  id bigserial PRIMARY KEY,
  description varchar(140) NOT NULL,
  completed boolean NOT NULL,
  created_at timestamp with time zone NOT NULL,
  -- Add Foreign Key to users table here
  user_id bigint REFERENCES users(id)
);
