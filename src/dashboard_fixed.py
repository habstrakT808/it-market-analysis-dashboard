# dashboard_fixed.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="IT Market Analysis Dashboard",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - FIXED LAYOUT & TYPOGRAPHY
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-width: 200px;
    }
    .metric-card h3 {
        color: #ffffff !important;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-card h2 {
        color: #ffffff !important;
        font-size: 1.8rem;
        margin: 0.3rem 0;
        font-weight: bold;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.2;
    }
    .metric-card p {
        color: #e8f4fd !important;
        font-size: 0.8rem;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .insight-box h3 {
        color: #ffffff !important;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .insight-box p {
        color: #ffffff !important;
        font-size: 1rem;
        line-height: 1.6;
    }
    .insight-box ul, .insight-box ol {
        color: #ffffff !important;
    }
    .insight-box li {
        color: #ffffff !important;
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    .insight-box strong {
        color: #ffeb3b !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load cleaned data with caching"""
    try:
        jobs_df = pd.read_csv('data/processed/it_jobs_cleaned.csv')
        tech_df = pd.read_csv('data/processed/tech_trends_cleaned.csv')
        
        # Load quality report if exists
        try:
            with open('data/processed/data_quality_report.json', 'r') as f:
                quality_report = json.load(f)
        except:
            quality_report = {}
        
        return jobs_df, tech_df, quality_report
    except FileNotFoundError:
        st.error("❌ Data files not found! Please run data collection and cleaning first.")
        st.stop()

def create_salary_analysis(df):
    """Create salary analysis visualizations - FIXED VERSION"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary distribution by experience level
        fig_salary_exp = px.box(
            df, 
            x='experience_level', 
            y='salary_avg',
            title='💰 Salary Distribution by Experience Level',
            color='experience_level',
            color_discrete_sequence=['#ff7f0e', '#2ca02c', '#d62728']
        )
        fig_salary_exp.update_layout(
            showlegend=False,
            yaxis_title="Average Salary (IDR)",
            xaxis_title="Experience Level"
        )
        st.plotly_chart(fig_salary_exp, use_container_width=True)
    
    with col2:
        # Salary by location
        location_salary = df.groupby('location')['salary_avg'].mean().sort_values(ascending=False).head(10)
        
        fig_salary_loc = px.bar(
            x=location_salary.values,
            y=location_salary.index,
            orientation='h',
            title='📍 Average Salary by Location (Top 10)',
            color=location_salary.values,
            color_continuous_scale='Blues'
        )
        fig_salary_loc.update_layout(
            xaxis_title="Average Salary (IDR)",
            yaxis_title="Location",
            showlegend=False
        )
        st.plotly_chart(fig_salary_loc, use_container_width=True)
    
    # Additional salary insights
    st.markdown("### 📈 Salary Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        median_salary = df['salary_avg'].median()
        st.metric("Median Salary", f"Rp {median_salary:,.0f}")
    
    with col2:
        highest_paying = df.groupby('title')['salary_avg'].mean().idxmax()
        highest_salary = df.groupby('title')['salary_avg'].mean().max()
        st.metric("Highest Paying Role", f"{highest_paying}", f"Rp {highest_salary:,.0f}")
    
    with col3:
        salary_growth = ((df[df['experience_level'] == 'Senior']['salary_avg'].mean() / 
                         df[df['experience_level'] == 'Junior']['salary_avg'].mean() - 1) * 100)
        st.metric("Junior to Senior Growth", f"{salary_growth:.1f}%")

def create_skills_analysis(df):
    """Create skills demand analysis - FIXED VERSION"""
    
    # Extract all skills
    all_skills = []
    for skills_str in df['required_skills'].dropna():
        skills = [skill.strip() for skill in str(skills_str).split(',')]
        all_skills.extend(skills)
    
    skill_counts = pd.Series(all_skills).value_counts().head(15)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top skills bar chart
        fig_skills = px.bar(
            x=skill_counts.values,
            y=skill_counts.index,
            orientation='h',
            title='🔧 Most In-Demand Skills',
            color=skill_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_skills.update_layout(
            xaxis_title="Number of Job Posts",
            yaxis_title="Skills",
            showlegend=False,
            height=500
        )
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        # Skills by salary
        skill_salary = {}
        for skill in skill_counts.head(10).index:
            mask = df['required_skills'].str.contains(skill, case=False, na=False)
            if mask.any():
                skill_salary[skill] = df[mask]['salary_avg'].mean()
        
        if skill_salary:
            skill_salary_df = pd.DataFrame(list(skill_salary.items()), 
                                         columns=['Skill', 'Avg_Salary'])
            skill_salary_df = skill_salary_df.sort_values('Avg_Salary', ascending=False)
            
            fig_skill_salary = px.bar(
                skill_salary_df,
                x='Avg_Salary',
                y='Skill',
                orientation='h',
                title='💰 Average Salary by Skill',
                color='Avg_Salary',
                color_continuous_scale='Oranges'
            )
            fig_skill_salary.update_layout(
                showlegend=False,
                height=500,
                xaxis_title="Average Salary (IDR)",
                yaxis_title="Skills"
            )
            st.plotly_chart(fig_skill_salary, use_container_width=True)
    
    # Skills trend analysis
    st.markdown("### 🚀 Technology Trends")
    
    # Create skills categories
    frontend_skills = ['JavaScript', 'React', 'Vue.js', 'Angular', 'HTML', 'CSS']
    backend_skills = ['Python', 'Java', 'PHP', 'Node.js', 'Laravel', 'Django']
    data_skills = ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Python', 'Tableau']
    devops_skills = ['Docker', 'Kubernetes', 'AWS', 'Azure', 'Linux', 'Git']
    
    categories = {
        'Frontend': sum([skill_counts.get(skill, 0) for skill in frontend_skills]),
        'Backend': sum([skill_counts.get(skill, 0) for skill in backend_skills]),
        'Data & Analytics': sum([skill_counts.get(skill, 0) for skill in data_skills]),
        'DevOps & Cloud': sum([skill_counts.get(skill, 0) for skill in devops_skills])
    }
    
    fig_categories = px.pie(
        values=list(categories.values()),
        names=list(categories.keys()),
        title='📊 Skills Distribution by Category',
        color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    )
    st.plotly_chart(fig_categories, use_container_width=True)

def create_market_overview(df):
    """Create market overview metrics and charts - FIXED LAYOUT"""
    
    # Key metrics with consistent layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Total Jobs</h3>
            <h2>{:,}</h2>
            <p>Active Postings</p>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        avg_salary = df['salary_avg'].mean()
        # Format salary to prevent wrapping
        if avg_salary >= 1000000:
            salary_formatted = f"{avg_salary/1000000:.1f}M"
        else:
            salary_formatted = f"{avg_salary/1000:.0f}K"
        
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Avg Salary</h3>
            <h2>Rp {}</h2>
            <p>Monthly Average</p>
        </div>
        """.format(salary_formatted), unsafe_allow_html=True)
    
    with col3:
        unique_companies = df['company'].nunique()
        st.markdown("""
        <div class="metric-card">
            <h3>🏢 Companies</h3>
            <h2>{}</h2>
            <p>Hiring Now</p>
        </div>
        """.format(unique_companies), unsafe_allow_html=True)
    
    with col4:
        remote_pct = (df['remote_option'].isin(['Remote', 'Hybrid']).sum() / len(df)) * 100
        st.markdown("""
        <div class="metric-card">
            <h3>🌐 Remote Jobs</h3>
            <h2>{:.1f}%</h2>
            <p>Remote/Hybrid</p>
        </div>
        """.format(remote_pct), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Job distribution by experience level
        exp_counts = df['experience_level'].value_counts()
        fig_exp = px.pie(
            values=exp_counts.values,
            names=exp_counts.index,
            title='👨‍💻 Job Distribution by Experience Level',
            color_discrete_sequence=['#ff7f0e', '#2ca02c', '#d62728']
        )
        fig_exp.update_layout(
            font=dict(size=12),
            title_font_size=16,
            height=400
        )
        st.plotly_chart(fig_exp, use_container_width=True)
    
    with col2:
        # Top job titles
        title_counts = df['title'].value_counts().head(8)
        fig_titles = px.bar(
            x=title_counts.values,
            y=title_counts.index,
            orientation='h',
            title='💼 Most Popular Job Titles',
            color=title_counts.values,
            color_continuous_scale='Blues'
        )
        fig_titles.update_layout(
            showlegend=False,
            xaxis_title="Number of Jobs",
            yaxis_title="Job Title",
            font=dict(size=12),
            title_font_size=16,
            height=400
        )
        st.plotly_chart(fig_titles, use_container_width=True)

def create_geographic_analysis(df):
    """Create geographic analysis - FIXED VERSION"""
    
    # Location distribution
    location_counts = df['location'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_locations = px.bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation='h',
            title='📍 Job Distribution by Location',
            color=location_counts.values,
            color_continuous_scale='Greens'
        )
        fig_locations.update_layout(
            xaxis_title="Number of Jobs",
            yaxis_title="Location",
            showlegend=False
        )
        st.plotly_chart(fig_locations, use_container_width=True)
    
    with col2:
        # Remote vs On-site
        remote_counts = df['remote_option'].value_counts()
        fig_remote = px.pie(
            values=remote_counts.values,
            names=remote_counts.index,
            title='🌐 Remote Work Options',
            color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c']
        )
        st.plotly_chart(fig_remote, use_container_width=True)
    
    # Regional analysis
    st.markdown("### 🗺️ Regional Market Analysis")
    
    # Group locations by region
    jakarta_region = df[df['location'].isin(['Jakarta', 'Bandung', 'Hybrid'])]
    java_region = df[df['location'].isin(['Surabaya', 'Yogya', 'Solo', 'Semarang', 'Malang'])]
    other_region = df[~df['location'].isin(['Jakarta', 'Bandung', 'Hybrid', 'Surabaya', 'Yogya', 'Solo', 'Semarang', 'Malang', 'Remote'])]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Jakarta Region", f"{len(jakarta_region)} jobs", f"Avg: Rp {jakarta_region['salary_avg'].mean():,.0f}")
    
    with col2:
        st.metric("Java Region", f"{len(java_region)} jobs", f"Avg: Rp {java_region['salary_avg'].mean():,.0f}")
    
    with col3:
        st.metric("Other Regions", f"{len(other_region)} jobs", f"Avg: Rp {other_region['salary_avg'].mean():,.0f}")
    
    # Lampung opportunity analysis
    st.markdown("### 🎯 Lampung Market Opportunity")
    
    lampung_jobs = df[df['location'].str.contains('Lampung', case=False, na=False)]
    
    if len(lampung_jobs) > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Jobs in Lampung", len(lampung_jobs))
        with col2:
            st.metric("Avg Salary", f"Rp {lampung_jobs['salary_avg'].mean():,.0f}")
        with col3:
            st.metric("Market Share", f"{(len(lampung_jobs)/len(df)*100):.1f}%")
    else:
        st.info("💡 **Market Opportunity**: No major IT job postings detected in Lampung. This represents a significant opportunity for Newus Technology to establish market leadership in the region!")

def create_business_insights(df):
    """Create business insights for Newus Technology - FINAL VERSION"""
    
    st.markdown("## 🎯 Strategic Insights for Newus Technology")
    
    # Market opportunities
    remote_pct = (df['remote_option'].isin(['Remote', 'Hybrid']).sum() / len(df)) * 100
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>🚀 Market Opportunities</h3>
        <ul>
            <li><strong>Lampung Market Gap:</strong> Minimal IT job postings indicate an underserved market with high potential</li>
            <li><strong>Remote Work Adoption:</strong> {remote_pct:.1f}% of jobs offer remote/hybrid - opportunity for distributed teams</li>
            <li><strong>Growing Demand:</strong> {len(df)} active job postings show robust IT market activity</li>
            <li><strong>Salary Competitiveness:</strong> Average salary of Rp {df['salary_avg'].mean():,.0f} indicates healthy market</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Technology recommendations - ALL CONTENT IN HEADER BOX
    top_skills = []
    for skills_str in df['required_skills'].dropna():
        skills = [skill.strip() for skill in str(skills_str).split(',')]
        top_skills.extend(skills)
    
    skill_counts = pd.Series(top_skills).value_counts().head(10)
    
    # Build technology list HTML
    tech_list_html = "<p>Based on market demand analysis, Newus Technology should prioritize:</p><div style='display: flex; gap: 2rem;'><div style='flex: 1;'><ul>"
    
    skills_list = list(skill_counts.items())
    mid_point = len(skills_list) // 2
    
    # First column
    for i, (skill, count) in enumerate(skills_list[:mid_point]):
        percentage = (count / len(df)) * 100
        tech_list_html += f"<li><strong>{skill}:</strong> {count} mentions ({percentage:.1f}% of jobs)</li>"
    
    tech_list_html += "</ul></div><div style='flex: 1;'><ul>"
    
    # Second column
    for i, (skill, count) in enumerate(skills_list[mid_point:]):
        percentage = (count / len(df)) * 100
        tech_list_html += f"<li><strong>{skill}:</strong> {count} mentions ({percentage:.1f}% of jobs)</li>"
    
    tech_list_html += "</ul></div></div>"
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>💡 Technology Investment Recommendations</h3>
        {tech_list_html}
    </div>
    """, unsafe_allow_html=True)
    
    # Talent Acquisition Strategy - ALL CONTENT IN HEADER BOX
    avg_salaries = df.groupby('experience_level')['salary_avg'].mean()
    
    # Build salary list HTML
    salary_list_html = "<p>Competitive salary benchmarks for different experience levels:</p><ul>"
    
    for level, salary in avg_salaries.items():
        salary_list_html += f"<li><strong>{level} Level:</strong> Rp {salary:,.0f}/month</li>"
    
    salary_list_html += "</ul>"
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>💰 Talent Acquisition Strategy</h3>
        {salary_list_html}
    </div>
    """, unsafe_allow_html=True)
    
    # Recommended Action Items - SINGLE COLUMN (as requested)
    action_items_html = """
    <ol>
        <li><strong>Expand to Lampung:</strong> Establish strong presence in underserved regional market</li>
        <li><strong>Build Remote Capabilities:</strong> Develop infrastructure for remote/hybrid work models</li>
        <li><strong>Skill Development:</strong> Train team in high-demand technologies (JavaScript, Python, React)</li>
        <li><strong>Competitive Pricing:</strong> Position services based on regional salary benchmarks</li>
        <li><strong>Partnership Strategy:</strong> Target companies hiring actively in IT space</li>
        <li><strong>Market Research:</strong> Continuously monitor technology trends and demands</li>
    </ol>
    """
    
    st.markdown(f"""
    <div class="insight-box">
        <h3>📋 Recommended Action Items</h3>
        {action_items_html}
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard function - FIXED VERSION"""
    
    # Header
    st.markdown('<h1 class="main-header">💻 IT Market Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Strategic Intelligence for Newus Technology - "New Experience With Us"</p>', unsafe_allow_html=True)
    
    # Load data
    jobs_df, tech_df, quality_report = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Dashboard Filters")
    
    # Experience level filter
    exp_levels = ['All'] + list(jobs_df['experience_level'].unique())
    selected_exp = st.sidebar.selectbox("Experience Level", exp_levels)
    
    # Location filter
    locations = ['All'] + list(jobs_df['location'].unique())
    selected_location = st.sidebar.selectbox("Location", locations)
    
    # Salary range filter
    min_salary, max_salary = st.sidebar.slider(
        "Salary Range (IDR)",
        min_value=int(jobs_df['salary_avg'].min()),
        max_value=int(jobs_df['salary_avg'].max()),
        value=(int(jobs_df['salary_avg'].min()), int(jobs_df['salary_avg'].max())),
        format="Rp %d"
    )
    
    # Apply filters
    filtered_df = jobs_df.copy()
    
    if selected_exp != 'All':
        filtered_df = filtered_df[filtered_df['experience_level'] == selected_exp]
    
    if selected_location != 'All':
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    
    filtered_df = filtered_df[
        (filtered_df['salary_avg'] >= min_salary) & 
        (filtered_df['salary_avg'] <= max_salary)
    ]
    
    # Show filtered data info
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**📊 Showing {len(filtered_df)} of {len(jobs_df)} jobs**")
    
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches your current filters. Please adjust the filter criteria.")
        return
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Market Overview", "💰 Salary Analysis", "🔧 Skills Demand", "📍 Geographic Analysis", "🎯 Business Insights"])
    
    with tab1:
        create_market_overview(filtered_df)
    
    with tab2:
        create_salary_analysis(filtered_df)
    
    with tab3:
        create_skills_analysis(filtered_df)
    
    with tab4:
        create_geographic_analysis(filtered_df)
    
    with tab5:
        create_business_insights(filtered_df)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>📊 IT Market Analysis Dashboard | Created for Newus Technology Interview</p>
        <p>📅 Data Analysis Period: {datetime.now().strftime("%B %Y")} | 🔄 Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        <p>💡 <strong>"New Experience With Us"</strong> - Empowering Strategic Decisions with Data</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()