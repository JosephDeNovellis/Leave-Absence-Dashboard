const mysql = require('mysql');
const credentials = require('./secrets.json');

/**
 * Database Interface Class - Allows creation of a database "object" to interact with the application database
 */
class DB_Interface {

    #con = null;

    /**
     * If a database connection is already established, no new connection will be created
     */
    constructor() { 
        if (this.#con == null) {
            this.#con = mysql.createConnection({
                host : credentials.host,
                user : credentials.user,
                password : credentials.password,
                database : credentials.database
            });

            this.#con.connect(function(err) {
                if (err) {
                    console.error('Error connecting to database: ' + err.message);
                    return;
                }
                console.log(`Successfully connected to database: ${credentials.database}`);
            });
        } else {
            return;
        }
    }

    // Might not need this?
    disconnect() {
        this.#con.end(function(err) {
            if (err) {
                console.error('Error closing connection: ' + err.message);
                return;
            }
            console.log(`Connection closed.`);
        });
    }

    /**
     * Create a database entry for an employee, using their email as an identifier
     * 
     * @param {String} email The employee's email address
     * @param {String} name The employee's full name
     * @param {String} password The employee's password - will be encrypted using MD5 hash
     * @param {Integer} company_id The employee's company id
     * @param {String} manager_email The employee's manager's email
     */
    add_employee(email, name, password, company_id, manager_email = null) {
        var query = "";

        if (manager_email == null) {
            query = "INSERT INTO employee (empl_email, empl_name, empl_pwd, company_id) VALUES ('" + email + "', '" + name + "',  MD5('" + password + "'), " + company_id + ");";
        } else {
            query = "INSERT INTO employee (empl_email, empl_name, empl_pwd, company_id, manager_email) VALUES ('" + email + "', '" + name + "',  MD5('" + password + "'), " + company_id + ", '" + manager_email + "');";
        }
        
        this.#con.query(query, function (err) {
            if (err) {
                console.error('Error inserting employee data: ' + err.message);
                return;
            }
            console.log("Employee insert successful");
        });
    }


    /**
     * Delete a database entry for an employee, using either their employee id or employee email address
     * 
     * @param {String} empl_email The email of the employee to be deleted
     */
    del_employee(empl_email) {
        this.#con.query("DELETE FROM employee WHERE empl_email = '" + empl_email + "';", function (err) {
            if (err) {
                console.error('Error deleting employee data: ' + err.message);
                return;
            }
            console.log("Employee deletion successful");
        });
    }


    /**
     * Retrieves a database entry for an employee, using either their employee id or employee email address
     * 
     * @param {String} empl_email The email of the employee  
     */
    ret_employee(empl_email) {
        return new Promise((resolve, reject) => {
            this.#con.query("SELECT * FROM employee WHERE empl_email = '" + empl_email + "';", function (err, result) {
                if (err) {
                    return reject(err);
                }
                return resolve(result);
            });
        });   
    }

}

module.exports = DB_Interface;