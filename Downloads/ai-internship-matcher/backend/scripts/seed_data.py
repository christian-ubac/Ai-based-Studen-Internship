"""
Seed data for AI Internship Matcher database.
Contains realistic AI/ML internship listings and sample student profiles.
"""

DEPARTMENTS = [
    {
        "name": "AI Research & Development",
        "program_focus": "Artificial Intelligence",
        "description": """Join our AI R&D team to work on cutting-edge machine learning projects. 
        You'll be involved in developing and training models, conducting experiments, and implementing 
        state-of-the-art AI algorithms. Great opportunity to work with large language models and 
        computer vision systems.""",
        "required_skills": "python,pytorch,tensorflow,machine learning,deep learning,neural networks,data analysis"
    },
    {
        "name": "Natural Language Processing",
        "program_focus": "NLP/ML",
        "description": """Work on advanced NLP projects including sentiment analysis, 
        text classification, and language generation. Help improve our language models and 
        develop new text processing pipelines.""",
        "required_skills": "python,nltk,spacy,transformers,bert,machine learning,nlp"
    },
    {
        "name": "Computer Vision Lab",
        "program_focus": "Computer Vision",
        "description": """Research and develop computer vision applications including object detection,
        image segmentation, and visual recognition systems. Work with latest CV models and contribute
        to real-world applications.""",
        "required_skills": "python,opencv,pytorch,CNN,image processing,deep learning,cuda"
    },
    {
        "name": "MLOps & Infrastructure",
        "program_focus": "ML Engineering",
        "description": """Help build and maintain our ML infrastructure. Work on model deployment,
        monitoring, and optimization. Experience with cloud platforms and containerization.""",
        "required_skills": "python,docker,kubernetes,aws,mlflow,git,ci/cd"
    },
    {
        "name": "Data Science & Analytics",
        "program_focus": "Data Science",
        "description": """Apply statistical analysis and machine learning to solve real business
        problems. Work with big data tools and develop predictive models.""",
        "required_skills": "python,sql,pandas,scikit-learn,statistics,data visualization,spark"
    }
]

STUDENTS = [
    {
        "name": "Alex Chen",
        "email": "alex.chen@university.edu",
        "program": "Computer Science",
        "gpa": 3.8,
        "protected_age": 22
    },
    {
        "name": "Sarah Johnson",
        "email": "sarah.j@university.edu",
        "program": "Data Science",
        "gpa": 3.9,
        "protected_age": 21
    },
    {
        "name": "Mohammed Ali",
        "email": "m.ali@university.edu",
        "program": "Artificial Intelligence",
        "gpa": 3.7,
        "protected_age": 23
    }
]

# Sample resume text (will be extracted from PDF)
SAMPLE_RESUME_TEXT = '''
ALEX CHEN
Machine Learning Engineer

EDUCATION
University of Technology
B.S. in Computer Science, Expected May 2026
GPA: 3.8/4.0

SKILLS
Programming: Python, Java, C++
Machine Learning: PyTorch, TensorFlow, Scikit-learn
Tools: Git, Docker, Linux
Languages: English (Native), Mandarin (Fluent)

PROJECTS
Sentiment Analysis System
- Developed BERT-based sentiment classifier achieving 92% accuracy
- Implemented real-time processing pipeline using Flask and Redis
- Deployed model using Docker containers

Object Detection App
- Built YOLOv5-based object detection system for mobile devices
- Optimized model performance using TensorRT
- Achieved 30 FPS on edge devices

EXPERIENCE
ML Research Assistant
University AI Lab
- Conducted experiments with transformer architectures
- Published paper on efficient attention mechanisms
- Mentored junior students in deep learning projects

SOFTWARE ENGINEERING INTERN
Tech Solutions Inc.
- Developed microservices using Python and FastAPI
- Implemented CI/CD pipelines using GitHub Actions
- Optimized database queries improving performance by 40%

ACHIEVEMENTS
- 1st Place, University ML Competition 2024
- Published paper at Regional AI Conference
- President, AI Student Society
'''