const DB_Interface = require('./src/db_interactions.js');
const DB = new DB_Interface(); 

DB.add_employee("test_email1", "test1", "test_password2", "Test Company");
DB.ret_employee("test_email1").then(function(rows) {
    console.log(rows);
}).catch((err => console.log(err)));


DB.add_employee("test_email2", "test2", "test_password2", "Test Company", "test_email1");
DB.ret_employee("test_email2").then(function(rows) {
    console.log(rows);
}).catch((err => console.log(err)));


