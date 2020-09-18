Bottle Sample App.
=================

### Wath's this?
This is sample web application for Bottle that is python web framework.

### Dependency
This sample application needs python3 libraries below.

+ bottle
+ sqlalchemy
+ mysqlclient
+ jinja2

### Setting Database
This application use Maria DB or MySQL. Please create user and databses for application.

**Scripts to create database and tables (MySQL)**
    
    CREATE DATABASE `book_data`;

    CREATE TABLE `books` (
         `id` INT NOT NULL AUTO_INCREMENT,

         `name` VARCHAR(255),

        `volume` VARCHAR(255),

        `author` VARCHAR(255),

        `publisher` VARCHAR(255),

        `memo` TEXT,

        `create_date` DATETIME NOT NULL DEFAULT NOW(),

        `del` TINYINT(4) NOT NULL DEFAULT '0',

       PRIMARY KEY (`id`));

    CREATE TABLE `book_categories` (
    	`id` INT NOT NULL AUTO_INCREMENT,

	    `code` VARCHAR(255),

	    `name` VARCHAR(255),

	PRIMARY KEY (`id`));

    CREATE USER 'bookuser'@'localhost' IDENTIFIED BY 'password';

    GRANT ALL PRIVILEGES ON book_data . * TO ‘bookuser’@‘localhost';