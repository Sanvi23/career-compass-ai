KNOWN_SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "React",
    "HTML",
    "CSS",
    "SQL",
    "Git",
    "Docker",
    "FastAPI",
    "Machine Learning",
    "TensorFlow",
    "Pandas",
    "NumPy",
    "AWS"
]


def extract_skills(text: str):

    detected = []

    lower_text = text.lower()

    for skill in KNOWN_SKILLS:

        if skill.lower() in lower_text:
            detected.append(skill)

    return detected