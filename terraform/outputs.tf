output "alb_dns_name" {
  description = "The URL of the Application Load Balancer to access the web app"
  value       = aws_lb.main.dns_name
}
