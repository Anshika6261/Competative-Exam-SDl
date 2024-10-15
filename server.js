// server.js (or app.js)
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());  // Enable CORS to allow requests from your frontend
app.use(express.json());

// MySQL connection setup
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Anshika@123',
    database: 'exam_data'
});

// Connect to MySQL
db.connect(err => {
    if (err) {
        console.error('Error connecting to the database:', err);
    } else {
        console.log('Connected to the MySQL database.');
    }
});

// API endpoint to fetch exam data
app.get('/api/exams', (req, res) => {
    const query = 'SELECT exam_name, title, link FROM exams';

    db.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching exam data:', err);
            res.status(500).json({ message: 'Server error. Could not retrieve data.' });
        } else {
            res.json(results);  // Send the exam data as JSON to the frontend
        }
    });
});

// Start the server
const port = 8080;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
