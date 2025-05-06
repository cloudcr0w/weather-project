# 📈 Weather Project – Progress & TODO

## ✅ Completed
- [x] Weather data collection via AWS Lambda (OpenWeather API)
- [x] Scheduled with Amazon EventBridge (daily run)
- [x] Raw JSON files saved in Amazon S3 (weather-project-raw-data)
- [x] Basic frontend hosted on AWS Amplify
- [x] GitHub Actions CI/CD (auto-build & deploy)
- [x] Frontend button to download weather data as CSV
- [x] CORS config for public S3 read access
- [x] Lambda function to fetch latest file from S3
- [x] API Gateway endpoint `/latest-weather` for frontend integration
- [x] Text-based architecture diagram (README)

## 🔄 In Progress
- [ ] Connect frontend to API Gateway (dynamic fetch of latest file)
- [ ] Clean up Lambda output (optional: presigned URLs)
- [ ] Refactor static HTML into modular frontend

## 🔜 Planned
- [ ] Weather chart (last 7 days – temperature trend)
- [ ] Server-side CSV generation in Lambda or CI
- [ ] Frontend date picker or time range selector
- [ ] Secure download via signed URL (IAM/Cognito)
- [ ] Store daily summaries in DynamoDB (or RDS)
- [ ] Implement Terraform/CDK IaC
- [ ] Admin-only dashboard (protected route or login)
- [ ] Add testing for new Lambda/API components

---

_Last updated: 2025-05-06_
