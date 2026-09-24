def build_tailored_package(cv_text: str, job_title: str, company: str, description: str):
    # Replace this deterministic adapter with your LLM provider.
    keywords = []
    for word in ["AI", "3D", "Unity", "C#", "Figma", "Adobe", "Blender", "UX", "design", "Python"]:
        if word.lower() in description.lower() and word.lower() in cv_text.lower():
            keywords.append(word)

    profile = cv_text[:1800]
    cover = (
        f"Application for {job_title} at {company}\n\n"
        f"I am interested in the {job_title} opportunity at {company}. "
        f"My background combines visual design, 3D, interactive experiences and technology. "
        f"Relevant capabilities reflected in my experience include: {', '.join(keywords) or 'creative technology and digital design'}.\n\n"
        "I would be glad to discuss how my experience could contribute to the team."
    )
    email = (
        f"Subject: Application | {job_title} | {company}\n\n"
        f"Hi,\n\nI’m reaching out regarding the {job_title} position at {company}. "
        "I have a background combining design, 3D, interactive technology and AI-oriented creative work. "
        "I’ve attached my tailored CV and portfolio for consideration.\n\n"
        "Best,\nBeatrice"
    )
    return profile, cover, email
