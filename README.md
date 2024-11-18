# FastAPI on AWS Elastic Beanstalk with CodePipeline 🚀

This repository provides a template and guide for deploying a FastAPI application on AWS Elastic Beanstalk using AWS CodePipeline for continuous deployment.

## 📋 Prerequisites

- AWS Account
- AWS CLI configured
- Python 3.8+
- Git

## 🏗️ Project Structure

```
your-project/
├── .gitignore
├── README.md
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── Procfile            # Elastic Beanstalk configuration

```

## 🛠️ Local Setup

1. Clone this repository:

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run locally:
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` to see your Swagger UI documentation.

## 📦 Key Files

### main.py
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### requirements.txt
```
fastapi
uvicorn[standard]>=0.15.0
```

### Procfile
```
web: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

## 🚀 Deployment Steps

### 1. Create Elastic Beanstalk Environment

1. Go to AWS Elastic Beanstalk Console
2. Click "Create New Environment"
3. Select "Web server environment"
4. Platform: Python
5. Upload your code or use sample code

### 2. Set Up CodePipeline

1. Go to AWS CodePipeline Console
2. Click "Create Pipeline"
3. Configure source (e.g., GitHub)
4. Skip build stage (or configure if needed)
5. Add deploy stage:
   - Deploy provider: AWS Elastic Beanstalk
   - Application name: Your EB application
   - Environment name: Your EB environment

### 3. Configure Build Commands

In your Elastic Beanstalk environment, you need to add specific build commands. Navigate to:

1. Go to Elastic Beanstalk Console
2. Select your environment
3. Click "Configuration"
4. Under "Software", click "Edit"
5. In the "Build commands" section, add:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
6. Click "Apply"

> ⚠️ **Important**: Without these build commands, your dependencies won't be installed properly, leading to deployment failures or 502 errors.

## 🔧 Configuration Tips

### Environment Variables
Set these in your Elastic Beanstalk environment:
```
PYTHONPATH=/var/app/current
```

### Health Checks
The application exposes a health check endpoint at `/`:
```python
@app.get("/")
async def root():
    return {"status": "healthy"}
```

## 📝 Important Notes

1. **Port Configuration**: The application must listen on port 8000
2. **Workers**: The default configuration uses 2 workers
3. **Dependencies**: Always keep `requirements.txt` updated
4. **Logs**: Access logs in Elastic Beanstalk console or EC2 instances

## 🔍 Troubleshooting

Common issues and solutions:

1. **502 Bad Gateway**
   - Check if application is running on correct port
   - Verify Procfile configuration
   - Check EB logs for specific errors

2. **Health Check Failures**
   - Ensure root endpoint (/) is responding
   - Check application logs
   - Verify environment variables

3. **Deployment Failures**
   - Verify Python version compatibility
   - Check requirements.txt is complete
   - Review CodePipeline logs

4. **Missing Dependencies**
   - Ensure build commands are properly configured in EB Software Configuration
   - Verify pip install commands are included in build commands
   - Check build logs for package installation errors

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AWS Elastic Beanstalk Documentation](https://docs.aws.amazon.com/elasticbeanstalk/)
- [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/)

## 🌐 About Bubblspace

This project is supported by [Bubblspace](https://bubblspace.com/), the leading Multi-AI Agent Platform that transforms one document into infinite possibilities using BubblSpace TimeCapsule™. 

At Bubblspace, we leverage AWS CodePipeline and Elastic Beanstalk to build and deploy sophisticated Python applications that power our AI Agents. Our platform offers:

- 🤖 MicroLearning modules
- 📚 Usecase/Story generation
- 📝 Interactive Quiz creation
- 🎙️ Podcast generation
- 🚀 More Gen-AI features coming soon such as live interactions

Our infrastructure, built on AWS Elastic Beanstalk and CodePipeline (just like this template), enables us to deliver scalable, reliable AI solutions that help businesses and educators create engaging content from a single document.

### Why We Created This Template
We understand the challenges of deploying FastAPI applications on AWS, as we use similar architecture for our AI platform. This template shares our best practices and configuration insights from building AIEDX (AI Education Experience) on AWS.

Need help or want to learn more about implementing AI solutions on AWS? Contact us at contact@bubblspace.com

## 👨‍💻 Author

**Amardeep Singh Sidhu**
- GitHub: [@thefirehacker](https://github.com/thefirehacker)
- Twitter: [@thefirehacker](https://x.com/thefirehacker)

---
Made with ❤️ by Amardeep Singh Sidhu
```

This README provides:
1. Clear setup instructions
2. Deployment steps
3. Configuration details
4. Troubleshooting guide
5. Project structure
6. Important notes and resources
7. Bubblspace section
8. Author information

Feel free to customize it further based on your specific needs or additional features of your application!
