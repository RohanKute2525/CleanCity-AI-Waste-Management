# 🌱 CleanCity AI

### AI-Powered Smart Waste Management & City Cleanliness Monitoring System

CleanCity AI is an AI-powered smart city waste management system designed to detect waste, monitor smart bins, identify waste hotspots, analyze citizen complaints, calculate city cleanliness scores, and support optimized waste collection.

The system combines **Artificial Intelligence, Machine Learning, Computer Vision, Data Analytics, and Interactive Maps** to provide a centralized platform for smart waste management.

---

## 🚀 Features

### 🤖 1. AI Waste Detection

Upload a waste image and use YOLO-based computer vision to detect different types of waste.

Supported categories:

- 🧴 Plastic
- 📄 Paper
- 🔩 Metal
- 🍾 Glass
- 🌱 Organic Waste
- 🗑️ Mixed Waste

The system provides:

- Waste type
- Detection confidence
- Number of detected objects
- Scan cleanliness score

---

### 🗑️ 2. Smart Bin Monitoring

Monitor smart waste bins using fill-level data.

Bin status:

| Fill Level | Status |
|---|---|
| Below 60% | 🟢 Normal |
| 60% – 79% | 🟡 Warning |
| 80%+ | 🔴 Critical |

The dashboard displays:

- Total bins
- Normal bins
- Warning bins
- Critical bins
- Average bin fill percentage

---

### 📍 3. AI Waste Hotspot Detection

Machine Learning is used to identify areas with a higher probability of waste accumulation.

The system considers factors such as:

- Recent complaints
- Waste detections
- Average bin fill
- Rainfall
- Uncollected bins
- Population density

An interactive **Leaflet map** displays hotspot locations.

---

### 🌱 4. AI City Cleanliness Score

CleanCity AI calculates an overall cleanliness score from **0–100**.

The score combines:

- 🗑️ Bin health
- 🚨 Complaint health
- 📍 Hotspot health
- ♻️ Waste health

Cleanliness rating:

| Score | Rating |
|---|---|
| 90–100 | Excellent |
| 75–89 | Good |
| 60–74 | Moderate |
| 40–59 | Poor |
| 0–39 | Critical |

---

### 🚨 5. Citizen Complaint Management

Citizens can submit waste-related complaints.

Complaint information includes:

- Location
- Complaint type
- Priority
- Description
- Status
- Date

The system maintains pending and resolved complaint statistics.

---

### 🚛 6. Smart Collection Routes

Collection route data can be displayed to support efficient waste collection.

The system can be extended to prioritize:

```text
Critical Bins
       ↓
High-Risk Hotspots
       ↓
Nearby Collection Points
       ↓
Optimized Route
