# Curriculum AI

Curriculum AI? Yes, I created a script to generate your resume in seconds using LLM, customizing your data for the job you want to apply for.

## Getting Started

To make it work, we need to set up your environment. You will need:

- Python 3
- Llama 3
- MiKTeX

### Installing Python

Installing Python is simple. Just download the version you need from: [https://www.python.org/](https://www.python.org/).

### Installing Llama 3

Llama 3 is also straightforward. Go to [https://ollama.com/](https://ollama.com/) and download the Ollama manager executable. Once installed, visit [https://ollama.com/library](https://ollama.com/library) and choose the LLM model you want to use. I recommend the Llama 3.1 8B, which is the one I used to generate my resumes.

### Installing MiKTeX

To install MiKTeX, go to [https://miktex.org/](https://miktex.org/), navigate to the download section, and install the TeX package manager.

**Important Installation Step**:  
When prompted, set the option **Install missing packages on-the-fly** to **YES**.

If you skip this step, during the first few runs of TeX, you will need to allow the manager to download the TeX packages required by the template; otherwise, it will not work.

### IDE
I recommend using VSCode with the extension: LaTeX Workshop.
Otherwise, use a LaTeX editor like TeXstudio, for example.

### python libs
The versions of the external libs I used are in the requirements.txt file

## Instructions

### Step 1: Adjust Your Data into templates 

First, go to the `template.txt` and `coverLetter.txt` files and adjust your personal data there. Yes, this part is a bit more suited for those familiar with LaTeX. However, after the first execution with the generated PDF, everything will become clearer and more intuitive.

### Step 2: Adjust Your Data to LLM model
Code Sections Overview

- **experienceFunc** - Contains the commands sent to the LLM model, returning what we need.

- **INPUT Section** - Fill in the indicated data.

- **Processing Words Section** - In this section of the code, an analysis of the 10 most used words in the job description will be performed.

- **Summary Section** - Look for the paragraph starting with `[HERE GOES YOUR EXPERIENCE]` and add your summary there. The current paragraph serves as a reference.

- **Experiences Section** - You should add as many experiences as you have in this section of the code. Examples are included in the code.

- **Generate Folder and File.tex Section** - This will create a dedicated folder for this generated version.

- **Cover Letter Section** - Edit according to the example within the field: `"This is my experience"`.

### Step 3: Run the python script 

### Step 4: Run the main file curriculum Latex generated with `YourName.tex`

### Step 5: Run the main file CoverLatter Latex generated with `YourName_coverLetter.tex`


## Authors

- [@rafabrasail](https://github.com/rafabrasail)
