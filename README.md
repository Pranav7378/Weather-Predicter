
```markdown
# 🇮🇳 Indian City Weather Forecast (Prophet + Streamlit)

Predict daily average temperatures for major Indian cities using **10 years of real weather data** and **Facebook’s Prophet** model.

Powered by:

- **Meteostat** – historical weather (40 + years)  
- **Prophet** – time‑series forecasting  
- **Visual Crossing** – vendor forecast benchmark  
- **Streamlit** – interactive web app

---

## 📊 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indiancityweatherpredictionwithprophet.streamlit.app)

> Forecast 3 – 365 days ahead for **Mumbai**, **Delhi**, **Bangalore**, **Hyderabad**, or **Chennai** and compare with a commercial API.

---

## 📈 Sample Results (15‑day horizon)

| City        | MAE (°C) | RMSE (°C) |
|-------------|---------:|----------:|
| **Mumbai**      | 0.55 | 0.66 |
| **Hyderabad**   | 1.45 | 1.53 |
| **Chennai**     | 0.39 | 0.46 |
| **Bangalore**   | 2.07 | 2.42 |
| **Delhi**       | –    | –    |

> ✅ MAE ≤ 1 °C = excellent, 1–2 °C = good, > 2 °C = room to improve.

---

## 🗂 Project Structure

```

Weather-Predicter/
├── app\_streamlit/         ← Streamlit front‑end
│   └── app.py
├── notebooks/             ← Colab training notebook
│   └── train.ipynb
├── models/                ← Pre‑trained Prophet models (\*.pkl, Git LFS)
├── src/                   ← Core modules
│   ├── data\_loader.py     ← Meteostat fetch
│   ├── model.py           ← Prophet trainer
│   └── forecast\_vendor.py ← Visual Crossing API
└── README.md

````

---

## 🧑‍💻 Run Locally

```bash
git clone https://github.com/Pranav7378/Weather-Predicter.git
cd Weather-Predicter
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app_streamlit/app.py
````

Add your Visual Crossing key in `.streamlit/secrets.toml`:

```toml
VC_KEY = "YOUR_API_KEY"
```

---

## 🧪 Train Your Own Model (Colab)

1. Open **`notebooks/train.ipynb`** in Google Colab
2. Set `city`, `lat`, `lon`
3. Run all cells → a `.pkl` model appears in `models/`
4. Commit/push via Git LFS – the Streamlit app loads it automatically

---

## 🌐 Deployed on Streamlit Cloud

[https://indiancityweatherpredictionwithprophet.streamlit.app](https://indiancityweatherpredictionwithprophet.streamlit.app)

---

## ✍️ Author

**Kodamasimham Chaitanya Pranav Sai**
📫 [chakry.sowji.abhi@gmail.com](mailto:chakry.sowji.abhi@gmail.com) • [LinkedIn](https://www.linkedin.com/in/kodamasimham-pranav-sai/)

---

⭐ If this repo helped you, please consider giving it a star!

```

---

Copy everything inside the code block above—including the markdown table and code fences—and paste it directly into **README.md**. Commit and push; GitHub will render it beautifully.
```
