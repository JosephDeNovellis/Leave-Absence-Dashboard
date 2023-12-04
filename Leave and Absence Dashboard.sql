CREATE TABLE leave_absence_db.company(
    company_name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE leave_absence_db.employee(
    empl_email VARCHAR(255) NOT NULL PRIMARY KEY,
    empl_name VARCHAR(255) NOT NULL,
    empl_pwd VARCHAR(255) NOT NULL,
    manager_email VARCHAR(255),
    company_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (manager_email) REFERENCES employee(empl_email) ON DELETE SET NULL,
    FOREIGN KEY (company_name) REFERENCES company(company_name)
);

CREATE TABLE leave_absence_db.time_off_request(
    req_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    empl_email VARCHAR(255) NOT NULL,
    req_start_date DATE NOT NULL,
    req_end_date DATE NOT NULL,
    req_reason VARCHAR(255) NOT NULL,
    req_status VARCHAR(10) NOT NULL DEFAULT "PENDING",
    UNIQUE (empl_email, req_start_date, req_end_date),
    FOREIGN KEY (empl_email) REFERENCES employee(empl_email)
);

CREATE TABLE leave_absence_db.wfh_day(
    empl_email VARCHAR(255),
    wfh_date DATE NOT NULL,
    PRIMARY KEY (empl_email, wfh_date),
    FOREIGN KEY (empl_email) REFERENCES employee(empl_email)
);