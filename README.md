# Serverless Contact Form

A production-ready, serverless contact form built on Amazon Web Services (AWS) for a local cake bakery business. Customers can submit custom cake queries, which are automatically stored in DynamoDB, trigger an instant notification email to the bakery owner via Amazon SES, and return a sleek success confirmation popup.

## 🚀 Architecture Flow
1. **Frontend**: Hosted on Amazon S3 (secured via CloudFront / HTTPS).
2. **API Layer**: Amazon API Gateway (`POST /contact`).
3. **Compute**: AWS Lambda (Python `boto3`).
4. **Database**: Amazon DynamoDB (`ContactSubmissions`).
5. **Notifications**: Amazon SES (Simple Email Service).

---

