from datetime import datetime
from typing import Dict, List
import re


def generate_cover_letter(resume_content: str, job_context: str) -> str:
    """
    Generate a professional cover letter template.
    """
    # Extract name from resume if possible
    name_match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+)', resume_content)
    name = name_match.group(1) if name_match else "[Your Name]"
    
    # Extract email
    email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', resume_content)
    email = email_match.group(0) if email_match else "[your.email@example.com]"
    
    # Extract phone
    phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_content)
    phone = phone_match.group(0) if phone_match else "[Your Phone]"
    
    # Extract key skills
    skills_section = ""
    if 'python' in resume_content.lower():
        skills_section = "Python development"
    elif 'javascript' in resume_content.lower():
        skills_section = "JavaScript development"
    else:
        skills_section = "software development"
    
    today = datetime.now().strftime("%B %d, %Y")
    
    cover_letter = f"""
# Cover Letter Template

**{name}**
{email} | {phone}
[Your City, State]

{today}

**[Hiring Manager's Name]**
**[Company Name]**
**[Company Address]**

Dear Hiring Manager,

## Opening Paragraph
I am writing to express my strong interest in the [Position Title] role at [Company Name]. With my background in {skills_section} and proven track record of delivering high-impact projects, I am excited about the opportunity to contribute to your team.

## Body Paragraph 1 - Your Qualifications
Throughout my career, I have developed expertise in:
- **Technical Excellence**: [Mention specific technologies from your resume that match the job]
- **Problem Solving**: [Highlight a key achievement with quantifiable results]
- **Team Collaboration**: [Discuss your experience working with cross-functional teams]

## Body Paragraph 2 - Why This Company
What particularly excites me about [Company Name] is [research the company and mention something specific - their products, mission, recent achievements, or company culture]. I am impressed by [specific aspect] and believe my skills in [relevant skills] would allow me to make meaningful contributions to [specific project/goal].

## Body Paragraph 3 - Your Value Proposition
In my previous role at [Most Recent Company], I:
- [Achievement 1 with metrics]
- [Achievement 2 with metrics]
- [Achievement 3 with metrics]

These experiences have prepared me to [specific contribution you can make to the company].

## Closing Paragraph
I am enthusiastic about the opportunity to bring my expertise in [key skills] to [Company Name]. I would welcome the chance to discuss how my background, skills, and enthusiasms align with your team's needs. Thank you for considering my application.

Sincerely,
{name}

---

## 📝 Instructions for Customization:

1. **Replace all [bracketed] sections** with specific information
2. **Research the company**: Visit their website, read recent news, check their mission
3. **Match keywords**: Use words from the job description naturally
4. **Quantify achievements**: Add specific numbers and metrics
5. **Show enthusiasm**: Demonstrate genuine interest in the role and company
6. **Proofread**: Check for typos and ensure proper formatting
7. **Keep it concise**: Aim for 3-4 paragraphs, max 1 page

## ✅ Cover Letter Checklist:
- [ ] Personalized to the company and role
- [ ] Includes 2-3 quantifiable achievements
- [ ] Mentions specific technologies/skills from job posting
- [ ] Shows knowledge of the company
- [ ] Professional tone but shows personality
- [ ] No typos or grammatical errors
- [ ] Contact information is current
- [ ] Saved as PDF with clear filename
"""
    
    return cover_letter


