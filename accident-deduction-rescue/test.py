"""
Sign Bridge - Balanced UI Implementation
A sign language learning platform with regional variations
Developer: Pavithra G

Design Philosophy: Balanced between minimal and dashboard-heavy
Clear component purpose, easy navigation, feature-rich but calm
"""

import streamlit as st

# ==================== STYLING SECTION ====================

def apply_custom_theme():
    """
    Apply custom dark theme with balanced layout styling.
    """
    st.markdown("""
        <style>
        /* ===== GLOBAL STYLES ===== */
        .stApp {
            background-color: #0D0D0D;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ===== HEADER STYLES (LEFT ALIGNED) ===== */
        .main-title {
            color: #4A9EFF;
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 8px;
            padding-top: 20px;
        }
        
        .subtitle {
            color: #A0A0A0;
            font-size: 16px;
            font-style: italic;
            margin-bottom: 30px;
        }
        
        .header-divider {
            border-top: 1px solid #2A2A2A;
            margin: 20px 0 30px 0;
        }
        
        /* ===== CONTROL PANEL STYLES ===== */
        .control-panel {
            background-color: #1A1A1A;
            padding: 25px;
            border-radius: 8px;
            border: 1px solid #2A2A2A;
        }
        
        .panel-section {
            margin-bottom: 25px;
        }
        
        .section-label {
            color: #EAEAEA;
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 8px;
            display: block;
        }
        
        /* ===== REPRESENTATION CARD STYLES ===== */
        .representation-card {
            background-color: #1A1A1A;
            padding: 30px;
            border-radius: 8px;
            border: 1px solid #2A2A2A;
            min-height: 450px;
        }
        
        .card-title {
            color: #EAEAEA;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .card-subtitle {
            color: #A0A0A0;
            font-size: 14px;
            margin-bottom: 25px;
        }
        
        /* Placeholder state */
        .placeholder-state {
            color: #A0A0A0;
            font-size: 16px;
            text-align: center;
            padding: 100px 20px;
            line-height: 1.8;
        }
        
        /* Active state - sign display */
        .sign-display {
            margin-top: 20px;
        }
        
        .sign-word {
            color: #4A9EFF;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 12px;
        }
        
        .sign-region-tag {
            display: inline-block;
            background-color: #2A2A2A;
            color: #A0A0A0;
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 13px;
            margin-bottom: 25px;
        }
        
        .sign-description {
            color: #EAEAEA;
            font-size: 15px;
            line-height: 1.8;
            margin-bottom: 20px;
            padding: 20px;
            background-color: #151515;
            border-radius: 6px;
            border-left: 3px solid #4A9EFF;
        }
        
        .detail-row {
            margin-bottom: 18px;
        }
        
        .detail-label {
            color: #4A9EFF;
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 6px;
        }
        
        .detail-value {
            color: #EAEAEA;
            font-size: 14px;
            line-height: 1.6;
        }
        
        /* Expandable section */
        .expandable-section {
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #2A2A2A;
        }
        
        /* ===== STREAMLIT COMPONENT OVERRIDES ===== */
        .stSelectbox label, .stTextInput label {
            color: #EAEAEA !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }
        
        .stSelectbox > div > div, .stTextInput > div > div > input {
            background-color: #2A2A2A !important;
            color: #EAEAEA !important;
            border: 1px solid #3A3A3A !important;
        }
        
        .stButton > button {
            background-color: #4A9EFF !important;
            color: #FFFFFF !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            padding: 10px 30px !important;
            border: none !important;
            border-radius: 6px !important;
            width: 100% !important;
            margin-top: 10px !important;
        }
        
        .stButton > button:hover {
            background-color: #3A8EEF !important;
        }
        
        .stButton > button:disabled {
            background-color: #2A2A2A !important;
            color: #5A5A5A !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #1A1A1A !important;
            color: #EAEAEA !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderContent {
            background-color: #151515 !important;
            border: 1px solid #2A2A2A !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ==================== DATA MANAGEMENT ====================

def load_sign_data():
    """Load sign language data with regional variations."""
    data = {
        "hello": {
            "standard": {
                "handshape": "Open hand, fingers together",
                "movement": "Wave side to side near head",
                "orientation": "Palm facing forward",
                "context": "Common greeting used in most informal and formal situations across all regions.",
                "description": "The standard 'hello' sign is performed by raising your dominant hand to head level with fingers together and palm facing forward. Wave your hand side to side in a friendly motion. This is universally recognized and appropriate for all contexts."
            },
            "northern": {
                "handshape": "Open hand, fingers spread",
                "movement": "Single wave motion",
                "orientation": "Palm facing outward",
                "context": "Northern regional variation with more emphasis on finger spread.",
                "description": "In northern regions, the 'hello' sign uses a more spread finger position with a single, deliberate wave motion. This variation emphasizes openness and is commonly used in casual greetings."
            },
            "southern": {
                "handshape": "Open hand, slight curve",
                "movement": "Multiple small waves",
                "orientation": "Palm angled forward",
                "context": "Southern variation with softer, more animated movement.",
                "description": "The southern 'hello' incorporates multiple small, gentle waves with a slight curve to the hand. This creates a warmer, more animated greeting style typical of southern sign language communities."
            }
        },
        "thank you": {
            "standard": {
                "handshape": "Flat hand, fingers together",
                "movement": "Move from chin forward and down",
                "orientation": "Palm facing upward at end",
                "context": "Express gratitude in various situations, from casual to formal.",
                "description": "The standard 'thank you' begins with your flat hand touching your chin, fingers together. Move your hand forward and downward, ending with palm facing up. This sign conveys sincere appreciation."
            },
            "northern": {
                "handshape": "Flat hand, relaxed fingers",
                "movement": "Direct forward motion from chin",
                "orientation": "Palm facing upward throughout",
                "context": "Northern variation with more direct, efficient movement.",
                "description": "Northern communities use a more direct motion, moving the hand straight forward from the chin with palm facing up throughout the entire sign. This reflects a more straightforward communication style."
            }
        },
        "goodbye": {
            "standard": {
                "handshape": "Open hand, fingers together",
                "movement": "Wave side to side",
                "orientation": "Palm facing forward",
                "context": "Casual farewell, similar to spoken goodbye wave.",
                "description": "The standard 'goodbye' sign mirrors the common wave gesture. Hold your hand at shoulder level with palm forward and wave side to side. This is universally understood across all regions."
            }
        },
        "please": {
            "standard": {
                "handshape": "Flat hand on chest",
                "movement": "Circular motion on chest",
                "orientation": "Palm facing chest",
                "context": "Polite request, used in both formal and informal settings.",
                "description": "To sign 'please', place your flat hand on your chest with palm facing inward. Make a circular motion over your heart area. This sign literally references the heart, conveying sincerity in your request."
            }
        },
        "sorry": {
            "standard": {
                "handshape": "Closed fist with 'A' handshape",
                "movement": "Circular motion on chest",
                "orientation": "Knuckles facing outward",
                "context": "Express apology or regret in various situations.",
                "description": "Form an 'A' handshape (closed fist with thumb beside fingers) and place it on your chest. Make a circular motion to express regret or apology. The movement over the heart emphasizes sincerity."
            }
        },
        "yes": {
            "standard": {
                "handshape": "Closed fist",
                "movement": "Nod motion up and down",
                "orientation": "Thumb on top",
                "context": "Affirmative response, agreement.",
                "description": "Make a fist with your thumb resting on top of your fingers. Move your fist up and down in a nodding motion, similar to nodding your head 'yes'. Simple and clear affirmative sign."
            }
        },
        "no": {
            "standard": {
                "handshape": "Extended index and middle fingers with thumb",
                "movement": "Tap fingers to thumb repeatedly",
                "orientation": "Palm facing forward",
                "context": "Negative response, disagreement.",
                "description": "Extend your index and middle fingers along with your thumb, keeping other fingers closed. Tap your two fingers against your thumb in a quick motion, like a mouth closing. Clear negative indicator."
            }
        },
        "help": {
            "standard": {
                "handshape": "Flat hand under closed fist",
                "movement": "Lift both hands upward together",
                "orientation": "Bottom palm facing up, top fist facing forward",
                "context": "Request assistance or offer help to others.",
                "description": "Place your dominant hand in a fist on top of your non-dominant flat hand (palm up). Lift both hands together upward. This represents lifting someone up or being lifted, symbolizing assistance."
            }
        }
    }
    return data

def get_available_words():
    """Get sorted list of available words."""
    data = load_sign_data()
    return sorted(list(data.keys()))

def get_available_regions(word):
    """Get available regions for a specific word."""
    data = load_sign_data()
    if word in data:
        return list(data[word].keys())
    return ["standard"]

def get_sign_info(word, region):
    """Get sign information for word and region."""
    data = load_sign_data()
    if word in data and region in data[word]:
        return data[word][region]
    return None

def get_other_regions(word, current_region):
    """Get information about other regional variations."""
    data = load_sign_data()
    if word not in data:
        return []
    
    other_regions = []
    for region, info in data[word].items():
        if region != current_region:
            other_regions.append({
                "region": region,
                "context": info.get("context", ""),
                "handshape": info.get("handshape", "")
            })
    return other_regions

# ==================== UI COMPONENTS ====================

def render_header():
    """Render left-aligned header with divider."""
    st.markdown("""
        <div class="main-title">🤟 Sign Bridge</div>
        <div class="subtitle">Connecting communities through sign language</div>
        <div class="header-divider"></div>
    """, unsafe_allow_html=True)

def render_control_panel():
    """Render simplified left control panel."""
    st.markdown('<div class="section-label">Select a word</div>', unsafe_allow_html=True)
    
    # Word selection
    words = get_available_words()
    selected_word = st.selectbox(
        "Choose word",
        options=[""] + words,
        key="word_select",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Region selection (only if word selected)
    selected_region = "standard"
    if selected_word:
        st.markdown('<div class="section-label">Region / Variation</div>', unsafe_allow_html=True)
        regions = get_available_regions(selected_word)
        
        # Format region names nicely
        region_display = {r: r.title() for r in regions}
        
        selected_region = st.selectbox(
            "Choose region",
            options=regions,
            format_func=lambda x: region_display[x],
            key="region_select",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Show sign button
    button_disabled = not selected_word
    show_button = st.button(
        "Show Sign",
        disabled=button_disabled,
        use_container_width=True
    )
    
    return selected_word, selected_region, show_button

def render_representation_card(word, region, show_data):
    """Render main representation card."""
    st.markdown("""
        <div class="card-title">Sign Representation</div>
        <div class="card-subtitle">Contextual and regional representation</div>
    """, unsafe_allow_html=True)
    
    if not show_data or not word:
        # Placeholder state
        st.markdown("""
            <div class="representation-card">
                <div class="placeholder-state">
                    Select a word and region to view its sign representation
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Active state
        sign_info = get_sign_info(word, region)
        
        if sign_info:
            st.markdown(f"""
                <div class="representation-card">
                    <div class="sign-word">{word.title()}</div>
                    <div class="sign-region-tag">Region: {region.title()}</div>
                    
                    <div class="sign-description">
                        {sign_info['description']}
                    </div>
                    
                    <div class="detail-row">
                        <div class="detail-label">Handshape</div>
                        <div class="detail-value">{sign_info['handshape']}</div>
                    </div>
                    
                    <div class="detail-row">
                        <div class="detail-label">Movement</div>
                        <div class="detail-value">{sign_info['movement']}</div>
                    </div>
                    
                    <div class="detail-row">
                        <div class="detail-label">Orientation</div>
                        <div class="detail-value">{sign_info['orientation']}</div>
                    </div>
                    
                    <div class="detail-row">
                        <div class="detail-label">Context</div>
                        <div class="detail-value">{sign_info['context']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Expandable "Other Regions" section
            other_regions = get_other_regions(word, region)
            if other_regions:
                with st.expander("🌍 Other Regions", expanded=False):
                    st.markdown('<div class="expandable-section">', unsafe_allow_html=True)
                    for other in other_regions:
                        st.markdown(f"""
                            <div style="margin-bottom: 20px; padding: 15px; background-color: #1A1A1A; border-radius: 6px;">
                                <div style="color: #4A9EFF; font-weight: 600; margin-bottom: 8px;">
                                    {other['region'].title()}
                                </div>
                                <div style="color: #EAEAEA; font-size: 14px; margin-bottom: 6px;">
                                    <strong>Handshape:</strong> {other['handshape']}
                                </div>
                                <div style="color: #A0A0A0; font-size: 13px;">
                                    {other['context']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Future video placeholder
            st.info("📹 Native video contributions will be added in future updates")
        else:
            st.markdown("""
                <div class="representation-card">
                    <div class="placeholder-state">
                        Sign information not available for this combination
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Sign Bridge",
        page_icon="🤟",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply theme
    apply_custom_theme()
    
    # Render header
    render_header()
    
    # Two-column layout: compact control panel + main content
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        selected_word, selected_region, show_button = render_control_panel()
    
    with col2:
        render_representation_card(selected_word, selected_region, show_button)

if __name__ == "__main__":
    main()