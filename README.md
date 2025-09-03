# Healing Atlas — Survivor-Centered Design for Safer Onboarding

A gentle, emotionally intelligent dashboard built with Django and vibe coding to support survivors through trauma-informed onboarding, resource mapping, and community connection.

---

## Table of Contents  
- Overview / Pitch  
- Pitch Deck  
- Demo Video  
- Flow  
- Screenshots  
- Deployed Link  
- Tech Stack  
- Build Process  
- Prompting Journey  
- How to Run Locally  
- Future Plans  
- Credits & Acknowledgments  

---

## Overview / Pitch

Healing Atlas is a survivor-first platform designed to guide users through emotionally safe onboarding, resource access, and community support. Every UI decision is paced with care, balancing technical clarity and emotional resonance.

Built with Django and vibe coding, this project centers intuitive prompting, emotional pacing, and technical transparency. It’s not just a dashboard—it’s a healing space.

---

## Pitch Deck

You can view the full pitch deck here:  
👉 [Healing Atlas Pitch Deck](https://www.canva.com/design/DAGxhrXv2xo/XWTQ9Nn8i-IStobt8X5XWQ/view?utm_content=DAGxhrXv2xo&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hd2952937e4)

This deck outlines the emotional logic, survivor-first design principles, and strategic roadmap behind Healing Atlas. It complements the README by offering a visual and narrative overview of the project’s purpose and future direction.

---

## Demo Video

[Watch the Demo](https://www.youtube.com/watch?v=9vgu9MREbIA)  
(Silent walkthrough — no voiceover, no captions. Just the interface, unfolding.)

---

## Flow

- **Landing Page**: Gentle hero image, soft palette, clear CTA  
- **Signup/Login**: Survivor-centered onboarding, tiered membership (Free, Basic, Premium)  
- **User Dashboard**:  
  - Mood tracker  
  - Journaling space  
  - Resources 
- **Paystack Integration**: Seamless, secure, emotionally clear  
- **Design Intent**: Every element is paced for emotional safety, clarity, and trust

---

## Screenshots

| Home Page | Sign Up | Login |
|-----------|---------|-------|
| ![Home Page](https://github.com/user-attachments/assets/88886358-be80-4398-9cd5-981d223a361c) | ![Sign Up](https://github.com/user-attachments/assets/50b45e76-9b39-45f1-bc8c-73af8979a432) | ![Login](https://github.com/user-attachments/assets/cf496794-a730-4ca9-aa82-5e70986def40) |

---

## Deployed Link

Explore the live site:  
👉 [Healing Atlas](https://healingatlas.onrender.com/)

---

## Tech Stack

- **Type**: Web Application  
Note: Healing Atlas is optimized for desktop browsers. Mobile access is possible, but the experience may feel visually compressed or less spacious. For the most emotionally clear and structured experience, we recommend using a laptop or desktop device._
- **Backend**: Django (Python)  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: SQLite (initially), scaled to PostgreSQL  
- **Sentiment Analysis**: Hugging Face API (used to generate emotional insights from journal entries and mood logs)  
- **Version Control**: Git & GitHub  
- **Deployment**: Render (automated builds from GitHub)  
- **Methodology**: Vibe Coding — emotionally paced prompting and healing-centered development

---

## Build Process (Step-by-Step)

1. **Emotional Mapping & Ideation**  
   - Defined survivor needs and emotional milestones  
   - Created a pacing map for onboarding flow  

2. **Django Setup**  
   - Initialized Django project and apps  
   - Configured models for users, resources, and payment integration  

3. **Database Design**  
   - Started with SQLite for simplicity  
   - Structured tables for trauma-informed data handling  
   - Migrated to PostgreSQL to support secure, scalable deployment on Render

4. **Frontend Development**  
   - Built responsive layouts with HTML, CSS  
   - Added interactive elements with JavaScript  
   - Styled with emotional cues (color, spacing, copy)  

5. **Views & Templates**  
   - Created Django views for onboarding, dashboard, and resource pages  
   - Used Django templating for dynamic rendering  
   - Integrated Hugging Face API to analyze journal and mood data, generating sentiment charts that visualize emotional patterns over time  

6. **Deployment**  
   - Versioned with GitHub  
   - Deployed via Render

---

## Prompting Journey (Vibe Coding)

This project was built using emotionally paced prompting. Here’s how the flow unfolded:

- **Prompt 1**: “Design a dashboard that feels like a warm hug but still gets things done.”  
- **Prompt 2**: “How do we guide someone gently through a story they’re scared to tell?”  
- **Prompt 3**: “Build a layout that breathes—space, softness, and clarity.”  
- **Prompt 4**: “What does safety look like in a button? In a font?”

Each prompt led to design and dev decisions that centered emotional safety. The vibe coding method allowed intuition and empathy to guide the technical build.

---

## How to Run Locally

On Windows

```bash
git clone https://github.com/Flora72/Healing_Atlas
cd Healing_Atlas
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
On Mac

```
git clone https://github.com/Flora72/Healing_Atlas
cd Healing_Atlas
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

---

## Future Plans

- Add multilingual support for broader accessibility  
- Integrate trauma-informed AI onboarding flows  
- Expand resource mapping to include global survivor networks
- Continue optimizing PostgreSQL for performance and scale 
- Build contributor guidelines with emotional tone pacing  
- Develop a modular toolkit for other survivor-led platforms  

---

## Credits & Acknowledgments

Built with care by Florence Ndinda. This project is rooted in survivor-first logic, emotional clarity, and the belief that technology can be a space for healing.

Special thanks to:  
- Survivors and advocates who shaped the emotional blueprint  
- Collaborators who offered feedback with gentleness and precision  
- The open-source community for tools that made this possible
