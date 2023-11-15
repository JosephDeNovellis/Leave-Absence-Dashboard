const mysql = require('mysql');
const credentials = require('./secrets.json');

/**
 * Database Interface Class - Allows creation of a database "object" to interact with the application database
 */
class DB_Interface {

    constructor() { 
        this.con = mysql.createConnection({
            host : credentials.host,
            user : credentials.user,
            password : credentials.password,
            database : credentials.database
        });

        this.con.connect(function(err) {
            if (err) {
                console.error('Error connecting to database: ' + err.message);
                return;
            }
            console.log(`Successfully connected to database: ${credentials.database}`);
        });
    }

    /**
     * Create a database entry for an employee. A unique employee id is automatically generated upon insertion
     * 
     * @param {String} name The employee's full name
     * @param {String} email The employee's email address
     * @param {String} password The employee's password - will be encrypted using MD5 hash
     * @param {Integer} company_id The employee's company id
     * @param {Integer} manager_id The employee's manager id
     */
    add_employee(name, email, password, company_id, manager_id = null) {
        var query = "";

        if (manager_id == null) {
            var query = "INSERT INTO employee (empl_name, empl_email, empl_pwd, company_id) VALUES ('" + name + "', '" + email + "', MD5('" + password + "'), " + company_id + ");";
        } else {
            var query = "INSERT INTO employee (empl_name, empl_email, empl_pwd, company_id, manager_id) VALUES ('" + name + "', '" + email + "',  MD5('" + password + "'), " + company_id + ", " + manager_id + ");";
        }

        this.con.query(query, function (err) {
            if (err) {
                console.error('Error inserting employee data: ' + err.message);
                return;
            }
            console.log("Employee insert successful");
        });
    }

    /**
     * Delete a database entry for an employee
     * 
     * @param {Integer} empl_id The employee's id
     */
    del_employee(empl_id) {
        var query = "DELETE FROM employee WHERE empl_id = " + empl_id + ";";

        this.con.query(query, function (err) {
            if (err) {
                console.error('Error deleting employee data: ' + err.message);
                return;
            }
            console.log("Employee deletion successful");
        });
    }

    /**
     * Retrieves a database entry for an employee
     * 
     * @param {Integer} empl_id The employee's id
     */
    ret_employee(empl_id) {
        // var query = "DELETE FROM employee WHERE empl_id = " + empl_id + ";";

        // this.con.query(query, function (err) {
        //     if (err) {
        //         console.error('Error deleting employee data: ' + err.message);
        //         return;
        //     }
        //     console.log("Employee deletion successful");
        // });
    }
}

module.exports = DB_Interface;