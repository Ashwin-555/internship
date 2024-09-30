const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const port = 5000;

// Set up middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(express.static('public'));

// Multer setup for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
});
const upload = multer({ storage: storage });

// Endpoint for Extract and Save
// Route to handle the form submission
app.post('/extract-save', (req, res) => {
    const folderPath = req.body.folderPath;
    const filename = req.body.filename;
    const date = req.body.date;

    console.log('Folder Path:', folderPath);
    console.log('Filename:', filename);
    console.log('Date:', date);

    if (!folderPath || !filename || !date) {
        return res.status(400).send('Missing required parameters');
    }

    // Ensure Python script path is correct
    const pythonScript = path.join(__dirname, 'extract_text.py');

    // Command to execute Python script with folderPath, filename, and date as arguments
    const command = `python "${pythonScript}" "${folderPath}" "${filename}" "${date}"`;

    // Execute the Python script
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).send(`Error: ${error.message}`);
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send(`stderr: ${stderr}`);
        }

        // Return the script output back to the user
        res.send(stdout);
    });
});

// Endpoint for Search and Tag
app.post('/search-tag', upload.single('file'), (req, res) => {
    const { searchTerm } = req.body;
    const filePath = path.join(__dirname, 'uploads', req.file.filename);
    
    exec(`python search_tag.py "${filePath}" "${searchTerm}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${stderr}`);
            return res.status(500).send(`Error: ${stderr}`);
        }
        res.send(`Search complete: ${stdout}`);
    });
});

// Endpoint for Extract from Invoice
app.post('/extract-invoice', upload.single('file'), (req, res) => {
    const filePath = path.join(__dirname, 'uploads', req.file.filename);

    exec(`python extract_invoice.py "${filePath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${stderr}`);
            return res.status(500).json({ error: 'Failed to extract invoice details' });
        }

        // Assuming stdout returns JSON like: {"invoiceNumber": "12345", "invoiceDate": "2024-01-01"}
        const invoiceDetails = JSON.parse(stdout);
        res.json(invoiceDetails); // Send the extracted details back as JSON
    });
});


// Start the server
const PORT = process.env.PORT || 5000;
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
