# 🌿 Plants App 🌿

A Flask-based web app from ACS-1710 designed to manage plants, integrated with MongoDB for data persistence.

## 🌐 Live online

You can view the deployed application [here](https://plants2.vis.mesmereyes.org/).

## 🛠️ Local Setup

### You will need pre-installed

- Docker
- Docker-Compose
- Git

### Steps to Run Locally in development mode

1. **Clone the Repository**  
   Add these commands via your terminal:

   ```sh
   git clone https://github.com/mcdott/3220-plants-dockerized.git plants-app
   cd plants-app
   ```

2. **Build and Run the Docker Containers**

   ```sh
   docker-compose up
   ```

3. **Access via Browser**

   ```sh
   http://0.0.0.0:5001/
   ```

4. **Shutdown the Docker Containers**  
   Press Ctrl + C and then run:
   ```sh
   docker-compose down
   ```

## ![Uptime Robot status](https://img.shields.io/uptimerobot/status/m795389342-d980ceac18c432b0a1287a1e)

## ![Static Badge](https://img.shields.io/badge/build-success-brightgreen)
