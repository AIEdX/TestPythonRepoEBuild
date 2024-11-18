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

### 3. Configure BuildSpec

This template uses AWS CodeBuild with a `buildspec.yml` file to manage dependencies:

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.x
  pre_build:
    commands:
      - echo "Starting pre-build phase"
      - python --version
  build:
    commands:
      - echo "Installing dependencies"
      - pip install -r requirements.txt
      - echo "Creating dependencies directory"
      - mkdir -p dependencies
      - pip install -r requirements.txt -t dependencies/
      - echo "Dependencies installed successfully"
      - ls -la
  post_build:
    commands:
      - echo "Build completed"

artifacts:
  files:
    - '**/*'
    - 'dependencies/**/*'
  base-directory: '.'
```

> ⚠️ **Important**: This buildspec.yml ensures all dependencies are properly packaged with your application.

## 🧪 Testing API Endpoints

### Using cURL

1. Health Check:
```bash
curl http://localhost:8000/
```

2. Create User:
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "password123"
  }'
```

3. Get All Users:
```bash
curl http://localhost:8000/users/
```

4. Get Specific User:
```bash
curl http://localhost:8000/users/1
```

### Using Postman

1. **Health Check**
   - Method: `GET`
   - URL: `http://localhost:8000/`
   - No headers or body required

2. **Create User**
   - Method: `POST`
   - URL: `http://localhost:8000/users/`
   - Headers:
     ```
     Content-Type: application/json
     ```
   - Body (raw JSON):
     ```json
     {
       "email": "test@example.com",
       "username": "testuser",
       "full_name": "Test User",
       "password": "password123"
     }
     ```

3. **Get All Users**
   - Method: `GET`
   - URL: `http://localhost:8000/users/`
   - No headers or body required

4. **Get Specific User**
   - Method: `GET`
   - URL: `http://localhost:8000/users/1`
   - No headers or body required

### Expected Responses

1. **Health Check Response**:
```json
{
    "status": "healthy",
    "timestamp": "2024-02-18T12:34:56.789Z",
    "service": "FastAPI AWS Template"
}
```

2. **Create User Response**:
```json
{
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "created_at": "2024-02-18T12:34:56.789Z"
}
```

3. **Get All Users Response**:
```json
[
    {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "created_at": "2024-02-18T12:34:56.789Z"
    }
]
```

4. **Error Response Example**:
```json
{
    "error": "Username already registered",
    "status_code": 400,
    "timestamp": "2024-02-18T12:34:56.789Z"
}
```

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
