
-----

# Indian City Weather Forecast with Prophet

-----

## Live Demo

Experience the live application here: [https://indiancityweatherpredictionwithprophet.streamlit.app](https://indiancityweatherpredictionwithprophet.streamlit.app)

## GitHub Repository

Access the full codebase here: [https://github.com/Pranav7378/Weather-Predicter](https://github.com/Pranav7378/Weather-Predicter)

-----

## Description

This is a **full-stack time series forecasting project** designed to predict daily average temperatures for major Indian cities using **Facebook Prophet**. The model is trained on 10 years of historical weather data and its predictions are rigorously compared against real-time vendor forecasts from Visual Crossing. Live evaluation is performed using **MAE** and **RMSE** metrics to assess accuracy.

-----

## Cities Covered

  * Mumbai
  * Delhi
  * Chennai
  * Bangalore
  * Hyderabad

-----

## Key Features

  * **Built and deployed entirely for ₹0** using free tools.
  * **Interactive Streamlit UI** for easy city selection and forecast range customization.
  * **Live model vs. vendor comparison** with real-time error metrics (MAE, RMSE).
  * Integrated **GitHub, Google Colab, and Git LFS** workflow for efficient development and version control.

-----

## Technologies Used

### Data

  * **Meteostat**: For historical weather data.
  * **Visual Crossing**: For benchmark real-time vendor forecasts.

### Model

  * **Facebook Prophet**: The core time series forecasting library.

### Frontend

  * **Streamlit**: For creating the interactive user interface.

### Backend

  * **Python**

### Deployment

  * **Streamlit Community Cloud**

### Version Control

  * **GitHub**: For source code management.
  * **Git LFS**: For handling large `.pkl` model files.

### Notebook Training

  * **Google Colab**

### Tools & Libraries

  * `Prophet`
  * `pandas`
  * `plotly`
  * `streamlit`
  * `requests`
  * `meteostat`
  * `sklearn`

-----

## Challenges Overcome

  * **API Limits**: Successfully switched from OpenWeatherMap to Meteostat and Visual Crossing to avoid API rate limits.
  * **Large Files**: Effectively managed and stored large `.pkl` model files using **Git LFS**.
  * **Cost-Efficiency & Reproducibility**: Designed the application to run offline on cached models, ensuring it remains cost-free and reproducible.

-----

## Impact

  * Achieved **portfolio-ready results** with **RMSE \< 0.5 °C** for key cities like Mumbai and Chennai.
  * Demonstrated strong capabilities in handling **data pipelines, model training, API integration, deployment, and live analytics**.

-----

## Author

**Kodamasimham Chaitanya Pranav Sai**

  * **Email**: pranav.kodamasimham@gmail.com
  * **LinkedIn**: [https://www.linkedin.com/in/kodamasimham-pranav-sai/](https://www.linkedin.com/in/kodamasimham-pranav-sai/)

-----