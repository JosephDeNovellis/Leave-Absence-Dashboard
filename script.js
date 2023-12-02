import DB_Interface from './src/db_interactions.js';
const DB = new DB_Interface(); 


function login() {
    // Fetch values from the form
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    console.log("Username:", username);
    console.log("Password:", password);

    // Use the DB_Interface to authenticate the user
    DB.ret_employee(username)
        .then(data => {
            console.log("Data from ret_employee:", data);

            // Check if the user exists in the database
            if (data.length > 0) {
                console.log("User found in the database");

                // Compare the entered password with the stored password
                
                if (data[0].empl_pwd === password) {
                    console.log("Password matched. Redirecting to dashboard...");
                    // Redirect to the dashboard if login is successful
                    window.location.href = 'dashboard.html';
                } else {
                    alert('Login failed. Incorrect password.');
                }
            } else {
                alert('Login failed. User not found.');
            }
        })
        .catch(error => {
            console.error('Error from ret_employee:', error);
        });
}


/*
document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display existing leave requests
    fetchLeaveRequests();

    // Fetch and display the username
    fetchUsername();

    // Display current week in columns
    displayCurrentWeekColumns();

    // Add event listener for leave form
    document.getElementById('leaveDate').addEventListener('change', function() {
        document.getElementById('leaveForm').style.display = 'block';
    });
});

function displayCurrentWeekColumns() {
    var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var weekColumns = document.getElementById('weekColumns');

    // Get the current date
    var currentDate = new Date();

    // Calculate the start and end of the current week
    var startDate = new Date(currentDate);
    startDate.setDate(currentDate.getDate() - currentDate.getDay()); // Start from Sunday
    var endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + 6); // End on Saturday

    // Display the current week
    document.getElementById('currentWeek').innerText = 'Week of: ' + formatDate(startDate) + ' to ' + formatDate(endDate);

    // Display columns for each day of the week
    daysOfWeek.forEach(function(day) {
        var dayColumn = document.createElement('div');
        dayColumn.className = 'day-column';
        dayColumn.innerText = day;

        weekColumns.appendChild(dayColumn);
    });

    // Add event listener for each day column
    weekColumns.addEventListener('click', function(event) {
        const dateBox = event.target;
        if (dateBox.tagName === 'DIV' && dateBox.classList.contains('day-column')) {
            // Set the selected date in the leave form
            document.getElementById('leaveDate').value = formatDate(startDate);
            // Show the leave form
            document.getElementById('leaveForm').style.display = 'block';
        }
    });
}

// ... (Rest of the code remains unchanged)

function formatDate(date) {
    var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
    return date.toLocaleDateString(undefined, options);
}


function fetchLeaveRequests() {
    // Fetch existing leave requests from the backend
    fetch('backend/leave_requests.php')
    .then(response => response.json())
    .then(data => {
        var leaveRequests = data.leaveRequests;
        var leaveRequestsList = document.getElementById('leaveRequests');
        
        leaveRequestsList.innerHTML = ''; // Clear existing list

        leaveRequests.forEach(function(request) {
            var listItem = document.createElement('li');
            listItem.innerText = request;
            leaveRequestsList.appendChild(listItem);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function fetchUsername() {
    // Fetch username from the backend
    fetch('backend/get_username.php')
    .then(response => response.json())
    .then(data => {
        document.getElementById('welcomeMessage').innerText = 'Welcome, ' + data.username + '!';
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function submitLeaveRequest() {
    // Fetch values from the form
    var leaveDate = document.getElementById('leaveDate').value;

    // Send leave request to the backend
    fetch('backend/submit_leave_request.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ leaveDate: leaveDate }),
    })
    .then(response => response.json())
    .then(data => {
        // Check the response from the backend
        if (data.success) {
            // Fetch and display updated leave requests
            fetchLeaveRequests();
        } else {
            alert('Leave request submission failed.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}*/
