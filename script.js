function login() {
    // Fetch values from the form
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Send login request to the backend
    fetch('backend/login.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        // Check the response from the backend
        if (data.success) {
            // Redirect to the dashboard if login is successful
            window.location.href = 'dashboard.html';
        } else {
            alert('Login failed. Please check your credentials.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display existing leave requests
    fetchLeaveRequests();

    // Fetch and display the username
    fetchUsername();

    // Display current week in columns
    displayCurrentWeekColumns();
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
}

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
}

