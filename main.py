import os
import re
import ast
import shutil
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
import string
import ollama

# Fist execution is necessery uncoment those lines, then you can comment again. 
# nltk.download('punkt')
# nltk.download('stopwords')

def experienceFunc(keywords, context, whatIdid):
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f"""
    You are an expert resume writer with over 20 years of experience. I'm writing a bullet point 
    for an experience on my resume. But I don't know how my success was measured.
    I will describe my responsabilities, the job description and your task is to list 5 relevant 
    metrics that i can include to quantify the impact of my work, do not include numbers in percentage or 
    statistics and also trying associate to use the relevant key works that i'll provaide to you: 

    keywords: {keywords}

    Here's what I did: {whatIdid}

    Here's the the job description: {context}

    Please provide the answer in a python list, all I expect is ["answer fort bullet 1", "answer fort bullet 2", "answer fort bullet 3", "answer fort bullet 4", "answer fort bullet 5"].
    Please, avoid Buzzwords!
    """
        },
    ])

    ansewrAI = str(response['message']['content'])

    padrao = r'\[(.*?)\]'
    resultado = re.findall(padrao, ansewrAI, re.DOTALL)

    if resultado:
        lista_filtrada = resultado[0] 
        lista_filtrada = ast.literal_eval(f'[{lista_filtrada}]')
    else:
        lista_filtrada = ["not genereted"]
        print("List not found")

    formatted_output = """
    \\resumeSubHeadingList
    {}
    \\resumeSubHeadingListEnd
    """.format("\n".join([f"  \\resumeItem{{\\textbullet\\ {metric}}}" for metric in lista_filtrada]))

    return formatted_output
#----------------

"""
    INPUT section
"""
company = "XPTO.co"
job_title = "Senior Software Engineer"
context_vacancy = "working with projects in the context of Senior Software Engineer"

# create project folder
folderName = f"{company}-{job_title}"
os.makedirs(folderName, exist_ok=True)

# context of the vacancy
context = """
XPTO.co aspires to be the global cloud compliance platform. Our ambitious mission is to build out our global, multi-cloud SaaS solution to scale to support all global transactions while providing highest levels of resiliency and performance. The AvaTax Engineering team at XPTO.co is responsible for designing, building and supporting our flagship determinations platform. 

You, as a Senior Software Engineer at XPTO.co, will be hands-on as part of the core AvaTax engineering team responsible for designing and driving a highly scalable, reliable, secure and performant global tax calculation engine. You will be part of the team that will drive, strategize and provide a path to build and deploy a highly distributed, multi-cloud solution integrating an ecosystem of services and data components.  A successful candidate will be a well-rounded software development engineer with a proven track record of building and executing engineering solutions working in an Agile environment. 

We are looking for a highly skilled and motivated Senior Software Engineer to join our development team and design and build components for our innovative tax compliance solutions. 

Lead the design and overall software development lifecycle for a set of core roadmap items
Participate in systemwide architecture discussions and facilitate integrations across engineering teams
Develop custom APIs and middleware to facilitate data exchange, synchronization, and real-time communication between different systems.
Implement robust error handling, data validation, and data transformation mechanisms to ensure data integrity and accuracy during integration processes
Optimize integration performance and scalability to accommodate a growing number of clients and increasing data volumes
Design and implement new features and maintain existing functionalities
Build and lead POCs to demonstrate technical feasibility
Focus on security aspects, observability, scalability, and telemetry
Perform code reviews and ensure coding standards and practices are followed
Implement and follow agile/scrum processes
Collaborate with other teams to solve cross functional challenges 
Optimize code to improve application efficiency
Bachelor/master's degree in computer science or equivalent 
Good understanding of Object-oriented programming languages 
Good understanding of eCommerce system architectures, APIs, data models, and authentication mechanisms. 
Good experience with RESTful APIs, JSON, XML, and other data interchange formats. 
Familiarity with authentication protocols like OAuth and token-based authentication. 
Experience in working in an Agile team with hands on with TDD, BDD 
Excellent problem-solving skills and a demonstrated ability to navigate complex technical challenges. 
Experience of working on AWS Cloud and DevOps (Terraform, Docker, ECS, etc.) would be beneficial. 
Excellent analytical and troubleshooting skills to be able to solve complex problems and critical production issues. 
Proven track record of delivering high-quality software projects on time. 
It is a position with international interaction teams only resumes sent in English will be considered.

"""
#------------------------------------------------
"""
    Processisng workds 
     - analysis of the most used words in the job description
"""
tokens = word_tokenize(context)
tokens = [word for word in tokens if word.isalnum()]
tokens = [word.lower() for word in tokens]
stop_words = set(stopwords.words('english'))
tokens = [word for word in tokens if word not in stop_words]
ps = PorterStemmer()
tokens = [ps.stem(word) for word in tokens]
freq_dist = FreqDist(tokens)
keywords = freq_dist.most_common(10)
#------------------------------------------------
"""
    Summary
"""
print("creating sumary")
response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': f"""
            You are an expert resume writer with over 20 years of experience. 
            Your task is to write a compelling summary for my resume based on the provided context and job description. 
            Please integrate the relevant keywords provided. Do not include numerical data or statistics. 
            The final summary should be no more than 5 lines and should be highly tailored to make me stand out to recruiters. 
            Return the summary as a Python list with a single item.
            Please, avoid Buzzwords! 

            Keywords: {keywords}

            Here's about myself in my own words: 
            [HERE GOES YOUR EXPERIENCE] Ex.:A passion for coding with Python since starting mechanical engineering fueled my studies, leading to early graduation. 
            Motivated by the potential of VR in industrial training, I leveraged my master's research on industrial robotics software 
            to create a VR tool, empowering operators. I'm a passionate sports enthusiast and a driven professional, and I bring the same 
            competitive spirit and commitment to excellence to my work. Just like in sports, I'm always striving to improve my skills, expand 
            my knowledge, and deliver exceptional results. Whether it's staying up-to-date on industry trends or taking on new challenges, I 
            approach every task with the same determination and focus that I bring to the playing field. I foster a culture of open communication. 
            I believe in leveraging the collective power of the team, and my clear communication style helps us achieve our goals together. 

            Job Description: {context}

            Provide the summary as a Python list with a single item. All I expect is ["summary"]
            Please, avoid Buzzwords! Do not use timeframes. Do not use percentage simbol. 
        """
    },
])

summary = str(response['message']['content'])
padrao = r'\[(.*?)\]'
resultado = re.findall(padrao, summary, re.DOTALL)
if resultado:
    lista_filtrada = resultado[0] 
    lista_filtrada = ast.literal_eval(f'[{lista_filtrada}]')
else:
    lista_filtrada = ["not genereted"]
pathSummary = os.path.join(folderName, "summary.tex")
with open(pathSummary, 'w') as arquivo:
    arquivo.write(lista_filtrada[0])

"""
    Experiences
