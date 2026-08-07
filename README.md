# ZED-IQ

Think Fast. Think Smart.

ZED-IQ is a Flask, SQLite, Bootstrap 5 quiz platform for Zambian schools and organizations. It includes administrator, teacher, and student roles, timed one-question-at-a-time quizzes, automatic scoring, dashboards, imports, reports, dark mode, and Render deployment files.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

Student portal:

- Home: `/`
- Student login: `/login`
- Dashboard: `/dashboard`
- Profile: `/profile`
- Logout: `/logout`

Administration portal:

- Admin login: `/admin/login`
- Dashboard: `/admin/dashboard`
- Question bank: `/admin/question-bank`
- Quizzes: `/admin/quizzes`
- Students: `/admin/students`
- Teachers: `/admin/teachers`
- Reports: `/admin/reports`
- Settings: `/admin/settings`

Default super admin:

- Email: `admin@zediq.local`
- Password: `Admin123!`

## Database

The SQLite database is created automatically at `instance/database.db` when `python run.py` starts. You can also run:

```bash
flask --app run.py init-db
```

## Question Import

Staff can upload CSV or XLSX files into the Question Bank with these columns:

```text
Question,Option A,Option B,Option C,Option D,Correct Answer,Subject,Topic,Grade,Difficulty,Question Type,Timer,Marks
What is the capital of Zambia?,Lusaka,Kitwe,Kasama,Ndola,A,Civic Education,Zambia,Grade 8,Easy,Multiple Choice,5,1
```

A downloadable CSV template is available at `/admin/question-bank/template.csv`.

## Curriculum Management

The database seeds Zambian secondary school subjects, Grade 8 through Grade 12, and default topics for Mathematics, Biology, Chemistry, Physics, and General Knowledge. Super Admins can manage subjects at `/admin/subjects`; staff can manage topics at `/admin/topics`.

## Deploy To Render

1. Push this project to GitHub.
2. Create a Render web service from the repository, or use `render.yaml`.
3. Set `SECRET_KEY` in Render if not using the generated value.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn wsgi:app`

## Git

```bash
git init
git add .
git commit -m "Initial ZED-IQ app"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Screenshot Placeholders

- Home page: `docs/screenshots/home.png`
- Teacher dashboard: `docs/screenshots/teacher-dashboard.png`
- Quiz screen: `docs/screenshots/quiz.png`
- Results: `docs/screenshots/results.png`
