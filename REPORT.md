# Project Report

#### The Team members
Olamipo Adewumi olamipo.adewumi@epita.fr OLADAGOAT
Fadl Annan fadl.annan@epita.fr fadl777 
Busra Iusein busra.iusein@epita.fr IB22-08-2006
---

#### Initial Design
Corpus Forge was designed as a local web application that allows users to upload documents and generate useful AI-based outputs from them.

The main idea was to keep the application simple but functional. Instead of building a complex system with a database and advanced frontend, we focused on making the main project features work clearly.

### Initial Architecture

The project is mainly organized around these parts:

- `app.py`: the main Streamlit application
- `data/`: stores uploaded documents locally
- `artifacts/`: stores generated outputs like flashcards, quizzes, and reports
- `JOURNAL.md`: records project activity and runtime logs
- `prompts_history.md`: stores prompts used with AI tools
- `README.md`: explains how to run the project
- `REPORT.md`: explains the technical choices and project development
- `.env`: stores the local Google API key

The application flow is:

1. The user uploads documents.
2. The documents are saved in the `data/` folder.
3. The user selects active documents.
4. The app reads the selected files.
5. The user chooses an AI feature.
6. The selected document content is sent to the Gemini API.
7. The result is shown in the app and saved in the `artifacts/` folder.

### Assumptions

We assumed that the app would run locally on each user’s computer. We also assumed that every group member would use their own `.env` file with their own Google API key.

We decided not to use a database because the project was small and local file storage was enough for this version. The goal was to build a working prototype that could be explained clearly during the presentation.

### Technical Choices

We used Python because it is simple and works well with AI tools and document processing. We used Streamlit because it allowed us to build a web app quickly without needing a separate frontend framework.

We used `pypdf` to read PDF files, `python-dotenv` to load the API key, and the Gemini API for AI generation.

---

#### Engineering Decisions

### Streamlit instead of Flask or FastAPI

We considered using Flask or FastAPI, but Streamlit was easier for this project because it gave us a working user interface quickly. Since the project focus was AI workflows and document interaction, Streamlit helped us spend less time on frontend design and more time on features.

### Local folders instead of a database

We considered using SQLite, but local folders were enough for the prototype. Uploaded documents are stored in `data/`, and generated outputs are stored in `artifacts/`.

This made the system easier to understand, test, and explain.

### `.env` file for API keys

We decided not to write the API key directly inside the code. Each person creates their own `.env` file locally.

This is safer because the API key should not be pushed to GitHub.

### Markdown for generated artifacts

Flashcards, quizzes, code reviews, and architecture reports are saved as Markdown files. Markdown is easy to read, easy to edit, and works well for documentation.

### Small commits instead of one big commit

We tried to commit features step by step. This made the Git history clearer and helped us avoid pushing everything in one large update.

---

#### Who Did What?

* Document how the project was originally divided among each team member.
* Document how responsibilities possibly evolved over time.
 
Since this is an individual project, all responsibilities were handled by one student.

- Repository setup: Olamipo Adewumi
- Application setup and testing: Olamipo Adewumi
- Document ingestion features: Olamipo Adewumi
- AI/RAG workflow implementation: Olamipo Adewumi
- Prompt engineering and testing: Olamipo Adewumi
- README, REPORT, and presentation preparation: Olamipo Adewumi
---

#### AI Collaboration
Document how AI tools were used.
AI tools were used during the project, but not to replace the whole development process. They were used mainly to help understand problems, debug errors, and improve small parts of the application.

The tools used included:

- GitHub Copilot Chat
- AI assistance for debugging
- AI assistance for prompt writing
- AI assistance for documentation structure

AI helped with:

- Understanding Streamlit errors
- Fixing API key loading problems
- Explaining why `python app.py` was not the correct way to run a Streamlit app
- Improving the prompt structure for AI question answering
- Suggesting how to organize the journal logger
- Helping structure the report

AI influenced the project by helping us move faster when we were stuck. However, every suggestion still had to be tested manually.
---

#### Failures and Iterations
#### “When AI Failed or Was Wrong”
AI was useful during the project, but it was not always correct. Some suggestions were incomplete, outdated, or did not work directly in the application.

### Incorrect model names

Some AI-generated suggestions used Gemini model names that did not work with the API. This caused errors such as model not found, quota errors, or unsupported model errors.

The team detected this by running the app and reading the error messages shown in Streamlit. The issue was fixed by changing the model name and testing again until the AI question answering feature worked correctly.

### API key confusion

AI suggestions did not fully solve the API key problem at first. The app was still using the wrong or old key. The issue was fixed by checking the `.env` file, restarting Streamlit, and using:

---

#### Lessons Learned
This project helped the team improve both technical and workflow skills.

Technical Growth
The team learned how to:
Build a local web application with Streamlit
Upload and read different document types
Extract text from PDF files
Use environment variables safely
Connect a web app to the Gemini API
Generate AI-based flashcards, quizzes, and reports
Save generated artifacts as Markdown files
Track basic AI usage statistics
Use GitHub with smaller and clearer commits

Workflow Improvements
The project showed the importance of:
Testing each feature before committing
Keeping .env private
Using .gitignore correctly
Writing meaningful commit messages
Keeping the main branch runnable
Documenting problems and fixes
Updating the journal and prompt history during development

Strengths of AI-Assisted Development

AI helped speed up debugging, explain errors, and suggest implementation ideas. It was especially useful for understanding Streamlit problems, API key issues, prompt structure, and documentation organization.

Limitations of AI-Assisted Development

AI was not always correct. Some suggestions used outdated packages, wrong model names, or incomplete fixes. The team learned that AI suggestions must always be tested and verified before being accepted.

## Conclusion

Corpus Forge is a working local web application that allows users to upload documents, interact with selected corpora using AI, and generate useful learning and code-related artifacts.

The project includes:
Document upload
Document deletion
Document selection
Document preview
AI question answering
Flashcard generation
Quiz generation
Code review report generation
Architecture and control-flow report generation
Artifact saving
AI usage tracking
Automatic journal logging

The main lesson from this project is that AI can be a useful engineering partner, but it still needs human testing, debugging, decision-making, and clear documentation.