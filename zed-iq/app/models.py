from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import inspect
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


def now_utc():
    return datetime.now(timezone.utc)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False, unique=True)
    district = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc)
    users = db.relationship("User", backref="school", lazy=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    active = db.Column(db.Boolean, default=True)
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.active


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(30), default="", index=True)
    description = db.Column(db.Text, default="")
    icon = db.Column(db.String(80), default="book")
    color = db.Column(db.String(20), default="#078052")
    active = db.Column(db.Boolean, default=True, index=True)
    built_in = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc)
    topics = db.relationship("Topic", backref="subject", cascade="all, delete-orphan")


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    name = db.Column(db.String(140), nullable=False, index=True)
    description = db.Column(db.Text, default="")
    active = db.Column(db.Boolean, default=True, index=True)
    built_in = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc)


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), default="")
    active = db.Column(db.Boolean, default=True, index=True)
    sort_order = db.Column(db.Integer, default=0)


class QuestionCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, default="")
    active = db.Column(db.Boolean, default=True, index=True)


class QuestionBank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False, index=True)
    option_a = db.Column(db.String(400), nullable=False)
    option_b = db.Column(db.String(400), nullable=False)
    option_c = db.Column(db.String(400), nullable=False)
    option_d = db.Column(db.String(400), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text, default="")
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"))
    grade = db.Column(db.String(50), default="", index=True)
    grade_id = db.Column(db.Integer, db.ForeignKey("grade.id"))
    difficulty = db.Column(db.String(30), default="Medium", index=True)
    question_type = db.Column(db.String(40), default="Multiple Choice", index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("question_category.id"))
    marks = db.Column(db.Integer, default=1)
    timer_seconds = db.Column(db.Integer, default=5)
    image = db.Column(db.String(255), default="")
    status = db.Column(db.String(20), default="active", index=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc)
    subject = db.relationship("Subject")
    topic = db.relationship("Topic")
    grade_level = db.relationship("Grade")
    category = db.relationship("QuestionCategory")
    created_by = db.relationship("User")


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"))
    grade = db.Column(db.String(50), default="")
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"))
    grade_scope = db.Column(db.String(200), default="")
    max_attempts = db.Column(db.Integer, default=1)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    timer_seconds = db.Column(db.Integer, default=5)
    pass_mark = db.Column(db.Integer, default=50)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc)
    subject = db.relationship("Subject")
    topic = db.relationship("Topic")
    teacher = db.relationship("User")
    questions = db.relationship("Question", backref="quiz", cascade="all, delete-orphan")