def tailor_resume(resume_content: str, job_description: str) -> str:
    """
    Provide suggestions for tailoring resume to specific job.
    """
    job_lower = job_description.lower()
    resume_lower = resume_content.lower()
    
    # Extract key requirements from job description
    required_skills = []
    common_skills = ['python', 'javascript', 'java', 'react', 'node', 'aws', 'docker', 'kubernetes', 'sql', 'machine learning']
    
    for skill in common_skills:
        if skill in job_lower and skill in resume_lower:
            required_skills.append(f"✅ {skill.title()}")
        elif skill in job_lower and skill not in resume_lower:
            required_skills.append(f"❌ {skill.title()} - ADD THIS!")
    
    suggestions = f"""
# Resume Tailoring Guide

## 🎯 Job-Specific Optimization

### Skills Alignment:
{chr(10).join(required_skills) if required_skills else "Analyze job description for required skills"}

### Action Items:
1. **Keywords**: Add these terms naturally throughout your resume
2. **Headline**: Adjust your professional summary to match the role
3. **Prioritize**: Move most relevant experience to the top
4. **Quantify**: Add metrics to your achievements
5. **Remove**: Take out irrelevant information

### Suggested Changes:

#### Professional Summary:
Rewrite your summary to include:
- The exact job title you're applying for
- 3-5 key skills from the job description
- Your years of experience
- One major achievement relevant to this role

#### Skills Section:
- List technical skills that appear in the job posting first
- Use the same terminology as the job description
- Include both acronyms and full terms (ML and Machine Learning)

#### Experience Section:
- Reorder bullet points to highlight relevant experience first
- Add metrics and numbers to show impact
- Use action verbs that match the job description
- Include projects that demonstrate required skills

### 📊 Tailoring Checklist:
- [ ] Job title mentioned in summary
- [ ] 80%+ of required skills included
- [ ] Used keywords from job description 3-5 times
- [ ] Achievements are quantified with metrics
- [ ] Most relevant experience listed first
- [ ] Removed irrelevant information
- [ ] File named: FirstName_LastName_JobTitle.pdf
"""
    
    return suggestions


