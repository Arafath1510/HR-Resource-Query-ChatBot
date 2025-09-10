
# HR Resource ChatBot


A simple chatbot that helps you find employees based on their skills, experience, and projects using smart search technology.

## How it Works

- You ask questions like "Find Python developers with 3+ years experience"
- The app understands what you're looking for using AI embeddings
- It searches through employee data and shows you the best matches
- No complicated AI needed - it uses fast semantic search


## What You Need
- Python 3.9+
- pip (Python package installer) + install requirements file

## Quick Setup

1. **Install required packages**:

pip install flask flask-cors sentence-transformers faiss-cpu numpy


2. **Add your employee data (create employees.json)**:
eg: ```
{
  "employees": [
    {
      "id": 1,
      "name": "Arafath Faruk",
      "skills": ["Python", "Numpy", "Pandas"," Scikit-learn"],
      "experience_years": 3,
      "projects": ["Churn Prediction", "Marketing Analytics"],
      "availability": "available"
    }
}```

4. **Run the Application**:

python app.py

4. **Open your browser and go to**: *http://localhost:5000*





##  How To Use

--> Type your question in the chat box

--> The bot will find matching employees

--> Results show skills, experience, and why they matched


## Example Questions to Try ?
"Find React developers"

"Who knows AWS and Docker?"

"Developers with 4+ years experience"

"People who worked on healthcare projects"
## API End Points
```http
GET / - Main chat interface

GET /employees - List all employees

GET /employees/search?q=query - Search employees

POST /chat - Chat with the bot
```
## How I Built This
 - I used AI tools to help with:

- Setting up the Flask server

- Configuring the search technology (FAISS + sentence transformers)

- Writing documentation

#### The smart parts I built myself:

- The matching logic that finds the right employees

- The response formatting to make answers clear and useful

### Why This Approach ?
- Fast: No waiting for complex AI models

- Simple: Easy to understand and maintain

- Effective: Finds what you're looking for quickly

- Self-contained: Everything runs on your computer
## Files in This Project
```
your-project/
1.├── app.py                 # Main application
2. ├── employees.json        # Your employee data
3. ├── templates/
   3.1     └── index.html    # Web interface
4. └── README.md             # This file
5. └── requirements.txt      # Package installer
```
## Need Help?

-> If something doesn't work:

-> Make sure all packages are installed

-> Check your employees.json file is valid JSON

-> Try stopping and restarting the app
## Future Ideas
- Add login for security
- Include more employee details
- Deploy online so others can use it
- Add filters for experience years
- Improve the accuracy of search similarity using other LLM



# Ready to start? Run python app.py and open your browser!

## ----------- BYE/RUN ------------