"""
#experience_one
print("creating experience_one experience ...")
whatIdid = """
    I provided consultancy on robotics and industrial automation to the company's board of directors. Many 
    of the discussed projects were successfully implemented, with some still under my supervision. For 
    instance, I oversaw the implementation of RFID cards for rapid identification of sterilization kits, 
    significantly reducing the time for locating and processing these products. Integrating this technology 
    with the company's IT infrastructure resulted in a substantial reduction in equipment processing time. 
"""
experience_one = experienceFunc(keywords, context, whatIdid)
pathBioxxi = os.path.join(folderName, "experience_one.tex")
with open(pathBioxxi, 'w') as arquivo:
    arquivo.write(experience_one)

#experience_two
print("creating experience_two experience ...")
whatIdid = """
    Provide support and guidance to engineers during routine maintenance procedures for electrical 
    networks and equipment; Administrative support, including the accurate and efficient population 
    of company databases with data, to streamline and optimize operations;
"""
experience_two = experienceFunc(keywords, context, whatIdid)
pathExperience_two = os.path.join(folderName, "experience_two.tex")
with open(pathExperience_two, 'w') as arquivo:
    arquivo.write(experience_two)


#------------------------------------------------
"""
    Generete folder and file.tex
"""

# create notes
timestamp = datetime.now().strftime("%Y-%m-%d %Hh %Mmin %Sseg")
timestamp = timestamp.replace(":", "-")

notes = f"{company}-{job_title} {timestamp}.txt"

textos = [summary, experience_one, experience_two]
pathNotes = os.path.join(folderName, notes)
with open(pathNotes, 'w') as arquivo:
    for text in textos:
        arquivo.write(text + '\n\n')

# copia template.txt para dentro e pasta e renomeias
rootPath = os.path.join(os.getcwd(), "template.txt")
pathTemplate = os.path.join(folderName, "YourName.tex")
shutil.copy(rootPath, pathTemplate)

print("!!! curriculum ready \o/  !!!")

#--------------------------------------------------
"""
    Cover Letter