def generate_interview_prep(resume_content: str, context: str) -> str:
    """
    Generate interview preparation guide.
    """
    prep_guide = f"""
# Interview Preparation Guide

## 📋 Common Interview Questions & How to Answer

### 1. "Tell me about yourself" (2-minute answer)
**Structure**: Present → Past → Future

*"I'm currently [current role/status] with expertise in [key skills]. Previously, I [major achievement]. I'm excited about this role because [why this position]."*

**Your customized answer**:
Based on your resume, emphasize:
- Your technical skills
- Recent projects with measurable impact
- Why you're interested in this specific role

---

### 2. "What's your greatest strength?"
**Formula**: Strength + Evidence + Relevance

Example answers based on your background:
- **Technical Excellence**: "My strength is [specific technical skill]. For example, [specific project where you used this skill and the result]."
- **Problem Solving**: "I excel at debugging complex issues. In my last role, I [specific example with outcome]."

---

### 3. "Tell me about a challenging project"
**STAR Method**:
- **S**ituation: Set the context
- **T**ask: Explain your responsibility
- **A**ction: Describe what you did
- **R**esult: Share the outcome (with metrics!)

Prepare 3-4 STAR stories covering:
- Technical challenge
- Team conflict
- Tight deadline
- Project failure and learning

---

### 4. "Why do you want to work here?"
**Research the company**:
- [ ] Read their About page and mission
- [ ] Check recent news/blog posts
- [ ] Review their products/services
- [ ] Look at employee reviews (Glassdoor)
- [ ] Find connections on LinkedIn

**Answer formula**: Company values + Your skills + Specific excitement

---

### 5. "Where do you see yourself in 5 years?"
**What they're really asking**: Are you committed? Do you have ambition?

**Good answer**: "In 5 years, I see myself having deep expertise in [relevant area], possibly in a [logical next role]. I'm excited about [company name] because [how this role helps you grow]."

---

## 💻 Technical Interview Prep

### Coding Practice:
- [ ] Review data structures (arrays, trees, graphs, hash maps)
- [ ] Practice algorithms (sorting, searching, dynamic programming)
- [ ] Study system design basics
- [ ] Review your resume projects in detail
- [ ] Prepare to explain your code decisions

### Platforms for Practice:
- LeetCode (Easy → Medium problems)
- HackerRank
- CodeSignal
- Project Euler

### Your Resume Projects - Be Ready to Discuss:
1. **Technical decisions**: Why did you choose X over Y?
2. **Challenges**: What was the hardest part?
3. **Trade-offs**: What would you do differently?
4. **Metrics**: What was the impact?

---

## 🎯 Behavioral Questions

Prepare examples for:
- Leadership
- Conflict resolution
- Failure and learning
- Innovation
- Time management
- Team collaboration

---

## ❓ Questions to Ask Them

### About the Role:
- "What does success look like in this role in the first 90 days?"
- "What are the biggest challenges facing the team right now?"
- "How does this role contribute to the company's goals?"

### About the Team:
- "Can you tell me about the team structure?"
- "What's the team's working style and culture?"
- "How does the team handle code reviews and collaboration?"

### About Growth:
- "What opportunities are there for professional development?"
- "How does the company support learning new technologies?"
- "What's the typical career path for this role?"

### About the Company:
- "What excites you most about working here?"
- "How has the company changed in the past year?"
- "What are the company's plans for growth?"

---

## 📝 Day Before Interview Checklist

- [ ] **Review your resume** - Know every detail
- [ ] **Research the company** - Recent news, products, culture
- [ ] **Prepare STAR stories** - Write them down
- [ ] **Technical practice** - Do 2-3 coding problems
- [ ] **Prepare questions** - Have 5-7 ready
- [ ] **Test your tech** - Camera, mic, internet (for virtual)
- [ ] **Plan your outfit** - Professional and comfortable
- [ ] **Get good sleep** - 7-8 hours

---

## 🎤 During the Interview

**Do's**:
✅ Smile and make eye contact
✅ Think before you speak
✅ Ask clarifying questions
✅ Show enthusiasm
✅ Take notes
✅ Use the interviewer's name

**Don'ts**:
❌ Badmouth previous employers
❌ Check your phone
❌ Interrupt the interviewer
❌ Give yes/no answers
❌ Discuss salary too early
❌ Appear desperate

---

## 📧 After the Interview

**Send a thank-you email within 24 hours**:

*Subject: Thank you - [Position Title] Interview*

Dear [Interviewer Name],

Thank you for taking the time to speak with me about the [Position Title] role at [Company]. I enjoyed learning about [specific topic discussed] and I'm even more excited about the opportunity to [specific contribution].

Our conversation reinforced my interest in [specific aspect of role/company]. I believe my experience with [relevant skill/project] would allow me to contribute to [team/company goal].

Please let me know if you need any additional information. I look forward to hearing from you.

Best regards,
[Your Name]

---

## 🎯 Final Tips

1. **Practice out loud** - Don't just think through answers
2. **Record yourself** - Watch for filler words and body language
3. **Mock interviews** - Practice with a friend
4. **Stay positive** - Frame everything constructively
5. **Be authentic** - Let your personality show
6. **Follow up** - Send that thank-you email!

**Remember**: The interview is a two-way street. You're also evaluating if this company is right for you!
"""
    
    return prep_guide


