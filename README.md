# SmokePal

**AI-powered nicotine intake estimation to help users understand and reduce their consumption.**

SmokePal provides quantitative feedback on nicotine intake. By measuring nicotine inhaled per puff, users can track progress, identify patterns, and work toward cessation with data driven insights.

---

## Quick Start

### Manual Calculator (No Hardware)

```
https://web-production-4710f.up.railway.app/
```

Enter:
- Air Inhaled (L)
- Nicotine Concentration (mg/ml)

Get: Estimated nicotine (mg)

---

## Installation

### Prerequisites
- Python 3.8+
- ESP32 and Sensors (optional, for hardware)

### Setup

```bash
cd NicotineCalculator
pip install -r requirements.txt
python web/app.py
```

Access: `http://localhost:5000`

---

## API Endpoints

### `/api/add` (POST)

**Request:**
```json
{
  "nicotine_concentration_mg_per_ml": 6-50,
  "user_id": 1,
  "vape_id": 1,
  "date": "2026-09-27",
  "air_inhaled": 0.98-5.67,
  "temperature_celsius": 20-50
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "History added"
}
```

---

## Usage Examples

### cURL
```bash
curl -X POST http://localhost:5000/api/add \
  -H "Content-Type: application/json" \
  -d '{
    "nicotine_concentration_mg_per_ml": 14,
    "user_id": 1,
    "vape_id": 1,
    "date": "2026-09-27",
    "air_inhaled": 2.45,
    "temperature_celsius": 32.1
  }'
```

### Python
```python
import requests

data = {
    "nicotine_concentration_mg_per_ml": 14,
    "user_id": 1,
    "vape_id": 1,
    "date": "2026-09-27",
    "air_inhaled": 2.45,
    "temperature_celsius": 32.1
}

response = requests.post("http://localhost:5000/api/add", json=data)
result = response.json()
print(result)
```

### JavaScript
```javascript
const data = {
  "nicotine_concentration_mg_per_ml": 14,
  "user_id": 1,
  "vape_id": 1,
  "date": "2026-09-27",
  "air_inhaled": 2.45,
  "temperature_celsius": 32.1
};

fetch("http://localhost:5000/api/add", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(result => console.log(result));
```

---

## Model Info

**Algorithm:** XGBoost Regressor

**Metrics:**
- R² Score
- MAE
- RMSE
- n_estimators
- max_depth
- learning_rate

---

---

## Testing

**Manual:**
```
Example
Air Inhaled: 4.5 L
Nicotine Concentration: 20 mg/ml
→ Result: 90 mg
```

**API:**
```bash
curl -X POST http://localhost:5000/api/add \
  -H "Content-Type: application/json" \
  -d '{
    "nicotine_concentration_mg_per_ml": 20,
    "user_id": 1,
    "vape_id": 1,
    "date": "2026-09-27",
    "air_inhaled": 4.5,
    "temperature_celsius": 35.0
  }'
```

Expected: `{"status": "success", "message": "History added"}`

---

## Disclaimer

⚠️ **Prototype - Not a Medical Device**

SmokePal is an experimental system. Nicotine estimates are AI-generated based on sensor data and should NOT be used for:
- Medical diagnosis
- Health decisions
- Clinical applications
- Regulatory compliance

Further validation required before medical/clinical use.

---

## Tech Stack

**ML:** XGBoost, scikit-learn, NumPy, Pandas  
**Backend:** Flask, joblib  
**Frontend:** HTML5, CSS  

---

**Status:** Prototype | **Updated:** September 2026