# URL Safety API

This project is a **URL Safety API** hosted on **Railway**, using **MongoDB** as its database and built with **FastAPI**. The API leverages a **BERT-based model** for URL safety prediction, providing reliable insights into the potential safety of any URL.

---

## Overview

This API analyzes URLs to determine their safety, making use of advanced NLP techniques with a BERT-based architecture to predict the likelihood of a URL being malicious or safe. This service is ideal for applications needing URL filtering, content moderation, or enhanced security for web interactions.

---

## Features

- **BERT-based URL Prediction**: Uses a pre-trained BERT model fine-tuned for URL safety analysis, providing high accuracy and contextual awareness in predictions.
- **FastAPI Framework**: Built with FastAPI for high-performance and quick response times.
- **MongoDB Integration**: Stores URL records and analysis results, ensuring scalable and persistent data management.
- **Deployed on Railway**: Easily accessible and ready for production, hosted on Railway for reliability and scalability.

---

## Benefits of Using the URL Safety API

- **Accurate Predictions**: The BERT model provides state-of-the-art accuracy by analyzing the structure and patterns in URLs, going beyond simple blacklists.
- **Scalable and Secure**: With Railway hosting and MongoDB, the API is built to handle large volumes of requests while ensuring data integrity and security.
- **Fast and Reliable**: FastAPI and Railway's infrastructure ensure low latency, making this API responsive for real-time applications.
- **Easy Integration**: Simple JSON-based responses make it easy to integrate with various applications and systems.

---

## Getting Started

To use this API, access the hosted endpoint on Railway. For details on endpoint usage and integration, refer to the documentation (if available).

---

## Technologies Used

- **FastAPI** - For building the RESTful API
- **MongoDB** - For data storage
- **BERT Model** - For URL safety analysis
- **Railway** - For hosting and deployment

---

## License

This project is licensed under the MIT License.

##Curious about the training of BERT architecture? please find safeNET repository under this github
