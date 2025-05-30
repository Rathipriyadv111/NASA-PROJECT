import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from config import DATABASE_NAME

# Set page config without overriding the custom theme from config.toml
st.set_page_config(
    page_title="NASA Asteroid Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS aligned with config.toml theme
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #262730; /* Text color from config.toml */
        margin-bottom: 30px;
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .sidebar .sidebar-content {
        background-color: #F0F2F6; /* Secondary background from config.toml */
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .filter-section {
        background-color: #FFFFFF; /* Background from config.toml */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Subtle shadow for light theme */
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .metric-container {
        background-color: #FFFFFF; /* Background from config.toml */
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Subtle shadow */
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .nav-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        background-color: #F0F2F6; /* Secondary background from config.toml */
        cursor: pointer;
        color: #262730; /* Text color from config.toml */
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .nav-item.active {
        background-color: #ff4b4b80; /* Primary color from config.toml */
        color: #FFFFFF; /* White for contrast */
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .filter-button {
        background-color: #ff4b4b80; /* Primary color from config.toml */
        color: #FFFFFF; /* White for contrast */
        border: none;
        padding: 10px 30px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .stSelectbox > div > div {
        background-color: #FFFFFF; /* Background from config.toml */
        color: #262730; /* Text color from config.toml */
        font-family: sans-serif; /* Font from config.toml */
    }
    
    .stSlider > div > div > div {
        background-color: #ff4b4b80; /* Primary color from config.toml */
    }
</style>
""", unsafe_allow_html=True)

class NEODashboard:
    def __init__(self):
        self.db_name = DATABASE_NAME
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_name)
    
    def execute_query(self, query):
        """Execute SQL query and return DataFrame"""
        conn = self.get_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_predefined_queries(self):
        """Return dictionary of predefined queries"""
        return {
            "1. Count asteroid approaches": """
                SELECT a.name, COUNT(*) as approach_count
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                GROUP BY a.id, a.name
                ORDER BY approach_count DESC
                LIMIT 20
            """,
            
            "2. Average velocity per asteroid": """
                SELECT a.name, AVG(ca.relative_velocity_kmph) as avg_velocity
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                GROUP BY a.id, a.name
                ORDER BY avg_velocity DESC
                LIMIT 20
            """,
            
            "3. Top 10 fastest asteroids": """
                SELECT a.name, MAX(ca.relative_velocity_kmph) as max_velocity
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                GROUP BY a.id, a.name
                ORDER BY max_velocity DESC
                LIMIT 10
            """,
            
            "4. Hazardous asteroids (>3 approaches)": """
                SELECT a.name, COUNT(*) as approach_count
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                WHERE a.is_potentially_hazardous_asteroid = 1
                GROUP BY a.id, a.name
                HAVING COUNT(*) > 3
                ORDER BY approach_count DESC
            """,
            
            "5. Month with most approaches": """
                SELECT strftime('%Y-%m', ca.close_approach_date) as month,
                       COUNT(*) as approach_count
                FROM close_approach ca
                GROUP BY strftime('%Y-%m', ca.close_approach_date)
                ORDER BY approach_count DESC
                LIMIT 10
            """,
            
            "6. Fastest approach speed": """
                SELECT a.name, ca.relative_velocity_kmph, ca.close_approach_date
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                ORDER BY ca.relative_velocity_kmph DESC
                LIMIT 1
            """,
            
            "7. Largest asteroids by diameter": """
                SELECT name, estimated_diameter_max_km
                FROM asteroids
                ORDER BY estimated_diameter_max_km DESC
                LIMIT 20
            """,
            
            "8. Asteroid with most approaches": """
                SELECT a.name, COUNT(*) as approach_count
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                GROUP BY a.id, a.name
                ORDER BY approach_count DESC
                LIMIT 1
            """,
            
            "9. Closest approach per asteroid": """
                SELECT a.name, ca.close_approach_date, 
                       MIN(ca.miss_distance_km) as closest_distance
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                GROUP BY a.id, a.name
                ORDER BY closest_distance ASC
                LIMIT 20
            """,
            
            "10. High velocity asteroids (>50,000 km/h)": """
                SELECT DISTINCT a.name
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                WHERE ca.relative_velocity_kmph > 50000
                ORDER BY a.name
            """,
            
            "11. Approaches per month": """
                SELECT strftime('%Y-%m', ca.close_approach_date) as month,
                       COUNT(*) as approach_count
                FROM close_approach ca
                GROUP BY strftime('%Y-%m', ca.close_approach_date)
                ORDER BY month
            """,
            
            "12. Brightest asteroid (lowest magnitude)": """
                SELECT name, absolute_magnitude_h
                FROM asteroids
                ORDER BY absolute_magnitude_h ASC
                LIMIT 10
            """,
            
            "13. Hazardous vs Non-hazardous count": """
                SELECT 
                    CASE 
                        WHEN is_potentially_hazardous_asteroid = 1 THEN 'Hazardous'
                        ELSE 'Non-Hazardous'
                    END as hazard_status,
                    COUNT(DISTINCT id) as count
                FROM asteroids
                GROUP BY is_potentially_hazardous_asteroid
            """,
            
            "14. Closer than Moon (<1 LD)": """
                SELECT a.name, ca.close_approach_date, ca.miss_distance_lunar
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                WHERE ca.miss_distance_lunar < 1
                ORDER BY ca.miss_distance_lunar ASC
            """,
            
            "15. Within 0.05 AU": """
                SELECT a.name, ca.close_approach_date, ca.astronomical
                FROM asteroids a
                JOIN close_approach ca ON a.id = ca.neo_reference_id
                WHERE ca.astronomical < 0.05
                ORDER BY ca.astronomical ASC
            """
        }
    
    def create_sidebar_navigation(self):
        """Create custom sidebar navigation"""
        st.sidebar.markdown("### 🌌 Asteroid Approaches")
        
        # Navigation items with custom styling
        if 'selected_page' not in st.session_state:
            st.session_state.selected_page = "Filter Criteria"
        
        # Filter Criteria button
        if st.sidebar.button("🔍 Filter Criteria", key="filter_btn", 
                           type="primary" if st.session_state.selected_page == "Filter Criteria" else "secondary"):
            st.session_state.selected_page = "Filter Criteria"
        
        # Queries button  
        if st.sidebar.button("📊 Queries", key="queries_btn",
                           type="primary" if st.session_state.selected_page == "Queries" else "secondary"):
            st.session_state.selected_page = "Queries"
        
        return st.session_state.selected_page
    
    def create_filters(self):
        """Create filter section matching the image layout"""
        st.sidebar.markdown("---")
        
        # Date filters in two columns
        st.sidebar.markdown("**📅 Date Range**")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date(2024, 1, 1), key="start_date")
        with col2:
            end_date = st.date_input("End Date", value=date(2025, 4, 13), key="end_date")
        
        st.sidebar.markdown("---")
        
        # Magnitude Range
        st.sidebar.markdown("**🌟 Min Magnitude**")
        magnitude_range = st.sidebar.slider("", 13.8, 32.61, (13.8, 32.61), key="magnitude")
        
        # Velocity Range
        st.sidebar.markdown("**⚡ Relative_velocity_kmph Range**")
        velocity_range = st.sidebar.slider("", 1418.21, 173071.83, (1418.21, 173071.83), key="velocity")
        
        # Min Diameter
        st.sidebar.markdown("**📏 Min Estimated Diameter (km)**")
        diameter_min_range = st.sidebar.slider("", 0.0, 4.62, (0.0, 4.62), key="diameter_min")
        
        # Max Diameter  
        st.sidebar.markdown("**📏 Max Estimated Diameter (km)**")
        diameter_max_range = st.sidebar.slider("", 0.0, 10.33, (0.0, 10.33), key="diameter_max")
        
        # Astronomical Unit
        st.sidebar.markdown("**🌍 Astronomical unit**")
        au_range = st.sidebar.slider("", 0.0, 0.50, (0.0, 0.50), key="au")
        
        # Hazardous filter
        st.sidebar.markdown("**⚠️ Only Show Potentially Hazardous**")
        hazard_filter = st.sidebar.selectbox("", [0, 1, "All"], key="hazard")
        
        # Filter button
        st.sidebar.markdown("---")
        filter_clicked = st.sidebar.button("Filter", type="primary", use_container_width=True)
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'magnitude_range': magnitude_range,
            'velocity_range': velocity_range,
            'diameter_min_range': diameter_min_range,
            'diameter_max_range': diameter_max_range,
            'au_range': au_range,
            'hazard_filter': hazard_filter
        }, filter_clicked
    
    def build_filter_query(self, filters):
        """Build SQL query based on filters"""
        base_query = """
            SELECT DISTINCT a.id, a.name, a.absolute_magnitude_h,
                   a.estimated_diameter_min_km, a.estimated_diameter_max_km,
                   a.is_potentially_hazardous_asteroid, ca.close_approach_date,
                   ca.relative_velocity_kmph, ca.astronomical, ca.miss_distance_km
            FROM asteroids a
            JOIN close_approach ca ON a.id = ca.neo_reference_id
            WHERE 1=1
        """
        
        conditions = []
        
        # Date filter
        conditions.append(f"ca.close_approach_date BETWEEN '{filters['start_date']}' AND '{filters['end_date']}'")
        
        # Magnitude filter
        conditions.append(f"a.absolute_magnitude_h BETWEEN {filters['magnitude_range'][0]} AND {filters['magnitude_range'][1]}")
        
        # Velocity filter
        conditions.append(f"ca.relative_velocity_kmph BETWEEN {filters['velocity_range'][0]} AND {filters['velocity_range'][1]}")
        
        # Diameter filters
        conditions.append(f"a.estimated_diameter_min_km BETWEEN {filters['diameter_min_range'][0]} AND {filters['diameter_min_range'][1]}")
        conditions.append(f"a.estimated_diameter_max_km BETWEEN {filters['diameter_max_range'][0]} AND {filters['diameter_max_range'][1]}")
        
        # AU filter
        conditions.append(f"ca.astronomical BETWEEN {filters['au_range'][0]} AND {filters['au_range'][1]}")
        
        # Hazardous filter
        if filters['hazard_filter'] != "All":
            conditions.append(f"a.is_potentially_hazardous_asteroid = {filters['hazard_filter']}")
        
        # Combine all conditions
        where_clause = " AND ".join(conditions)
        final_query = f"{base_query} AND {where_clause} ORDER BY ca.close_approach_date DESC LIMIT 10000"
        
        return final_query
    
    def run_dashboard(self):
        """Main dashboard function"""        
        # Header with emoji and styling
        st.markdown('<div class="main-header">🚀 NASA Asteroid Tracker 🌌</div>', unsafe_allow_html=True)
        
        # Sidebar navigation
        page = self.create_sidebar_navigation()
        
        if page == "Filter Criteria":
            # Create filters
            filters, filter_clicked = self.create_filters()
            
            # Main content area
            if filter_clicked or 'filtered_data' not in st.session_state:
                # Execute filtered query
                query = self.build_filter_query(filters)
                df = self.execute_query(query)
                st.session_state.filtered_data = df
            else:
                df = st.session_state.filtered_data if 'filtered_data' in st.session_state else pd.DataFrame()
            
            # Display results
            if not df.empty:
                st.subheader("🛸 Filtered Asteroids")
                
                # Summary metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Records", len(df))
                with col2:
                    hazardous_count = len(df[df['is_potentially_hazardous_asteroid'] == 1])
                    st.metric("Hazardous", hazardous_count)
                with col3:
                    avg_velocity = df['relative_velocity_kmph'].mean()
                    st.metric("Avg Velocity", f"{avg_velocity:.2f} km/h")
                with col4:
                    min_distance = df['miss_distance_km'].min()
                    st.metric("Closest Approach", f"{min_distance:.2f} km")
                
                # Data table with better formatting
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "close_approach_date": st.column_config.DateColumn("Close Approach Date"),
                        "relative_velocity_kmph": st.column_config.NumberColumn("Velocity (km/h)", format="%.2f"),
                        "astronomical": st.column_config.NumberColumn("AU", format="%.4f"),
                        "miss_distance_km": st.column_config.NumberColumn("Miss Distance (km)", format="%.2f"),
                        "estimated_diameter_min_km": st.column_config.NumberColumn("Min Diameter (km)", format="%.4f"),
                        "estimated_diameter_max_km": st.column_config.NumberColumn("Max Diameter (km)", format="%.4f"),
                        "absolute_magnitude_h": st.column_config.NumberColumn("Magnitude", format="%.2f"),
                        "is_potentially_hazardous_asteroid": st.column_config.CheckboxColumn("Hazardous")
                    }
                )
            else:
                st.info("👆 Click the Filter button to load asteroid data")
        
        elif page == "Queries":
            st.subheader("📊 Predefined Analysis Queries")
            
            queries = self.get_predefined_queries()
            selected_query = st.selectbox("Select Analysis", list(queries.keys()))
            
            if st.button("Execute Query", type="primary"):
                df = self.execute_query(queries[selected_query])
                
                st.subheader(f"Results: {selected_query}")
                st.dataframe(df, use_container_width=True)
                
                # Create visualizations based on query type
                if "velocity" in selected_query.lower() and len(df.columns) >= 2:
                    fig = px.bar(df.head(10), x=df.columns[0], y=df.columns[1], 
                               title=f"Velocity Analysis: {selected_query}")
                    st.plotly_chart(fig, use_container_width=True)
                
                elif "month" in selected_query.lower() and len(df.columns) >= 2:
                    fig = px.line(df, x=df.columns[0], y=df.columns[1],
                                title=f"Monthly Trend: {selected_query}")
                    st.plotly_chart(fig, use_container_width=True)
                
                elif "count" in selected_query.lower() and len(df.columns) >= 2:
                    fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                               title=f"Distribution: {selected_query}")
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    dashboard = NEODashboard()
    dashboard.run_dashboard()