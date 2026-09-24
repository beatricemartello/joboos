from ..config import settings

KEYWORDS = ["AI", "3D", "Unity", "C#", "Blender", "Figma", "Adobe", "Python", "XR", "UX", "design", "metaverse", "creative technology"]

def generate(cv_text, job):
    jd = job.description.lower()
    matched = [k for k in KEYWORDS if k.lower() in jd and k.lower() in cv_text.lower()]

    evidence = cv_text[:2500] if cv_text else "Upload a master CV to enable evidence-based tailoring."

    tailored = f"""TARGETED CV PLAN
Role: {job.title}
Company: {job.company}

Priority keywords supported by the master CV:
{", ".join(matched) if matched else "Review required"}

Evidence to prioritize:
{evidence}

Rule: this module may rephrase and prioritize evidence from the master CV, but must not invent experience, skills, titles or results."""

    cover = f"""Application for {job.title} at {job.company}

I am interested in the {job.title} opportunity at {job.company}. My background combines visual design, 3D, interactive experiences and technology. Relevant areas from my experience include {", ".join(matched) if matched else "creative technology and digital design"}.

I would be glad to discuss how this background could contribute to the team."""

    email = f"""Subject: Application | {job.title} | {job.company}

Hi,

I’m reaching out regarding the {job.title} position at {job.company}. My background combines design, 3D, interactive technology and AI-oriented creative work.

I’ve prepared a tailored CV and portfolio for the role:
{settings.portfolio_url}

Best,
Beatrice"""

    social = f"""Hi! I just applied for the {job.title} role at {job.company}. My background combines design, 3D, interactive technology and AI. I’d love to connect and learn more about the team."""

    return tailored, cover, email, social
