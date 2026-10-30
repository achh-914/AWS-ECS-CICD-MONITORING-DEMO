# AWS ECS Fargate: CI/CD & Monitoring

Automated, keyless deployment of a containerized web app to AWS ECS Fargate with Terraform, GitHub Actions (OIDC), and CloudWatch/SNS alerting.

---

## 💡 The Problem & The Solution

Small teams often deploy by hand: build an image on a laptop, copy it to a server, paste secrets into config files, and find out the app is down when a customer complains.

This project replaces that with:

| Before | After |
| :--- | :--- |
| **Manual deploys** | Every push to `main` builds, tests, and deploys automatically |
| **AWS access keys stored in CI** | Short-lived credentials via GitHub OIDC (no stored keys) |
| **Click-built infrastructure** | Everything defined in Terraform and reproducible |
| **"We'll notice if it breaks"** | CloudWatch alarms send an email through SNS |

---

## 🏗️ Architecture

```mermaid
flowchart LR
    Dev([Developer]) -->|git push| GH[GitHub Actions]
    GH --> GA[GitHub Actions Runner]
    GA -->|OIDC: temporary credentials| IAM[AWS IAM Role]
    GA -->|build and push image| ECR[(Amazon ECR)]
    GA -->|update service| ECS[ECS Fargate]

    subgraph AWS [AWS Region: eu-west-1]
        User([User]) -->|HTTP/HTTPS| ALB[Application Load Balancer]
        ALB --> ECS
        ECR -.->|image pull| ECS
        ECS -->|logs| CWL[CloudWatch Logs]
        CWL --> ALM[CloudWatch Alarms]
        ALM --> SNS[SNS Topic]
    end

    SNS -->|email| Ops([On-call email])
