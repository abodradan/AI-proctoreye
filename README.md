# AI ProctorEye

**⚠️ This project is currently under active development. Expect frequent updates and changes.**

AI ProctorEye is an intelligent system designed to verify student identities, monitor their behavior during exams, and ensure a secure and fair examination environment. The project leverages AI techniques such as face recognition, barcode scanning, and behavior analysis to detect suspicious activity and prevent cheating.

## Features

- **Student Identity Verification**: Matches a student's current image with the one stored in the database using barcode information.
- **Exam Seat Verification**: Confirms that the student is seated in the correct location.
- **Behavior Monitoring**: Analyzes student behavior during the exam to detect cheating attempts.
- **Progressive Steps**: The project is structured in steps, where each step builds on the previous one to gradually enhance the system's capabilities.
- **Student Registration**: New feature to register students via a user-friendly frontend, uploading their image and details to the backend for processing.
- **Real-time Error Reporting**: The API now returns specific error messages, such as "No face detected in the image," which are displayed in the frontend for better user feedback.

## Project Structure

The project is divided into two main parts:

1. **Real Project** (Python-based API):

   - Contains the core functionality of student identity verification and behavior monitoring.
   - Developed using Python and organized into steps for incremental development.

2. **Frontend Project** (React-based UI):
   - A user interface for registering students, displaying their information, and handling image uploads.
   - Integrated with the API to facilitate seamless communication between frontend and backend.

### Directory Structure

```bash
AI-proctoreye/
│
├── api/  # Core system and API
|   ├── databse/
|   ├── routes/
|   ├── services/
|   ├── services_v2/
|   ├── main.py
|   └── requirements.txt
|   └── README.md
│
├── frontend/  # React-based UI
|   ├── src/
|   |   ├── monitoring/
|   |   |   └── monitoring.jsx
|   |   ├── students/
|   |   |   ├── AddStudent.js
|   |   |   └── StudentList.js
|   |   |   └── ...
│
└── README.md               # Project documentation
```

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/abodradan/AI-proctoreye.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd AI-proctoreye
   ```

3. **Create a Virtual Environment**:

   ```bash
   cd api
   python -m venv venv
   ```

4. **Activate the Virtual Environment**:

   - On **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**:

   After activating the virtual environment, install the required dependencies from the `requirements.txt` file (on api folder):

   ```bash
   pip install -r api/requirements.txt
   ```

6. **Set Up MySQL Database**:

   - Ensure you have **XAMPP** or another MySQL server running to:
   - Create a new database for your project and configure the connection settings in your code in `database/database_manager.py`.

7. **Frontend Setup (React)**:

   - Navigate to the `frontend` folder and install necessary dependencies:

     ```bash
     cd frontend
     npm install
     ```

## Usage

1. **Run the API Server**:

   In the `api` folder, run:

   ```bash
   uvicorn main:app --reload
   ```

   This will start the backend API server on `http://localhost:8000`.

2. **Run the React Frontend**:

   In the `frontend` folder, run:

   ```bash
   npm start
   ```

   This will start the React development server on `http://localhost:3000`.

   - Open your browser and go to `http://localhost:3000` to access the frontend interface where you can add new students, view the student list, and interact with the backend API.

## Development Steps

1. **Step 1**: Create an algorithm to compare the current student's image with the stored one using the barcode.
2. **Step 2**: Identify the student by comparing their image with all students stored in the database, starting with those taking the exam at the same time.
3. **Step 3**: Verify the student is seated in the correct location by matching their image with the expected student for that seat.
4. **Step 4**: Monitor student behavior and detect cheating during the exam.
5. **Step 5**: Add frontend functionality for registering students with their images and details.

## Error Handling and API Updates

- The API now returns more specific error messages for the frontend to handle, such as:
  - "No face detected in the image"
  - "Error saving student data"
- The React frontend now properly displays these errors using an alert box, ensuring users receive relevant feedback when errors occur.

### Example:

If the API encounters an error such as "No face detected in the image", the frontend will display:

```plaintext
Error: No face detected in the image
```

## Future Improvements

- Implement live video analysis for real-time behavior monitoring.
- Add scalability to handle larger datasets and more students efficiently.
- Integrate with external exam management systems for seamless operation.

## Contributing

We welcome contributions to enhance the project! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature-branch
   ```

3. Make your changes.
4. Commit your changes with a descriptive message:

   ```bash
   git commit -m "Add new feature"
   ```

5. Push to the branch you created:

   ```bash
   git push origin feature-branch
   ```

6. Create a new Pull Request:
   - Go to your forked repository on GitHub.
   - Click on the "Pull Requests" tab.
   - Click on the "New Pull Request" button.
   - Select your branch from the dropdown and create the pull request, adding any relevant comments.

## .gitignore

To maintain a clean and organized repository, the following items are included in the `.gitignore` file:

- Python bytecode and cache files
- Virtual environment directories
- Environment variable files
- Logs and debugging files
- SQLite databases (if used)
- Mock databases used for testing
- Node.js dependencies (if frontend uses Node.js)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
