from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# Content for the resume
resume_content = '''
[Your Name]
[Your Contact Information: Phone Number and Email Address]
[Your Address]

Summary:
Self-taught Software Engineer with a strong passion for coding and a solid foundation in [Your Technical Skills]. Demonstrated ability to design, develop, and deploy software applications through self-directed learning and personal projects. Skilled in [Programming Languages, Frameworks, and Tools] with a keen eye for detail and a drive for continuous learning. Excited to leverage my skills and experience to contribute to a dynamic software development team.

Skills:
- Proficient in [Programming Languages, Frameworks, and Tools] through self-directed learning
- Solid understanding of data structures, algorithms, and software development principles
- Strong problem-solving skills with the ability to troubleshoot and debug complex code
- Experience with [Database Management Systems, Web Development, etc.]
- Familiarity with [Agile methodologies/SDLC/Version control]
- Excellent communication and collaboration skills

Work Experience:
[Project Name], [Month Year - Present]
- Developed [Specific Features/Functionality] for [Project Description] using [Technologies/Tools].
- Collaborated with team members to optimize code performance and ensure software quality.
- Successfully delivered [Project Milestones/Results] within project timelines.

[Personal Project Name], [Month Year - Month Year]
- Independently designed and developed [Project Description] using [Technologies/Tools].
- Implemented [Specific Features/Functionality] resulting in [Achievements/Impact].
- Leveraged [Emerging Technologies/Tools] to optimize performance and improve user experience.

Education:
Self-taught through online resources, tutorials, and personal projects

Certifications:
- [Certification Name], [Certifying Organization], [Year]

Languages:
- Fluent in [Languages]

Interests:
- [Hobbies/Interests related to your field or technology]

References:
Available upon request
'''

# Create a list to hold the flowables
resume = []

# Set up stylesheet
styles = getSampleStyleSheet()
normal_style = styles['Normal']
heading_style = styles['Heading1']

# Add resume content as paragraphs
resume.append(Paragraph('Resume', heading_style))
resume.append(Spacer(1, 12))
resume.append(Paragraph(resume_content, normal_style))

# Create a landscape letter-sized page
doc = SimpleDocTemplate("resume.pdf", pagesize=landscape(letter))

# Add the resume flowables to the document
doc.build(resume)

pw: $hf3P3X76l8s
