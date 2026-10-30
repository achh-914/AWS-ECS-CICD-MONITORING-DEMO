<div align="center">

# 🚀 AWS ECS Fargate: CI/CD & Monitoring

**Keyless, fully automated container delivery on AWS, provisioned as code.**

![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform&logoColor=white)
![AWS ECS](https://img.shields.io/badge/AWS-ECS%20Fargate-FF9900?logo=amazonaws&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-OIDC-2088FF?logo=githubactions&logoColor=white)
![CloudWatch](https://img.shields.io/badge/CloudWatch-SNS%20Alerts-E7157B?logo=amazoncloudwatch&logoColor=white)
![Region](https://img.shields.io/badge/Region-eu--west--1-232F3E)

</div>

---

## 📌 Overview

A production-style reference implementation that takes a containerized web app from `git push` to a **highly available, monitored deployment on AWS ECS Fargate**. Infrastructure is 100% Terraform, authentication is 100% keyless (GitHub OIDC), and failures are reported by email before users notice.

| | |
|---|---|
| **Compute** | AWS ECS Fargate (serverless containers), 2 Availability Zones |
| **Networking** | Custom VPC, public subnets (ALB), private subnets (tasks) |
| **CI/CD** | GitHub Actions with OIDC, no stored AWS keys |
| **Registry** | Amazon ECR |
| **Observability** | CloudWatch Alarms, SNS email notifications |
| **IaC** | Terraform |

---

## 💡 The Problem & The Solution

Small teams often deploy by hand: build an image on a laptop, copy it to a server, paste secrets into config files, and find out the app is down when a customer complains.

| Before | After |
|---|---|
| Manual deploys | Every push to `main` builds, tests, and deploys automatically |
| AWS access keys stored in CI | Short-lived credentials via GitHub OIDC (no stored keys) |
| Click-built infrastructure | Everything defined in Terraform and reproducible |
| "We'll notice if it breaks" | CloudWatch alarms send an email through SNS |

---

## 🏗️ Architecture

```mermaid
flowchart TB
    User([End User / Client])

    subgraph CICD["CI/CD Automation"]
        GH[GitHub Actions Workflow]
        IAM[AWS IAM Role]
        ECR[(Amazon ECR)]
    end

    subgraph VPC["AWS VPC - eu-west-1"]
        subgraph PUB["Multi-AZ Public Subnets"]
            ALB[Application Load Balancer]
        end
        subgraph PRIV["Multi-AZ Private Subnets"]
            T1[ECS Fargate Task - AZ1]
            T2[ECS Fargate Task - AZ2]
        end
    end

    subgraph OBS["Observability and Alerts"]
        CW[CloudWatch Alarms]
        SNS[Amazon SNS Topic]
        OPS([DevOps Team])
    end

    GH -->|OIDC Token Auth| IAM
    GH -->|Build and Push Image| ECR
    ECR -.->|Deploy Image| T1
    ECR -.->|Deploy Image| T2
    User -->|HTTPS Request| ALB
    ALB -->|Route Traffic| T1
    ALB -->|Route Traffic| T2
    T1 -.->|Metrics| CW
    T2 -.->|Metrics| CW
    CW -->|Trigger Alert| SNS
    SNS -->|Email Notification| OPS
```

**How to read it**

- 🔵 **Delivery path:** GitHub Actions authenticates to AWS through OIDC, builds the image, and pushes it to ECR. ECS pulls it and rolls out the new tasks.
- 🟢 **Request path:** users reach the Application Load Balancer in the public subnets. The ALB forwards traffic to Fargate tasks in private subnets across two AZs.
- 🔴 **Alert path:** task metrics feed CloudWatch Alarms. When an alarm fires, SNS emails the DevOps team.

---

## 🔄 CI/CD Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant GH as GitHub Actions
    participant AWS as AWS IAM (OIDC)
    participant ECR as Amazon ECR
    participant ECS as ECS Fargate

    Dev->>GH: git push to main
    GH->>AWS: Request OIDC token
    AWS-->>GH: Short-lived credentials
    GH->>ECR: Build and push image
    GH->>ECS: Update service
    ECS->>ECR: Pull new image
    ECS-->>GH: Deployment complete
```

---

## 🔐 Security by Design

| Control | Implementation |
|---|---|
| **No long-lived secrets** | GitHub OIDC replaces static AWS access keys |
| **Network isolation** | Tasks run in private subnets with no public IP |
| **Single entry point** | Only the ALB is internet-facing |
| **Least privilege** | The CI role is limited to what the pipeline needs |
| **Resilience** | Tasks spread across two Availability Zones |

---

## 📊 Monitoring & Alerting

```mermaid
flowchart TB
    T1[ECS Fargate Task - AZ1] -.->|Metrics| CW[CloudWatch Alarms]
    T2[ECS Fargate Task - AZ2] -.->|Metrics| CW
    CW -->|Trigger Alert| SNS[Amazon SNS Topic]
    SNS -->|Email Notification| OPS([DevOps Team])
```

Alarms watch service health. When a threshold is breached, SNS sends an email so the team reacts before customers report the issue.

---

## 📁 Repository Structure

```text
.
├── .github/workflows/    # CI/CD pipeline
├── app/                  # Application source and Dockerfile
├── terraform/            # VPC, ALB, ECS, ECR, IAM, CloudWatch, SNS
└── README.md
```

---

## ⚡ Quick Start

**Prerequisites:** AWS account, AWS CLI, Terraform, Docker, a GitHub repository.

```bash
cd terraform
terraform init
terraform validate
terraform plan
terraform apply
```

Push to `main` to trigger the pipeline:

```bash
git push origin main
```

**Tear down** (to avoid unnecessary costs):

```bash
cd terraform && terraform destroy
```

---

## 🗺️ Roadmap

- [ ] HTTPS with ACM certificate and custom domain
- [ ] Auto Scaling on CPU and request count
- [ ] Remote Terraform state (S3 + locking)
- [ ] Container and IaC security scanning in CI
- [ ] Blue/green deployments

---

## 👥 Authors

[@achh-914](https://github.com/achh-914) · [@meriem-achh](https://github.com/meriem-achh)
