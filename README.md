# 🚀 AWS ECS Fargate CI/CD & Monitoring Demo

A production-grade, highly secure, and fully automated cloud infrastructure deployed on AWS using **Terraform**, **AWS ECS Fargate**, **GitHub Actions OIDC**, and **CloudWatch/SNS Monitoring**.

---

## 🏗️ How It Works

```mermaid
graph TD
    User([End User / Client]) -->|HTTPS Request| ALB[Application Load Balancer]
    
    subgraph Multi-AZ Public Subnets
        ALB
    end
    
    subgraph Multi-AZ Private Subnets
        ALB -->|Route Traffic| ECS1[ECS Fargate Task - AZ1]
        ALB -->|Route Traffic| ECS2[ECS Fargate Task - AZ2]
    end

    subgraph CI/CD Automation
        GHA[GitHub Actions Workflow] -->|OIDC Token Auth| AWS_IAM[AWS IAM Role]
        GHA -->|Build & Push Image| ECR[(Amazon ECR)]
        ECR -->|Deploy Image| ECS1
        ECR -->|Deploy Image| ECS2
    end

    subgraph Observability & Alerts
        ECS1 -.->|Metrics| CW[CloudWatch Alarms]
        ECS2 -.->|Metrics| CW
        CW -->|Trigger Alert| SNS[Amazon SNS Topic]
        SNS -->|Email Notification| DevSecOps([DevOps Team])
    end

    style ALB fill:#f9f,stroke:#333,stroke-width:2px
    style ECR fill:#bbf,stroke:#333,stroke-width:2px
    style CW fill:#ffe,stroke:#333,stroke-width:2px
