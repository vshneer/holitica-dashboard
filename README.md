# Holitica Portfolio
Data analysis | E-Commence | Customer behaviour

## Running locally with Docker

Build the image and start the Streamlit server:

```bash
docker build -t holitica-dashboard .
docker run -p 8501:8501 holitica-dashboard
```

The application will be available at `http://localhost:8501`.

## Continuous Deployment

A GitHub Actions workflow (`.github/workflows/deploy.yml`) builds the Docker
image and pushes it to an AWS Elastic Container Registry (ECR) on every push to
the `main` branch. To enable this workflow configure the following secrets in
your GitHub repository:

- `AWS_ACCOUNT_ID` – your AWS account number
- `AWS_REGION` – the AWS region where the ECR repository lives
- `AWS_ROLE_TO_ASSUME` – IAM role that the workflow can assume to push to ECR

Once pushed, the image can be deployed using AWS services such as ECS or
Elastic Beanstalk.