def generate_salary_negotiation_guide() -> str:
    """
    Generate salary negotiation tips.
    """
    guide = """
# 💰 Salary Negotiation Guide

## 🎯 Research First

### Before the Offer:
1. **Use salary tools**:
   - levels.fyi (tech salaries)
   - Glassdoor
   - PayScale
   - LinkedIn Salary

2. **Consider total compensation**:
   - Base salary
   - Signing bonus
   - Stock options/RSUs
   - Annual bonus
   - Benefits (health, 401k match, PTO)
   - Remote work options
   - Professional development budget

## 🗣️ The Negotiation

### When They Ask Your Expectations:
**Option 1**: "I'm focused on finding the right role. What's the budgeted range for this position?"

**Option 2**: "Based on my research and experience, I'm looking for something in the $X-Y range, but I'm flexible for the right opportunity."

### When You Get the Offer:
**Never accept immediately!**

Say: "Thank you so much! I'm excited about this opportunity. Can I have [24-48 hours] to review the details?"

### Your Negotiation Email:

*Subject: Re: Offer for [Position Title]*

Dear [Hiring Manager],

Thank you for the offer! I'm excited about joining [Company] and contributing to [specific team/project].

After careful consideration of the role's responsibilities and my research of market rates for similar positions, I'd like to discuss the compensation package.

Based on my [X years] of experience in [relevant skills] and the value I can bring, particularly in [specific area], I was hoping for a base salary of $[your target].

I'm confident I can make significant contributions to [team/company goal], and I believe this adjustment better reflects the value I'll bring.

I'm flexible and open to discussing the complete package. Would you be available for a brief call to discuss this?

Thank you for your consideration.

Best regards,
[Your Name]

## ✅ Do's and Don'ts

### Do:
✅ Negotiate! Most offers expect it
✅ Be specific with numbers
✅ Emphasize your value
✅ Stay professional and positive
✅ Get everything in writing
✅ Consider the full package

### Don't:
❌ Accept immediately
❌ Lie about other offers
❌ Make ultimatums
❌ Get emotional
❌ Only focus on salary
❌ Burn bridges if you decline

## 💡 Pro Tips

1. **Timing matters**: Negotiate after the offer, not during interviews
2. **Have a number**: Know your target salary range
3. **Be ready to walk**: Know your minimum acceptable offer
4. **Anchor high**: Your first number sets the range
5. **Get creative**: If they won't budge on salary, negotiate other benefits
6. **Everything is negotiable**: Signing bonus, start date, remote work, etc.

Remember: The worst they can say is no, and you're still left with the original offer!
"""
    
    return guide


def generate_linkedin_optimization() -> str:
    """
    Generate LinkedIn profile optimization guide.
    """
    guide = """
# 📱 LinkedIn Optimization Guide

## Profile Sections to Optimize:

### 1. Profile Photo
✅ Professional headshot
✅ Smile and make eye contact
✅ Plain background
✅ High resolution
❌ Selfies, group photos, or casual shots

### 2. Headline (120 characters)
**Formula**: Role | Key Skills | Value Proposition

Examples:
- "Senior Software Engineer | Python, AWS, ML | Building Scalable Systems"
- "Data Scientist | ML, AI, Analytics | Turning Data into Insights"

### 3. About Section (2,600 characters)
**Structure**:
- Opening hook (what you do)
- Your story (how you got here)
- Skills and expertise
- What you're looking for
- Call to action

### 4. Experience Section
For each role:
- Use action verbs
- Include metrics and achievements
- Add media (projects, articles, presentations)
- Use keywords naturally

### 5. Skills Section
- Add 50 skills (maximum)
- Put top skills first
- Include variations (ML and Machine Learning)
- Get endorsements

### 6. Recommendations
- Request from managers and colleagues
- Give to receive
- Be specific about what to highlight

## 🎯 Profile Optimization Tips

1. **Keywords**: Use job title keywords throughout
2. **Active**: Post and engage regularly
3. **Open to Work**: Turn on the green badge
4. **Custom URL**: linkedin.com/in/yourname
5. **Featured Section**: Showcase your best work
6. **Certifications**: Add all relevant credentials
7. **Volunteer**: Shows well-roundedness
8. **Languages**: Add any you speak

## 📈 Engagement Strategy

### Post Ideas:
- Share articles about your industry
- Write about lessons learned
- Celebrate team wins
- Share your projects
- Comment on industry trends
- Engage with your network's posts

### Best Times to Post:
- Tuesday-Thursday
- 8-10 AM or 12-2 PM
- Avoid weekends and very early/late hours

## 🤝 Networking

1. **Connect**: Send personalized connection requests
2. **Engage**: Comment meaningfully on posts
3. **Message**: Follow up with new connections
4. **Join**: Participate in relevant groups
5. **Follow**: Companies you're interested in

Remember: LinkedIn is your professional online presence. Keep it current and professional!
"""
    
    return guide