class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question_bank_id = db.Column(db.Integer, db.ForeignKey("question_bank.id"), nullable=False)
    order = db.Column(db.Integer, default=0)
    quiz = db.relationship("Quiz")
    bank_question = db.relationship("QuestionBank")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), default="")
    order = db.Column(db.Integer, default=0)
    choices = db.relationship("Choice", backref="question", cascade="all, delete-orphan")


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    label = db.Column(db.String(1), nullable=False)
    text = db.Column(db.String(400), nullable=False)
    correct = db.Column(db.Boolean, default=False)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Float, default=0)
    passed = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime(timezone=True), default=now_utc)
    completed_at = db.Column(db.DateTime(timezone=True))
    quiz = db.relationship("Quiz")
    student = db.relationship("User")
    answers = db.relationship("Answer", backref="result", cascade="all, delete-orphan")


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey("result.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    selected_label = db.Column(db.String(20), default="No Answer")
    correct = db.Column(db.Boolean, default=False)
    answered_at = db.Column(db.DateTime(timezone=True), default=now_utc)
    question = db.relationship("Question")


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


DEFAULT_SUBJECTS = {
    "Core Secondary School Subjects": [
        "Mathematics", "English Language", "Integrated Science", "Biology", "Chemistry", "Physics",
        "Civic Education", "History", "Geography", "Religious Education",
        "Computer Studies / Information and Communication Technology (ICT)",
    ],
    "Business and Commercial Subjects": [
        "Commerce", "Business Studies", "Economics", "Principles of Accounts", "Entrepreneurship",
    ],
    "Agriculture, Technical and Practical Subjects": [
        "Agricultural Science", "Design and Technology", "Technical Drawing", "Metalwork", "Woodwork",
        "Home Economics", "Food and Nutrition", "Fashion and Fabrics", "Art and Design", "Music",
    ],
    "Zambian Local Languages": ["Chinyanja", "Bemba", "Tonga", "Lozi", "Kaonde", "Lunda", "Luvale"],
    "General Knowledge": ["General Knowledge"],
}


DEFAULT_TOPICS = {
    "Mathematics": ["Algebra", "Geometry", "Trigonometry", "Statistics", "Probability", "Sets", "Functions", "Mensuration", "Matrices", "Calculus"],
    "Biology": ["Cells", "Genetics", "Ecology", "Human Body Systems", "Plants", "Reproduction", "Microorganisms", "Evolution"],
    "Chemistry": ["Atomic Structure", "Periodic Table", "Chemical Bonding", "Acids and Bases", "Organic Chemistry", "Electrolysis", "Chemical Reactions"],
    "Physics": ["Mechanics", "Electricity", "Magnetism", "Waves", "Light", "Heat", "Energy", "Forces"],
    "General Knowledge": [
        "Zambia", "Africa", "World History", "World Geography", "Science", "Technology", "Artificial Intelligence",
        "Sports", "Football", "Olympics", "Entertainment", "Music", "Movies", "Famous People", "Literature",
        "Business", "Economics", "Politics", "Current Affairs", "Environment", "Climate Change", "Health",
        "Culture", "Inventions", "Space", "Nature", "Mathematics Puzzles", "Logic and IQ Questions", "Mixed Trivia",
    ],
}


def _code_for(name):
    return "".join(part[0] for part in name.replace("/", " ").replace("(", " ").split() if part).upper()[:12]


def apply_additive_migrations():
    """Add columns introduced after the first SQLite schema without dropping data."""
    inspector = inspect(db.engine)
    tables = set(inspector.get_table_names())
    additions = {
        "subject": [
            ("code", "VARCHAR(30) DEFAULT ''"), ("description", "TEXT DEFAULT ''"), ("icon", "VARCHAR(80) DEFAULT 'book'"),
            ("color", "VARCHAR(20) DEFAULT '#078052'"), ("active", "BOOLEAN DEFAULT 1"), ("built_in", "BOOLEAN DEFAULT 0"),
            ("created_at", "DATETIME"),
        ],
        "question_bank": [
            ("topic_id", "INTEGER"), ("grade_id", "INTEGER"), ("question_type", "VARCHAR(40) DEFAULT 'Multiple Choice'"), ("category_id", "INTEGER"),
        ],
        "quiz": [
            ("topic_id", "INTEGER"), ("grade_scope", "VARCHAR(200) DEFAULT ''"), ("max_attempts", "INTEGER DEFAULT 1"),
            ("start_date", "DATETIME"), ("end_date", "DATETIME"),
        ],
    }
    with db.engine.begin() as connection:
        for table, columns in additions.items():
            if table not in tables:
                continue
            existing = {column["name"] for column in inspector.get_columns(table)}
            for name, definition in columns:
                if name not in existing:
                    connection.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")


def seed_defaults():
    apply_additive_migrations()
    if not School.query.first():
        db.session.add(School(name="ZED-IQ Demo School", district="Lusaka"))
    for category, subjects in DEFAULT_SUBJECTS.items():
        for subject_name in subjects:
            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                subject = Subject(
                    name=subject_name,
                    code=_code_for(subject_name),
                    description=category,
                    icon="globe2" if subject_name == "General Knowledge" else "book",
                    color="#d6a21f" if subject_name == "General Knowledge" else "#078052",
                    active=True,
                    built_in=True,
                )
                db.session.add(subject)
            else:
                subject.built_in = True
                if not subject.code:
                    subject.code = _code_for(subject.name)
    db.session.flush()
    for subject_name, topics in DEFAULT_TOPICS.items():
        subject = Subject.query.filter_by(name=subject_name).first()
        if subject:
            for topic_name in topics:
                if not Topic.query.filter_by(subject_id=subject.id, name=topic_name).first():
                    db.session.add(Topic(subject_id=subject.id, name=topic_name, built_in=True))
    for order, grade_name in enumerate(["Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"], start=8):
        if not Grade.query.filter_by(name=grade_name).first():
            db.session.add(Grade(name=grade_name, description="Secondary school level", sort_order=order))
    for category_name in ["Curriculum", "General Knowledge", "Competition", "Practice", "Examination"]:
        if not QuestionCategory.query.filter_by(name=category_name).first():
            db.session.add(QuestionCategory(name=category_name))
    if not User.query.filter_by(email="admin@zediq.local").first():
        admin = User(name="ZED-IQ Administrator", email="admin@zediq.local", role="super_admin", active=True)
        admin.set_password("Admin123!")
        db.session.add(admin)
    else:
        admin = User.query.filter_by(email="admin@zediq.local").first()
        if admin.role == "admin":
            admin.role = "super_admin"
    db.session.commit()
