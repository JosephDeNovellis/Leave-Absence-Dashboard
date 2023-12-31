import json
import datetime
import mysql.connector

class DB_Interface:
    """
    Database Interface Class - Allows creation of a database "object" to interact with the application database
    """

    con = None
    db_cursor = None

    def __init__(self):
        """
        If a database connection is already established, no new connection will be created
        """
        if (DB_Interface.con == None):
            file = open('secrets.json')
            credentials = json.load(file)
            file.close()
            DB_Interface.con = mysql.connector.connect(
                host=credentials['host'],
                user=credentials['user'],
                password=credentials['password'],
                database=credentials['database']
            )
            DB_Interface.db_cursor = DB_Interface.con.cursor(dictionary=True)
        else:
            return


    def add_employee(self, email: str, name: str, password: str, company_name: str, manager_email: str = None):
        """
        Create a database entry for an employee, using their email as an identifier

        Parameters:
        email (str): The employee's email address
        name (str): The employee's full name
        password (str): The employee's password - will be encrypted using MD5 hash
        company_name (str): company_name The employee's company name
        manager_email (str): The employee's manager's email
        """
        query = "";

        if (manager_email == None):
            query = "INSERT INTO employee (empl_email, empl_name, empl_pwd, company_name) VALUES ('" + email + "', '" + name + "',  MD5('" + password + "'), '" + company_name + "');";
        else:
            query = "INSERT INTO employee (empl_email, empl_name, empl_pwd, company_name, manager_email) VALUES ('" + email + "', '" + name + "',  MD5('" + password + "'), '" + company_name + "', '" + manager_email + "');";
        
        try:
            DB_Interface.db_cursor.execute(query)
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Employee record inserted.")
        except Exception as e:
            print("Error inserting record:", e)
            return False


    def del_employee(self, email: str):
        """
        Delete a database entry for an employee, using their employee email address

        Parameters:
        email (str): The email of the employee to be deleted
        """
        try:
            DB_Interface.db_cursor.execute("DELETE FROM employee WHERE empl_email = '" + email + "';")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Employee record(s) deleted.")
        except Exception as e:
            print("Error deleting record:", e)
            return False


    def ret_employee(self, email: str) -> list:
        """
        Retrieves a database entry for an employee, using their employee email address
    
        Parameters:
        email (str): The email of the employee

        Returns:
        list: A list containing the database entry for the employee, or an empty list if no entry exists
        """
        DB_Interface.db_cursor.execute("SELECT * FROM employee WHERE empl_email = '" + email + "';")
        return(DB_Interface.db_cursor.fetchall())


    def ret_employee_pwd(self, email: str, password: str) -> list:
        """
        Retrieves a database entry for an employee, using their employee email address and password

        Parameters:
        email (str): The email of the employee
        password (str): The password of the employee

        Returns:
        list: A list containing the database entry for the employee, or an empty list if no entry exists
        """
        DB_Interface.db_cursor.execute("SELECT * FROM employee WHERE empl_email = '" + email + "' AND empl_pwd = MD5('" + password + "');")
        return(DB_Interface.db_cursor.fetchall())
    

    def is_manager(self, email: str) -> bool:
        """
        Parameters:
        email (str): The email of the employee

        Returns: True if the employee is a manager, False otherwise
        """
        DB_Interface.db_cursor.execute("SELECT * FROM employee WHERE manager_email = '" + email + "';")
        if DB_Interface.db_cursor.fetchall() == []:
            return False
        else:
            return True


    def add_company(self, company_name: str):
        """
        Create a database entry for a company. Company name will be used as the identifier

        Parameters:
        company_name (str): The company's name
        """
  
        try:
            DB_Interface.db_cursor.execute("INSERT INTO company (company_name) VALUES ('" + company_name + "');")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Company record(s) inserted.")
        except Exception as e:
            print("Error inserting record:", e)
            return False


    def del_company(self, company_name: str):
        """
        Delete a database entry for a company, using the company name
     
        Parameters:
        company_name (str): The name of the company to be deleted
        """
        try:
            DB_Interface.db_cursor.execute("DELETE FROM company WHERE company_name = '" + company_name + "';")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Company record(s) deleted.")
        except Exception as e:
            print("Error deleting record:", e)
            return False


    def ret_company(self, company_name: str) -> list:
        """
        Retrieves a database entry for a company, using the company name

        Parameters: 
        company_name (str): The name of the company

        Returns:
        list: A list containing the database entry for the company, or an empty list if no entry exists
        """
        DB_Interface.db_cursor.execute("SELECT * FROM company WHERE company_name = '" + company_name + "';")
        return(DB_Interface.db_cursor.fetchall())


    def add_leave_request(self, email: str, start_date: datetime, end_date: datetime, reason: str):
        """
        Create a leave request and store it in the database

        Parameters:
        email (str): The employee's email
        start_date (datetime): The start date of the leave request
        end_date (datetime): The end date of the leave request - will be the same as req_start_date if the employee only books one day off
        reason (str): The reason for the employee's leave request
        """

        start_date_formatted = self.__format_date(start_date)
        end_date_formatted = self.__format_date(end_date)

        try:
            DB_Interface.db_cursor.execute("INSERT INTO time_off_request (empl_email, req_start_date, req_end_date, req_reason) VALUES ('" + email + "', '" + start_date_formatted + "', '" + end_date_formatted + "', '" + reason + "');")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Leave request record inserted.")
        except Exception as e:
            print("Error inserting record:", e)
            return False


    def del_leave_request(self, req_id: int):
        """
        Delete a database entry for a leave request
        
        Parameters:
        req_id (int): The id of the request to be deleted
        """
        try:
            DB_Interface.db_cursor.execute("DELETE FROM time_off_request WHERE req_id = '" + str(req_id) + "';")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Leave request record(s) deleted.")
        except Exception as e:
            print("Error deleting record:", e)
            return False

    
    def update_leave_request(self, req_id: int, status: str):
        """
        Update a database entry for a leave request
        
        Parameters:
        req_id (int): The id of the request to be updated
        status (str): Either PENDING, APPROVED or DENIED
        """
        try:
            DB_Interface.db_cursor.execute("UPDATE time_off_request SET req_status = '" + status + "' WHERE req_id = " + str(req_id) + ";")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Leave request record updated.")
        except Exception as e:
            print("Error updating record:", e)
            return False


    def ret_leave_request(self, empl_email: str) -> list:
        """
        Retrieves all leave requests associated with an employee
        
        Parameters:
        empl_email (str): The email of the employee

        Returns:
        list: A list containing the database entries for the leave requests, or an empty list if no entries exist
        """
        DB_Interface.db_cursor.execute("SELECT * FROM time_off_request WHERE empl_email = '" + empl_email + "' ORDER BY req_start_date;")
        return(DB_Interface.db_cursor.fetchall())
    

    def ret_leave_request_week(self, email: str, date: datetime) -> list:
        """
        Retrieves all current and future leave requests associated with an employee
        
        Parameters:
        empl_email (str): The email of the employee
        date (datetime): A date in the week to search

        Returns:
        list: A list containing the database entries for the leave requests, or an empty list if no entries exist
        """
        date = self.__format_date(date)
        DB_Interface.db_cursor.execute("SELECT * FROM time_off_request WHERE empl_email = '" + email + "' AND req_end_date >= '" + date + "';")
        return(DB_Interface.db_cursor.fetchall())
    

    def ret_leave_request_id(self, req_id: int) -> list:
        """
        Retrieves a request using its ID
        
        Parameters:
        req_id (int): The request ID

        Returns:
        dic: A list containing the database entry for the leave request, or an empty list if no entry exists
        """
        DB_Interface.db_cursor.execute("SELECT * FROM time_off_request WHERE req_id = " + str(req_id) + " ORDER BY req_start_date;")
        return(DB_Interface.db_cursor.fetchall())
    

    def ret_subordinate_leave_requests(self, manager_email: str) -> list:
        """
        Retrieves all leave requests associated with an manager's subordinates

        Parameters:
        manager_email (str): The email of the manager

        Returns:
        list: A list containing the database entries for the leave requests, or an empty list if no entries exist
        """
        DB_Interface.db_cursor.execute("SELECT t.* FROM time_off_request t, employee e WHERE e.empl_email = t.empl_email AND e.manager_email = '" + manager_email + "' ORDER BY t.req_start_date;")
        return(DB_Interface.db_cursor.fetchall())
    

    def ret_status_leave_requests(self, manager_email: str, status: str) -> list:
        """
        Retrieves all leave requests with the provided status associated with an manager's subordinates

        Parameters:
        manager_email (str): The email of the manager
        status (str): The status of the leave request

        Returns:
        list: A list containing the database entries for the leave requests, or an empty list if no entries exist
        """
        DB_Interface.db_cursor.execute("SELECT e.empl_name, t.* FROM time_off_request t, employee e WHERE t.req_status = '" + status + "' AND e.empl_email = t.empl_email AND e.manager_email = '" + manager_email + "' ORDER BY t.req_start_date;")
        return(DB_Interface.db_cursor.fetchall())
    
    def request_overlapping(self, empl_email: str, start_date: datetime, end_date: datetime) -> bool:
        """
        Determines if any existing requests overlap with the provided dates

        Parameters:
        empl_email (str): The email address of the employee to check
        start_date (datetime): The start date of the time period to check
        end_date (datetime): The end date of the time period to check

        Returns:
        bool: True if the dates overlap with an existing record, False otherwise
        """
        start_date_formatted = self.__format_date(start_date)
        end_date_formatted = self.__format_date(end_date)

        DB_Interface.db_cursor.execute("SELECT * FROM time_off_request WHERE empl_email = '" + empl_email + "' AND ('" + start_date_formatted + "' <= req_end_date AND '" + end_date_formatted + "' >= req_start_date);")
        existing_requests = DB_Interface.db_cursor.fetchall()
        if existing_requests == []:
            return False
        else:
            return True

    def add_wfh_day(self, email: str, date: datetime):
        """
        Store data for a work from home day
        
        Parameters:
        email (str): The employee's email
        date (datetime): The date of the work from home day
        """
        date_formatted = self.__format_date(date)

        try:
            DB_Interface.db_cursor.execute("INSERT INTO wfh_day (empl_email, wfh_date) VALUES ('" + email + "', '" + date_formatted + "');")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Work from home day record inserted.")
        except Exception as e:
            print("Error inserting record:", e)
            return False


    def del_wfh_day(self, email: str, date: datetime):
        """
        Delete a database entry for a work from home date

        Parameters:
        email (str): The email of the request to be deleted
        date (datetime): The date to be deleted
        """
        date_formatted = self.__format_date(date)

        try:
            DB_Interface.db_cursor.execute("DELETE FROM wfh_day WHERE empl_email = '" + email + "' AND wfh_date = '" + date_formatted + "';")
            DB_Interface.con.commit()
            print(DB_Interface.db_cursor.rowcount, "Work from home day record(s) deleted.")
        except Exception as e:
            print("Error deleting record:", e)
            return False


    def ret_wfh_day(self, email: str) -> list:
        """
        Retrieves all work from home days associated with an employee
        
        Parameters:
        email (str): The email of the employee

        Returns:
        list: A list containing the database entries for the work from home days, or an empty list if no entries exist
        """
        DB_Interface.db_cursor.execute("SELECT * FROM wfh_day WHERE empl_email = '" + email + "' ORDER BY wfh_date;")
        return(DB_Interface.db_cursor.fetchall())
    

    def ret_wfh_day_week(self, email: str, date: datetime) -> list:
        """
        Retrieves all work from home days associated with an employee for the current week of the given day and beyond
        
        Parameters:
        email (str): The email of the employee
        date (datetime): A date in the week to search

        Returns:
        list: A list containing the database entries for the work from home days, or an empty list if no entries exist
        """
        week_start = date - datetime.timedelta(date.weekday())

        week_start = self.__format_date(week_start)

        DB_Interface.db_cursor.execute("SELECT * FROM wfh_day WHERE empl_email = '" + email + "' AND wfh_date >= '" + week_start + "';")
        return(DB_Interface.db_cursor.fetchall())
    

    def wfh_day_overlapping(self, email: str, date: datetime) -> bool:
        """
        Checks if an employee has already booked a date for work from home
        
        Parameters:
        email (str): The email of the employee
        date (datetime): The date to check

        Returns:
        bool: True if the date has already been scheduled, False otherwise
        """
        DB_Interface.db_cursor.execute("SELECT * FROM wfh_day WHERE empl_email = '" + email + "' AND wfh_date = '" + self.__format_date(date) + "';")
        existing_requests = DB_Interface.db_cursor.fetchall()
        if existing_requests == []:
            return False
        else:
            return True


    def valid_wfh_day(self, email: str, date: datetime, max_week_wfh_days: int) -> bool:
        """
        Checks if an employee can book the given work from home date for the current week 
        
        Parameters:
        email (str): The email of the employee
        date (datetime): The date to schedule
        max_week_wfh_days (int): The maximum number of days an employee is allowed to work from home each week

        Returns:
        bool: True if the employee can schedule the date, False otherwise
        """
        week_start = date - datetime.timedelta(date.weekday())
        week_end = week_start + datetime.timedelta(6)

        week_start = self.__format_date(week_start)
        week_end = self.__format_date(week_end)

        print(week_start, week_end)

        DB_Interface.db_cursor.execute("SELECT * FROM wfh_day WHERE empl_email = '" + email + "' AND wfh_date >= '" + week_start + "' AND wfh_date <= '" + week_end + "';")
        existing_requests = DB_Interface.db_cursor.fetchall()
        print(existing_requests)
        if len(existing_requests) < max_week_wfh_days:
            return True
        else:
            return False
        

    def __format_date(self, date: datetime) -> str:
        """
        Converts a datetime object to a string properly formatted for database insertion

        Parameters:
        date (datetime): The date to format
        
        Returns:
        str: String representation of the date, in the format YYYY-MM-DD
        """
        return('-'.join(str(day) for day in [date.year, date.month, date.day]))