from app.skill_extractor import extract_skills


def calculate_match(resume_text: str,
                    job_description: str):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    matched = list(
        resume_skills.intersection(job_skills)
    )

    missing = list(
        job_skills - resume_skills
    )

    if len(job_skills) == 0:
        score = 0
    else:
        score = int(
            len(matched) /
            len(job_skills) * 100
        )

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }