import pickle
import streamlit as st
import requests
from streamlit.components.v1 import html

# Page Configuration (must be first)
st.set_page_config(
    page_title="Movie Magic Recommender",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium look
st.markdown("""
<style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.8) !important;
        border-right: 1px solid #444;
    }
    
    /* Header Styling */
    .header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff8a00, #e52e71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-family: 'Montserrat', sans-serif;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .subheader {
        text-align: center;
        color: rgba(255,255,255,0.7);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Select Box Styling */
    .stSelectbox > div > div {
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid #5e5e5e !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #ff8a00, #e52e71);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        display: block;
        margin: 0 auto;
        width: fit-content;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Movie Cards */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .movie-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .movie-card img {
        border-radius: 10px;
        aspect-ratio: 2/3;
        object-fit: cover;
        margin-bottom: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        transition: transform 0.3s ease;
    }
    
    .movie-card img:hover {
        transform: scale(1.03);
    }
    
    .movie-title {
        color: white;
        font-weight: 600;
        font-size: 1rem;
        margin-top: auto;
        text-align: center;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        margin: 2rem 0 1.5rem;
        text-align: center;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add custom font
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800&family=Open+Sans&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Main App
st.markdown("<h1 class='header'>Movie Magic Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Discover your next favorite film based on movies you love</p>", unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.markdown("## 🎬 About")
    st.markdown("""
    This recommender system suggests movies similar to your selection using advanced algorithms.
    """)
    st.markdown("## 🔍 How It Works")
    st.markdown("""
    1. Select a movie you enjoy
    2. Click "Find Recommendations"
    3. Discover new favorites!
    """)
    st.markdown("## 📊 Data Source")
    st.markdown("""
    Movie data powered by TMDB API
    """)

# Load Data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Movie Selection
col1, col2, col3 = st.columns([1,2,1])
with col2:
    selected_movie = st.selectbox(
        "Select a movie you love:",
        movies['title'].values,
        help="Choose a movie to get personalized recommendations"
    )

# Recommendation Button
if st.button('✨ Find Recommendations'):
    with st.spinner('Searching for cinematic treasures...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        st.markdown("<h2 class='section-header'>Recommended For You</h2>", unsafe_allow_html=True)
        
        # Create columns with custom styling
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.markdown(f"""
                <div class='movie-card'>
                    <img src="{recommended_movie_posters[i]}" style="width:100%">
                    <p class='movie-title'>{recommended_movie_names[i]}</p>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p class="footer">© 2023 Movie Magic Recommender | Powered by Streamlit</p>', unsafe_allow_html=True)