"""
print("----Init Cover Letter")
print("----Creating couver letter base")
rootPath = os.path.join(os.getcwd(), "coverLetter.txt")
pathTemplate = os.path.join(folderName, "YourName_coverLetter.tex")
shutil.copy(rootPath, pathTemplate)

# basic text to cover letter: 
print("----Creating base text of cover letter start")
baseText_start = f"I am writing to express my interest in the {job_title} position at {company}, as advertised. With a solid background in engineering and over 7 years of experience in software development, I believe that my skills and passion for creating innovative solutions make me an ideal candidate for this role."
pathbaseText_start = os.path.join(folderName, "baseText_start.tex")
with open(pathbaseText_start, 'w') as arquivo:
    arquivo.write(baseText_start)

print("----Creating base text of cover letter end")
baseText_start_end = f"Thank you for your consideration, and I am available to discuss how I can contribute to the continued success of {company}. I have attached my resume for your review and look forward to the opportunity to speak with you soon."
pathbaseText_end = os.path.join(folderName, "baseText_end.tex")
with open(pathbaseText_end, 'w') as arquivo:
    arquivo.write(baseText_start_end)

print("----Creating couver target job")
pathJobTitle = os.path.join(folderName, "targetjob.tex")
with open(pathJobTitle, 'w') as arquivo:
    arquivo.write(job_title)

print("----Creating experience paragraph")
response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': f"""
            I am writing a cover letter.
            I need to write a paragraph to highlight my experience.
            Here is a paragraph template: In my previous experience at company xxx, I had the opportunity to 
            lead several software development projects, where I applied agile methodologies and test-driven 
            development (TDD) techniques to ensure the delivery of high-quality products. My experience 
            includes working with a variety of programming languages, such as Java, Python, and C++, and 
            with frameworks like React and Angular. Additionally, my ability to solve complex problems and 
            my skill in working effectively in a team were fundamental to the success of the projects I led.
            This is my experience:(
                Education:
                Pos-Graduation in Artificial Intelligence and Machining Learning
                2022-2023 - Pontifical Catholic University of Minas Gerais (PUC Minas)
                2016-2018 - Military Engineer Institute(IME), Rio de Janeiro, Brazil
                Mechanical Engineer 
                - 2010-2014 - University of Rio de Janeiro Estate (UERJ)
                Work Experience:                
                experience_one - Automation Consultant - dec. 2017 - jun. 2018 - Rio de Janeiro, Brasil - 
                    I provided consultancy on robotics and industrial automation to the company's board of directors. Many of the
                    discussed projects were successfully implemented, with some still under my supervision. For instance, I oversaw 
                    the implementation of RFID cards for rapid identification of sterilization kits, significantly reducing the 
                    time for locating and processing these products. Integrating this technology with the company's IT 
                    infrastructure resulted in a substantial reduction in equipment processing time.	
                experience_two - Israel Electric Company - Trainee - nov. 2015 - mar. 2016 - Jerusalem, Israel - 
                    Provide support and guidance to engineers during routine maintenance procedures for electrical networks 
                    and equipment; Administrative support, including the accurate and efficient population of company databases 
                    with data, to streamline and optimize operations;        
                )
            The position I am applying for is: {context_vacancy}

            Your task is to rewrite the template paragraph based on my experience, focusing on the position I am applying for.
            I need this paragraph inside a python list like this: ["the paragraph goes here"].
            Do not use Buzzwords.
            Do not include numerical data or statistics.
    """       
    },
])
ansewrAI_experience = str(response['message']['content'])

padrao = r'\[(.*?)\]'
resultado = re.findall(padrao, ansewrAI_experience, re.DOTALL)

if resultado:
    lista_filtrada = resultado[0] 
    lista_filtrada = ast.literal_eval(f'[{lista_filtrada}]')
else:
    lista_filtrada = ["not genereted"]
    print("List not found")

formatted_output_experience = f"{lista_filtrada[0]}"

pathText = os.path.join(folderName, "experience.tex")
with open(pathText, 'w') as arquivo:
    arquivo.write(formatted_output_experience)

print("-----Creating motivation paragraph")
response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': f"""
            I am writing a cover letter.
            I need to write a paragraph to highlight my motivation.
            Here is a paragraph template: The {company} is known for its innovation and commitment to excellence, and I am excited about the prospect of contributing to your team. I am particularly interested in {context_vacancy}, and I believe that my skills in [mention relevant skills or technologies related to the job] will be a valuable addition to your team.
            Here is about the company: {context}
            The position I am applying for is: {context_vacancy}

            Your task is to rewrite the template paragraph based on the company context, focusing on the position I am applying for and showing motivation with the application.
            I need this paragraph inside a python list like this: ["the paragraph goes here"].
            Do not use Buzzwords.
            Do not include numerical data or statistics.
    """       
    },
])
ansewrAI_motivation = str(response['message']['content'])

padrao = r'\[(.*?)\]'
resultado = re.findall(padrao, ansewrAI_motivation, re.DOTALL)

if resultado:
    lista_filtrada = resultado[0] 
    lista_filtrada = ast.literal_eval(f'[{lista_filtrada}]')
else:
    lista_filtrada = ["not genereted"]
    print("List not found")

formatted_output_motivation = f"{lista_filtrada[0]}"

pathText = os.path.join(folderName, "motivation.tex")
with open(pathText, 'w') as arquivo:
    arquivo.write(formatted_output_motivation)

print('Obbaaa')


