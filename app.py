import streamlit as st
from ollama import chat

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="TouchGrass Buddy",
    page_icon="🌿",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "mission" not in st.session_state:
    st.session_state.mission = None

for key in ["c1", "c2", "c3", "c4", "c5"]:
    if key not in st.session_state:
        st.session_state[key] = False

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🌿 TouchGrass Buddy")

st.subheader(
    "AI-Powered Outdoor Adventure Generator"
)

st.info(
    "Runs entirely offline using Ollama and Llama 3.2. "
    "No internet connection required. No user data leaves your device."
)

st.write(
    """
Most AI applications try to keep people on screens.
TouchGrass Buddy does the opposite by generating personalized outdoor adventures
that encourage exploration, exercise, mindfulness, and real-world experiences.
"""
)

# --------------------------------------------------
# USER INPUTS
# --------------------------------------------------

time_available = st.selectbox(
    "⏱️ How much time do you have?",
    [
        "15 Minutes",
        "30 Minutes",
        "60 Minutes"
    ]
)

location_type = st.selectbox(
    "📍 Where are you going?",
    [
        "Park",
        "Neighborhood",
        "Garden",
        "Beach",
        "Anywhere"
    ]
)

adventure_type = st.selectbox(
    "🎯 What kind of adventure do you want?",
    [
        "Nature Exploration",
        "Photography",
        "Fitness",
        "Family Fun",
        "Mindfulness"
    ]
)

# --------------------------------------------------
# GENERATE MISSION
# --------------------------------------------------

if st.button("🚀 Generate Outdoor Mission"):

    prompt = f"""
You are an outdoor adventure designer.

Create a fun outdoor mission.

Time Available: {time_available}
Location: {location_type}
Adventure Type: {adventure_type}

Rules:

- Create a creative mission title.
- Create exactly 5 outdoor challenges.
- Keep challenges short.
- Use emojis.
- Encourage outdoor exploration.
- Keep total response under 100 words.

Format:

# Mission Title

1. Challenge
2. Challenge
3. Challenge
4. Challenge
5. Challenge
"""

    with st.spinner("Generating your outdoor adventure..."):

        response = chat(
            model="llama3.2:latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        st.session_state.mission = response.message.content

        # Reset checkboxes
        for key in ["c1", "c2", "c3", "c4", "c5"]:
            st.session_state[key] = False

# --------------------------------------------------
# DISPLAY MISSION
# --------------------------------------------------

if st.session_state.mission:

    st.markdown("---")

    st.subheader("🌿 Your Adventure Mission")

    st.markdown(st.session_state.mission)

    st.markdown("---")

    # --------------------------------------------------
    # PROGRESS TRACKER
    # --------------------------------------------------

    st.subheader("✅ Mission Progress Tracker")

    st.checkbox(
        "Challenge 1 Completed",
        key="c1"
    )

    st.checkbox(
        "Challenge 2 Completed",
        key="c2"
    )

    st.checkbox(
        "Challenge 3 Completed",
        key="c3"
    )

    st.checkbox(
        "Challenge 4 Completed",
        key="c4"
    )

    st.checkbox(
        "Challenge 5 Completed",
        key="c5"
    )

    completed = sum([
        st.session_state.c1,
        st.session_state.c2,
        st.session_state.c3,
        st.session_state.c4,
        st.session_state.c5
    ])

    progress = completed / 5

    st.progress(progress)

    st.write(
        f"Progress: {int(progress * 100)}%"
    )

    if progress == 1:

        st.success(
            "🎉 Mission Completed! Great job getting outdoors and touching grass!"
        )

    st.markdown("---")

    # --------------------------------------------------
    # START NEW ADVENTURE
    # --------------------------------------------------

    if st.button("🔄 Start New Adventure"):

        keys_to_remove = [
            "mission",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5"
        ]

        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()