const mysql =  require('mysql');
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
     * @param {Integer} company_name The employee's company name
     * @param {String} manager_email The employee's manager's email
     */
    add_employee(email, name, password, company_name, manager_email = null) {
        var query = "";

        if (manager_email == null) {
            query = "INSERT INTO employee (empl_email, empl_name, empl_pwd, company_name) VALUES ('" + email + "', '" + name + "',  MD5('" + password + "'), '" + company_name + "');";
        } else {
            query = "INSERT INTO employee (empl_email, empl_name, empl_pwd, company_name, manager_email) VALUES ('" + email + "', '" + name + "',  MD5('" + password + "'), '" + company_name + "', '" + manager_email + "');";
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
     * Delete a database entry for an employee, using either their employee email address
     * 
     * @param {String} email The email of the employee to be deleted
     */
    del_employee(email) {
        this.#con.query("DELETE FROM employee WHERE empl_email = '" + email + "';", function (err) {
            if (err) {
                console.error('Error deleting employee data: ' + err.message);
                return;
            }
            console.log("Employee deletion successful");
        });
    }


    /**
     * Retrieves a database entry for an employee, using their employee email address
     * 
     * @param {String} email The email of the employee  
     */
    ret_employee(email) {
        return new Promise((resolve, reject) => {
            this.#con.query("SELECT * FROM employee WHERE empl_email = '" + email + "';", function (err, result) {
                if (err) {
                    return reject(err);
                }
                return resolve(result);
            });
        });   
    }


    /**
     * Retrieves a database entry for an employee, using their email address and password
     * 
     * @param {String} email The email of the employee  
     * @param {String} password The password of the employee
     */
    ret_employee(email, password) {
        return new Promise((resolve, reject) => {
            this.#con.query("SELECT * FROM employee WHERE empl_email = '" + email + "' AND empl_pwd = MD5('" + password + "');", function (err, result) {
                if (err) {
                    return reject(err);
                }
                return resolve(result);
            });
        });   
    }


    /**
     * Create a database entry for a company. Company name will be used as the identifier
     * 
     * @param {String} company_name The company's name
     */
    add_company(company_name) {
        this.#con.query("INSERT INTO company (company_name) VALUES ('" + company_name + "');", function (err) {
            if (err) {
                console.error('Error inserting company data: ' + err.message);
                return;
            }
            console.log("Company insert successful");
        });
    }


    /**
     * Delete a database entry for a company, using the company name
     * 
     * @param {String} company_name The name of the company to be deleted
     */
    del_company(company_name) {
        this.#con.query("DELETE FROM company WHERE company_name = '" + company_name + "';", function (err) {
            if (err) {
                console.error('Error deleting company data: ' + err.message);
                return;
            }
            console.log("Employee company successful");
        });
    }


    /**
     * Retrieves a database entry for a company, using the company name
     * 
     * @param {String} company_name The name of the company
     */
    ret_company(company_name) {
        return new Promise((resolve, reject) => {
            this.#con.query("SELECT * FROM company WHERE company_name = '" + company_name + "';", function (err, result) {
                if (err) {
                    return reject(err);
                }
                return resolve(result);
            });
        });   
    }


    /**
     * Create a leave request and store it in the database
     * 
     * @param {String} email The employee's email
     * @param {Date} start_date The start date of the leave request
     * @param {Date} end_date The end date of the leave request - will be the same as req_start_date if the employee only books one day off
     * @param {String} reason The reason for the employee's leave request
     */
    add_leave_request(email, start_date, end_date, reason) {
        var start_date_formnatted = [start_date.getFullYear(), start_date.getMonth() + 1, start_date.getDate()].join('-');
        var end_date_formnatted = [end_date.getFullYear(), end_date.getMonth() + 1, end_date.getDate()].join('-');

        this.#con.query("INSERT INTO time_off_request (empl_email, req_start_date, req_end_date, req_reason) VALUES ('" + email + "', '" + start_date_formnatted + "', '" + end_date_formnatted + "', '" + reason + "');", function (err) {
            if (err) {
                console.error('Error inserting leave request data: ' + err.message);
                return;
            }
            console.log("Leave request insert successful");
        });
    }


    /**
     * Retrieves all leave requests associated with an employee
     * 
     * @param {String} empl_email The email of the employee  
     */
    ret_leave_request(empl_email) {
        return new Promise((resolve, reject) => {
            this.#con.query("SELECT * FROM time_off_request WHERE empl_email = '" + empl_email + "';", function (err, result) {
                if (err) {
                    return reject(err);
                }
                return resolve(result);
            });
        });   
    }


    /**
     * Retrieves all leave requests associated with an manager's subordinates
     * 
     * @param {String} manager_email The email of the manager
     */
    ret_subordinate_leave_requests(manager_email) {
        return new Promise((resolve, reject) => {
            this.#con.query("SELECT t.* FROM leave_absence_db.time_off_request t, leave_absence_db.employee e WHERE e.empl_email = t.empl_email AND e.manager_email = '" + manager_email + "';", function (err, result) {
                if (err) {
                    return reject(err);
                }
                return resolve(result);
            });
        });   
    }


    /**
     * Delete a database entry for a leave request
     * 
     * @param {String} email The email of the request to be deleted
     * @param {Integer} req_id The id of the request to be deleted
     */
    del_leave_request(email, req_id) {
        this.#con.query("DELETE FROM employee WHERE empl_email = '" + email + "' AND req_id = '" + req_id + "';", function (err) {
            if (err) {
                console.error('Error deleting leave request data: ' + err.message);
                return;
            }
            console.log("Leave request deletion successful");
        });
    }


    /**
     * Store data for a work from home day
     * 
     * @param {String} email The employee's email
     * @param {Date} date The date of the work from home day
     */
    add_wfh_day(email, date) {
        var date_formnatted = [date.getFullYear(), date.getMonth() + 1, date.getDate()].join('-');

        this.#con.query("INSERT INTO wfh_day (empl_email, req_date) VALUES ('" + email + "', '" + date_formnatted + "');", function (err) {
            if (err) {
                console.error('Error inserting work from home day data: ' + err.message);
                return;
            }
            console.log("Work from home day insert successful");
        });
    }


    /**
     * Retrieves all work from home days associated with an employee
     * 
     * @param {String} email The email of the employee  
     */
    ret_wfh_day(email) {
        return new Promise((resolve, reject) => {
            this.#con.query("SELECT * FROM wfh_day WHERE empl_email = '" + email + "';", function (err, result) {
                if (err) {
                    return reject(err);
                }
                return resolve(result);
            });
        });   
    }


    /**
     * Delete a database entry for a work from home date
     * 
     * @param {String} email The email of the request to be deleted
     * @param {Date} date The date to be deleted
     */
    del_leave_request(email, date) {
        var date_formnatted = [date.getFullYear(), date.getMonth() + 1, date.getDate()].join('-');

        this.#con.query("DELETE FROM wfh_day WHERE empl_email = '" + email + "' AND wfh_date = '" + date_formnatted + "';", function (err) {
            if (err) {
                console.error('Error deleting work from home day data: ' + err.message);
                return;
            }
            console.log("Work from home day deletion successful");
        });
    }

}

module.exports = DB_Interface;