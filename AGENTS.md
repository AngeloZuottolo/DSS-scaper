# AGENTS.md

## Project Overview

DSS SkyNet Fleet Scraper - Automated login and data extraction from SkyNetX fleet management portal.

## Build / Test / Run Commands

### Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

### Running
```bash
# Run the scraper
python scraper.py

# Or via batch script (Windows)
run_scraper.bat
```

### Testing
```bash
# Run all tests (pytest)
python -m pytest tests/ -v

# Run a specific test file
python -m pytest tests/test_scraper.py -v

# Run a single test
python -m pytest tests/test_scraper.py::test_login -v
```

### Code Quality (if available)
```bash
# Python linting
ruff check .

# Python formatting
ruff format .

# Type checking
python -m mypy .
```

## Code Style Guidelines

### Python

- **Indentation:** 4 spaces (no tabs)
- **Line length:** 100 characters max
- **Docstrings:** Google style for public functions/classes
- **Type hints:** Use modern syntax (`str | None`, `list[dict]`)
- **Naming:**
  - `snake_case` for functions, variables, file names
  - `PascalCase` for class names
  - `SCREAMING_SNAKE_CASE` for constants
- **Imports:** Standard library → third-party → local (blank line between groups)
- **Error handling:** Use specific exceptions; wrap API calls in try/except
- **Logging:** Use `print()` with bracketed prefixes (`[OK]`, `[ERROR]`, `[INFO]`)

### HTML

- **Structure:** Semantic HTML5 elements (`<header>`, `<main>`, `<section>`)
- **Language:** Set `lang` attribute (e.g., `lang="it"`)
- **Meta:** Include charset and viewport
- **Comments:** HTML comments for major sections

### CSS

- **Variables:** Use CSS custom properties (`:root`) for theming
- **Naming:** kebab-case (e.g., `.stat-card`, `.tab-btn`)
- **Organization:** Group related properties
- **Responsive:** Use CSS Grid and Flexbox

## Architecture

### File Structure
```
DSS-scaper/
├── scraper.py         # Main scraper logic (SkyNetScraper class)
├── config.py         # Configuration and environment variables
├── index.html        # Dashboard HTML with inline CSS/JS
├── skynet_data.json  # Output data file
├── session.json      # Session persistence
├── .env              # Credentials (not committed)
├── requirements.txt  # Python dependencies
└── run_scraper.bat   # Windows runner script
```

### Key Classes

- **`SkyNetScraper`** (scraper.py): Main class handling login, session persistence, and data extraction

### Data Flow
1. Load credentials from `.env` via `config.py`
2. Create `SkyNetScraper` instance and call `login()`
3. Extract data via `get_sitemap()`, `get_functionalities()`, `get_units()`
4. Save to `skynet_data.json` and update `index.html`

## Configuration

Credentials stored in `.env`:
```
DSS_USERNAME=your_username
DSS_PASSWORD=your_password
DSS_PIN=your_pin          # Optional, defaults to "demodss"
```

## Dependencies

- `requests` - HTTP client
- `python-dotenv` - Environment variables
- `playwright` - Browser automation (available but optional)
- `beautifulsoup4` - HTML parsing (available but optional)
- `lxml` - XML/HTML parser (available but optional)

## CI/CD

- **Python version:** 3.11
- **Test framework:** pytest (gracefully handles missing tests)
- **Workflow:** `.github/workflows/ci.yml`

## Conventions

- **No secrets in code:** Use `.env` for credentials
- **Session persistence:** Save to `session.json` for re-authentication
- **Data output:** JSON format with ISO timestamps
- **Error output:** Colored/prefixed console messages

## Current Status (19/03/2026)

### Project Progress
- [x] Project setup and repository initialization
- [x] SkyNet scraper implementation with login automation
- [x] HTML dashboard with interactive UI
- [x] Session persistence with `session.json`
- [x] Daily activity report generation (Word format)

### Completed Features
- Automated login to SkyNetX portal
- Sitemap and functionalities extraction
- Units data retrieval
- Interactive dashboard (`index.html`)
- Data export to `skynet_data.json`
- Daily report generation (`Report_Attivita_*.docx`)

### Next Steps
- [ ] Add unit tests for scraper functions
- [ ] Implement error handling improvements
- [ ] Add scheduling capability for automated runs

## Git Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit with descriptive message
3. Push and create PR to `master`
4. CI runs automatically on push/PR
