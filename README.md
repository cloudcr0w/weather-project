# WEATHER-PROJECT :cloud:

WELCOME to the WEATHER-PROJECT - my second project showing my skills in AWS
:construction: **UNDER CONSTRUCTION** :construction:
https://main.d24ky3ld7v2sml.amplifyapp.com

## WHAT IS THIS PROJECT?

This repository showcases a **serverless application** that periodically fetches weather data from a public API, stores it in the cloud, processes the information, and (in future iterations) visualizes the results.
This project uses the **OpenWeather API (free plan)**, which allows fetching weather data **once per day** due to rate limits. If you want to run this project with your own API key, you will need to register on [OpenWeather](https://openweathermap.org/api).

## Architecture
```bash
## Architecture

```
+------------------------+         +-------------------+
|  GitHub (repo + CI/CD)|  --->   |  AWS Amplify      |
|  + GitHub Actions     |         |  (frontend deploy)|
+------------------------+         +-------------------+

                                        |
                                        v
                               +------------------+
                               |  Static Website  |
                               |  (download.html) |
                               +------------------+
                                        |
                                        v
                               [FETCH LATEST JSON]
                                        |
                                        v
+--------------+     invokes     +----------------------+     reads      +------------------------------+
|   User       |  ----------->   |   API Gateway        |  ----------->  | Lambda: GetLatestWeatherFile |
| (browser)    |                 |  /latest-weather     |                |  (list & get from S3)         |
+--------------+                 +----------------------+                +------------------------------+
                                                                                |
                                                                                v
                                                                 +--------------------------------------+
                                                                 |  S3 bucket: weather-project-raw-data |
                                                                 |  raw/wroclaw,pl/*.json               |
                                                                 +--------------------------------------+
```
```

### Wrocław Weather App

This is a simple serverless  weather application showcasing the current weather data for Wrocław, Poland. The weather data is fetched from the OpenWeather API and is updated once a day. Structure is : html, css, js, python files. The app includes additional features such as:

- **Gallery** : A small collection of images showcasing iconic places in Wrocław, including attractions like the Main Square, Ostrów Tumski, and the Centennial Hall.
What to Explore: Short descriptions of key attractions and their significance.
- **Events** : Information about major upcoming events in Wrocław, such as the Christmas Market, Good Beer Festival, and New Horizons Film Festival.
- **Multilingual Support** : The app supports both Polish and English languages, with a simple toggle switch to change the language.
The application provides a clean, responsive design, making it user-friendly on both desktop and mobile devices.

- **Continuous Deployment with AWS Amplify**
This project is hosted and continuously deployed using AWS Amplify. Changes pushed to the main branch are automatically built and deployed.

## KEY AWS SERVICES

- **AWS Lambda** – Cyclical data fetching and processing
- **Amazon EventBridge** – Triggers Lambda on a schedule (once daily)
- **Amazon S3** – Stores raw CSV/JSON data
- **DynamoDB / RDS** – Holds processed data
- **AWS Amplify (Gen2)** – Hosts a frontend for data visualization
- **AWS Cloudwatch** - Holds logs from app (in future logs will be stored in S3) :construction:
- **AWS CloudTrail** -  for real-time monitoring and auditing of API activity :construction:
- **AWS CloudFormation** - for automating infrastructure and improving deployment consistency 
- **GitHub** – Version control & project history

## PROJECT STATUS

📌 See project roadmap: [PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md)


## ✅ Continuous Integration & Deployment (CI/CD)

This project uses **GitHub Actions** to automate deployment and testing:

- ✅ **Automated Testing** – Every push runs unit tests using `pytest`
- ✅ **Automatic AWS Deployment** – If tests pass, the Lambda function is updated
- ✅ **No Manual Uploading** – Code is packed and pushed automatically

Check out the [`.github/workflows/deploy-getweather.yml`](.github/workflows/deploy-getweather.yml) file for details.

## HOW TO RUN LOCALLY

To run this project on your local machine:

1️⃣ **Clone the repository**  

```sh
git clone https://github.com/your-username/weather-project.git
cd weather-project
```

2️⃣ Set up environment variables
This project uses environment variables stored in a .env file.

Recommended method: Copy the .env.example file and rename it to .env
```sh
cp .env.example .env
```
Open .env and replace placeholder values with your own API keys and AWS settings.
Alternatively, you can manually create a .env file in the project root and add:
```sh
OPENWEATHER_API_KEY=your_api_key_here
BUCKET_NAME=your_bucket_name_here
TABLE_NAME=your_table_name_here
```
Or export them as environment variables:
```sh
export OPENWEATHER_API_KEY=your_api_key_here
export BUCKET_NAME=your_bucket_name_here
export TABLE_NAME=your_table_name_here
```

3️⃣ Install dependencies
Backend (Python):
```sh
pip install -r requirements.txt
```

Frontend (Node.js):
```sh
cd frontend
npm install
npm start
```

4️⃣ Run backend locally
Get Weather Data
```sh
python lambda/get_weather/main.py
```
Analyze Weather Data
```sh
python lambda/analyze_weather/analyze_data.py
```

5️⃣ Deploy to AWS

This project **uses GitHub Actions for deployment**, so **you don't need to manually upload ZIP files**.

If you want to deploy manually, use:
```sh
zip -r get_weather_lambda.zip lambda/get_weather/*
aws lambda update-function-code --function-name GetWeatherFunction --zip-file fileb://get_weather_lambda.zip
```

## CONTRIBUTION & FEEDBACK

Feedback is always welcome! Feel free to open an **issue** or submit a **pull request** with any suggestions or improvements.

:construction: **STAY TUNED FOR UPDATES!** :construction:

## 🔗 Connect with me!
- 🌍 **Portfolio**: [crow-project.click](https://crow-project.click)
- 🏗 **GitHub**: [github.com/cloudcr0w](https://github.com/cloudcr0w)
- 💼 **LinkedIn**: [linkedin.com/in/adam-wrona-111ba728b](https://www.linkedin.com/in/adam-wrona-111ba728b)