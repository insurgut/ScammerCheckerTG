
import streamlit as st

def apply_styles():
    """
    Apply custom CSS styling to the Streamlit app
    """
    bg_color = "#f5f7fa"
    text_color = "#333333"
    card_bg = "#ffffff"
    primary_color = "#4169e1"  # Royal Blue

    st.markdown(f"""
    <style>
        /* Main styles */
        .main {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Override Streamlit's default background */
        .stApp {{
            background-color: {bg_color};
        }}

        /* Fonts for all text */
        * {{
            font-family: 'Roboto', sans-serif !important;
        }}

        /* Base text size increase */
        .stMarkdown p {{
            font-size: 1.4rem !important;
            line-height: 1.8 !important;
            font-weight: 400;
            color: {text_color};
        }}

        /* Headers */
        h1 {{
            color: {primary_color};
            font-weight: 800;
            margin-bottom: 2rem;
            font-size: 3rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        h2 {{
            color: {primary_color};
            font-weight: 700;
            margin-top: 2.2rem;
            margin-bottom: 1.5rem;
            font-size: 2.4rem !important;
            letter-spacing: 0.03em;
        }}

        h3 {{
            color: {primary_color};
            font-weight: 600;
            margin-top: 1.8rem;
            margin-bottom: 1.2rem;
            font-size: 2rem !important;
            letter-spacing: 0.02em;
        }}

        /* Form styling */
        .stButton>button {{
            width: 100%;
            background-color: {primary_color};
            color: white;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 1rem 1.5rem;
            margin-top: 1rem;
            font-size: 1.3rem !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .stButton>button:hover {{
            opacity: 0.9;
            transform: scale(1.02);
            transition: all 0.2s ease;
        }}

        /* Info card */
        .info-card {{
            background-color: {card_bg};
            border-left: 6px solid {primary_color};
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 6px 10px rgba(0,0,0,0.1);
        }}

        /* Status indicators */
        .element-container div[data-testid="stAlert"] {{
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
            font-size: 1.3rem !important;
            font-weight: 500;
            background-color: {card_bg};
            color: {text_color};
        }}

        /* Input fields */
        .stTextInput>div>div>input {{
            border-radius: 8px;
            border: 2px solid #ddd;
            padding: 1rem !important;
            font-size: 1.3rem !important;
            background-color: {card_bg};
            color: {text_color};
        }}

        .stSelectbox label, .stTextInput label {{
            font-size: 1.3rem !important;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 0.5rem;
            color: {text_color};
        }}

        /* Spinners */
        .stSpinner>div {{
            border-top-color: {primary_color} !important;
            border-left-color: {primary_color} !important;
        }}

        /* Result container */
        .result-container {{
            padding: 2rem;
            border-radius: 12px;
            margin-top: 2rem;
            margin-bottom: 2rem;
            background-color: {card_bg};
            border: 2px solid #eee;
            font-size: 1.3rem !important;
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            color: {text_color};
        }}

        /* Footer */
        footer {{
            visibility: hidden;
        }}

        /* Override all Streamlit elements */
        .css-1d391kg, .css-12oz5g7 {{
            background-color: {bg_color};
        }}
        
        .stTextInput>div {{
            background-color: {card_bg};
        }}
        
        .stSelectbox>div>div {{
            background-color: {card_bg};
            color: {text_color};
        }}
        
        /* Sidebar background */
        section[data-testid="stSidebar"] {{
            background-color: {card_bg};
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Responsive design for mobile */
        @media (max-width: 768px) {{
            .stButton>button {{
                padding: 1.2rem 1.5rem;
            }}

            h1 {{
                font-size: 2.6rem !important;
            }}

            h2 {{
                font-size: 2.2rem !important;
            }}

            .stMarkdown p {{
                font-size: 1.3rem !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)
