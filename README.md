# 🚀 NASA Near-Earth Object (NEO) Tracker

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-green.svg)
![NASA API](https://img.shields.io/badge/NASA-API-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A comprehensive asteroid tracking system that monitors Near-Earth Objects using NASA's API**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation)

</div>

---

## 🌟 Features

### 🔥 **Core Capabilities**
- **Real-time Data Collection**: Automatically fetches 10,000+ asteroid records from NASA's NEO API
- **Intelligent Database Storage**: SQLite-powered storage with optimized schema design
- **Interactive Dashboard**: Beautiful Streamlit web interface with real-time filtering
- **Advanced Analytics**: 15+ predefined queries for comprehensive asteroid analysis
- **Smart Filtering**: Multi-dimensional filtering by date, velocity, size, and hazard level

### 📊 **Analytics & Visualizations**
- Velocity distribution analysis
- Monthly approach patterns  
- Hazardous asteroid identification
- Size correlation studies
- Interactive charts and graphs

### 🎯 **Key Metrics Tracked**
- Asteroid approach velocities (km/h)
- Miss distances (km, AU, Lunar Distance)
- Estimated diameters and magnitudes
- Potentially hazardous asteroid classification
- Close approach dates and orbital bodies

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/nasa-neo-tracker.git
cd nasa-neo-tracker

# Set up virtual environment
python -m venv neo_env
source neo_env/bin/activate  # On Windows: neo_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure NASA API key
# Edit config.py and add your API key

# Set up database and collect data
python database_setup.py

# Launch the dashboard
streamlit run streamlit_app.py
```

**🎉 That's it! Your asteroid tracker is now live at `http://localhost:8501`**

## 📋 Prerequisites

- **Python 3.8+**
- **NASA API Key** (free from [api.nasa.gov](https://api.nasa.gov))
- **5GB free disk space** (for database storage)
- **Stable internet connection** (for API data collection)

## 🛠 Installation

### 1. **Get NASA API Key**
```bash
# Visit https://api.nasa.gov
# Register with your name and email
# Save your API key (format: qSxX9kz1L7....)
```

### 2. **Project Setup**
```bash
mkdir nasa_neo_tracker
cd nasa_neo_tracker

# Clone or download project files
git clone <repository-url> .

# Create virtual environment
python -m venv neo_env
```

### 3. **Activate Environment**
```bash
# Windows
neo_env\Scripts\activate

# macOS/Linux
source neo_env/bin/activate
```

### 4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 5. **Configure API**
Edit `config.py`:
```python
NASA_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
```

## 📁 Project Structure

```
nasa_neo_tracker/
├── 📄 README.md                 # This file
├── ⚙️ config.py                 # Configuration settings
├── 🔍 data_extraction.py        # NASA API data collector
├── 🗄️ database_setup.py         # Database initialization
├── 📊 streamlit_app.py          # Interactive dashboard
├── 📋 requirements.txt          # Python dependencies
└── 💾 asteroid_data.db          # SQLite database (auto-created)
```

## 💻 Usage

### **Initialize Database**
```bash
python database_setup.py
```
*Collects 10,000+ asteroid records and sets up SQLite database*

### **Launch Dashboard**
```bash
streamlit run streamlit_app.py
```
*Opens interactive web interface at http://localhost:8501*

### **Dashboard Features**

#### 🔍 **Filter Criteria Tab**
- **Date Range**: Filter approaches by date
- **Velocity Range**: Filter by approach speed (km/h)
- **Diameter Range**: Filter by asteroid size
- **Distance Range**: Filter by miss distance (AU)
- **Hazard Level**: Filter potentially hazardous asteroids

#### 📊 **Queries Tab**
Ready-to-use analytical queries:
1. Count asteroid approaches
2. Average velocity per asteroid  
3. Top 10 fastest asteroids
4. Hazardous asteroids analysis
5. Monthly approach patterns
6. Closest approach records
7. Largest asteroids by diameter
8. High-velocity asteroid identification
9. Lunar distance analysis
10. Brightness correlation studies
...and 5 more advanced queries!

## 🔧 Configuration

### **config.py Settings**
```python
NASA_API_KEY = "your_api_key_here"
BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"
TARGET_RECORDS = 10000
DATABASE_NAME = "asteroid_data.db"
START_DATE = "2024-01-01"
BATCH_DAYS = 7
```

### **API Rate Limiting**
- NASA API: 1,000 requests/hour
- Built-in rate limiting (1 second delays)
- Automatic retry logic for failed requests

## 📊 Database Schema

### **Asteroids Table**
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Unique asteroid identifier |
| `name` | TEXT | Asteroid designation |
| `absolute_magnitude_h` | REAL | Brightness measurement |
| `estimated_diameter_min_km` | REAL | Minimum diameter (km) |
| `estimated_diameter_max_km` | REAL | Maximum diameter (km) |
| `is_potentially_hazardous_asteroid` | BOOLEAN | Hazard classification |

### **Close Approach Table**
| Column | Type | Description |
|--------|------|-------------|
| `neo_reference_id` | INTEGER | Links to asteroids table |
| `close_approach_date` | DATE | Date of closest approach |
| `relative_velocity_kmph` | REAL | Approach velocity (km/h) |
| `astronomical` | REAL | Distance in Astronomical Units |
| `miss_distance_km` | REAL | Miss distance (kilometers) |
| `miss_distance_lunar` | REAL | Distance in Lunar Distance units |
| `orbiting_body` | TEXT | Reference body (usually "Earth") |

## 🎯 Example Queries

### **Find Fastest Asteroids**
```sql
SELECT a.name, MAX(ca.relative_velocity_kmph) as max_velocity
FROM asteroids a
JOIN close_approach ca ON a.id = ca.neo_reference_id
GROUP BY a.id, a.name
ORDER BY max_velocity DESC
LIMIT 10;
```

### **Monthly Approach Patterns**
```sql
SELECT strftime('%Y-%m', ca.close_approach_date) as month,
       COUNT(*) as approach_count
FROM close_approach ca
GROUP BY strftime('%Y-%m', ca.close_approach_date)
ORDER BY approach_count DESC;
```

## 🚨 Troubleshooting

### **Common Issues**

**API Key Error**
```bash
Error: Invalid API key
Solution: Check config.py and ensure your NASA API key is correct
```

**Database Connection Error**
```bash
Error: Database locked
Solution: Close any other applications using the database file
```

**Streamlit Port Busy**
```bash
Error: Port 8501 is already in use
Solution: Use: streamlit run streamlit_app.py --server.port 8502
```

### **Performance Tips**
- Close unused database connections
- Limit query results for large datasets
- Use date filters to improve performance
- Monitor API rate limits during data collection

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### **Areas for Contribution**
- Additional visualization types
- New analytical queries
- Performance optimizations
- UI/UX improvements
- Documentation enhancements

## 📈 Roadmap

- [ ] **Real-time Data Updates**: Live API integration
- [ ] **Machine Learning**: Trajectory prediction models
- [ ] **Mobile App**: React Native companion app
- [ ] **API Endpoints**: RESTful API for data access
- [ ] **Advanced Visualizations**: 3D orbital plots
- [ ] **Email Alerts**: Notifications for close approaches
- [ ] **Multi-database Support**: PostgreSQL/MySQL options

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA**: For providing the incredible NEO API
- **Streamlit**: For the amazing dashboard framework
- **Python Community**: For the excellent libraries used
- **Contributors**: Everyone who helps improve this project

## 📞 Support

**Need Help?**
- 📧 **Email**: rathipriyadv@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/nasa-neo-tracker/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/nasa-neo-tracker/discussions)

---

<div align="center">

**⭐ If this project helped you, please consider giving it a star!**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
