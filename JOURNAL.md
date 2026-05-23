# This Journal gets updated automatically by the Journal Logger Agent
## 2026-05-18

### Work completed
- Opened the Corpus Forge starter project in VS Code.
- Installed and ran the Streamlit application locally.
- Tested document upload with a TXT file.
- Confirmed that uploaded documents can be selected and previewed.
- Added document removal so users can delete uploaded files.
- Added AI question answering for selected documents using the Gemini API.
- Added AI usage display with request count and estimated token usage.
- Added flashcard generation from selected documents.
- Added quiz generation from selected documents.
- Added code review report generation for source code documents.

### Problems encountered
- The app first failed because it was run with `python app.py` instead of `streamlit run app.py`.
- Streamlit was not recognized at first, so dependencies had to be installed.
- The first Gemini model name did not work with the API.
- The API key was not loading correctly until `load_dotenv(override=True)` was used.
- Some API keys or model names caused quota or invalid key errors.

### Fixes
- Used `python -m streamlit run app.py` to run the app correctly.
- Added `.env` support for the Google API key.
- Changed the model to a working Gemini model.
- Tested the Ask AI feature after fixing the key and model issue.
- Saved generated artifacts inside the `artifacts` folder.

### Next steps
- Add architecture and control-flow report generation.
- Improve the README with setup instructions.
- Update the report with team members, architecture, engineering decisions, and AI collaboration.
- Create or update `.env.example` so teammates know how to configure their own API key.
### **New Interaction**
- **Hook Version**: 1.02
- **Date**: 19-05-2026 14:06
- **Prompt**: Add an automatic journal logger to this Streamlit app.  Requirements: - Use JOURNAL.md in the project root. - Create a function called log_journal(action). - The function should append the current date/time and the action to JOURNAL.md. - Log these actions:   - when a document is uploaded   - when a document is deleted   - when the user asks AI a question   - when flashcards are generated   - when a quiz is generated   - when a code review report is generated - Do not remove existing features. - Keep the code simple and beginner-friendly.

### **Summary of Changes**
- **Date**: 19-05-2026 14:20
- **Task**: Added automatic journal logging functionality to Corpus Forge Streamlit app
- **Changes Made**:
  1. Added `from datetime import datetime` import
  2. Created `log_journal(action)` function that appends timestamped entries to JOURNAL.md
  3. Called `log_journal()` at 5 action points:
     - Document upload: logs filename
     - Document deletion: logs filename
     - User asks AI: logs first 50 characters of question
     - Flashcards generated: logs action
     - Quiz generated: logs action
  4. No existing features were removed
  5. Code is simple and beginner-friendly with docstring
- **Format**: Entries are appended to JOURNAL.md in chronological order with format: `- **YYYY-MM-DD HH:MM:SS**: action description`
- **Next Steps**: Code review report logging can be added when that feature is implemented

- **2026-05-23 21:17:42**: Architecture/control-flow report generated