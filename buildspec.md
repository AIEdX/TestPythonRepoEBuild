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
      - echo "Dependencies installed successfully"
      - ls -la  # List files for verification
  post_build:
    commands:
      - echo "Build completed"

artifacts:
  files:
    - '**/*'