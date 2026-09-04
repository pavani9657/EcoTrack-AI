import streamlit as st
import pandas as pd
from datetime import date

from calculations import calculate_impact
from database import create_database, save_activity, get_activities
from ml_model import predict_next_impact

st.set_page_config(
    page_title="EcoTrack AI",
    page_icon="🌱",
    layout="wide"
)

create_database()

# Load history
activities = get_activities()

columns = [
    "date",
    "distance",
    "vehicle",
    "electricity",
    "water",
    "meals",
    "meat_meals",
    "plastic_bottles",
    "total_impact"
]

if activities:
    df = pd.DataFrame(activities, columns=columns)
    df["date"] = pd.to_datetime(df["date"])
else:
    df = pd.DataFrame(columns=columns)


# Navigation
st.sidebar.title("🌱 EcoTrack AI")

page = st.sidebar.selectbox(
    "Choose page",
    ["Home", "History", "Ask EcoAI"]
)


# HOME
if page == "Home":

    st.title("🌱 EcoTrack AI")
    st.write("Track your environmental impact every day.")

    st.divider()

    st.header("📝 Record Today's Activity")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🚗 Transportation")

        distance = st.number_input(
            "Distance travelled (km)",
            min_value=0.0,
            value=0.0
        )

        vehicle = st.selectbox(
            "Transportation type",
            ["Car", "Bus", "Train", "Bike", "Walk"]
        )

        st.subheader("⚡ Electricity")

        electricity = st.number_input(
            "Electricity used (kWh)",
            min_value=0.0,
            value=0.0
        )

        st.subheader("🚿 Water")

        water = st.number_input(
            "Water used (litres)",
            min_value=0.0,
            value=0.0
        )

    with col2:

        st.subheader("🍽️ Food")

        meals = st.number_input(
            "Number of meals",
            min_value=0,
            value=0
        )

        meat_meals = st.number_input(
            "Non-vegetarian meals",
            min_value=0,
            value=0
        )

        st.subheader("🗑️ Waste")

        plastic_bottles = st.number_input(
            "Plastic bottles used",
            min_value=0,
            value=0
        )

    st.divider()

    if st.button("🌱 Calculate & Save", use_container_width=True):

        result = calculate_impact(
            distance,
            vehicle,
            electricity,
            water,
            meals,
            meat_meals,
            plastic_bottles
        )
        prediction = predict_next_impact()

        prediction = predict_next_impact()

        if prediction is not None:
            st.metric(
                "🤖 ML Predicted Impact",
                f"{prediction:.2f} kg CO₂e"
            )
        else:
            st.info(
                "🤖 ML prediction will be available after recording at least 3 activities."
            )

        save_activity(
            str(date.today()),
            distance,
            vehicle,
            electricity,
            water,
            meals,
            meat_meals,
            plastic_bottles,
            result["total"]
        )

        st.success("Activity saved successfully! 🌱")

        st.metric(
            "Total Impact",
            f"{result['total']:.2f} kg CO₂e"
        )

        st.subheader("Impact Breakdown")

        a, b, c, d, e = st.columns(5)

        a.metric("🚗 Transport", f"{result['transport']:.2f}")
        b.metric("⚡ Electricity", f"{result['electricity']:.2f}")
        c.metric("🍽️ Food", f"{result['food']:.2f}")
        d.metric("🚿 Water", f"{result['water']:.2f}")
        e.metric("🗑️ Waste", f"{result['waste']:.2f}")


# HISTORY
# HISTORY 
elif page == "History": 
    st.title("📊 EcoTrack Dashboard") 
    st.write("Monitor your environmental impact and track your progress.") 
 
    activities = get_activities() 
 
    if not activities: 
        st.info( 
            "No activities recorded yet. " 
            "Go to Home and add your first activity." 
        ) 
 
    else: 
        df_history = pd.DataFrame( 
            activities, 
            columns=columns 
        ) 
 
        # Convert date safely 
        df_history["date"] = pd.to_datetime( 
            df_history["date"], 
            errors="coerce" 
        ) 
 
        # Basic statistics 
        total_impact = df_history["total_impact"].sum() 
        average_impact = df_history["total_impact"].mean() 
        activity_count = len(df_history) 
        latest_impact = df_history.iloc[0]["total_impact"] 
 
        # ------------------------- 
        # KEY METRICS 
        # ------------------------- 
        st.subheader("🌍 Your Impact Overview") 
 
        col1, col2, col3, col4 = st.columns(4) 
 
        col1.metric( 
            "🌍 Total Impact", 
            f"{total_impact:.2f} kg CO₂e" 
        ) 
 
        col2.metric( 
            "📊 Average", 
            f"{average_impact:.2f} kg CO₂e" 
        ) 
 
        col3.metric( 
            "📝 Activities", 
            activity_count 
        ) 
 
        col4.metric( 
            "🌱 Latest Impact", 
            f"{latest_impact:.2f} kg CO₂e" 
        ) 
 
        st.divider() 
 
        # ------------------------- 
        # ML PREDICTION 
        # ------------------------- 
        st.subheader("🤖 AI Impact Prediction") 
 
        prediction = predict_next_impact() 
 
        if prediction is not None: 
            st.metric( 
                "Predicted Next Impact", 
                f"{prediction:.2f} kg CO₂e" 
            ) 
 
            if prediction < average_impact: 
                st.success( 
                    "🌱 Good trend! Your predicted impact is " 
                    "below your historical average." 
                ) 
            elif prediction > average_impact: 
                st.warning( 
                    "⚠️ Your predicted impact is above your " 
                    "historical average. Try reducing your " 
                    "highest-impact activities." 
                ) 
            else: 
                st.info( 
                    "📊 Your predicted impact is close to " 
                    "your historical average." 
                ) 
        else: 
            st.info( 
                "Record at least 3 activities to generate " 
                "an ML prediction." 
            ) 
 
        st.divider() 
 
        # ------------------------- 
        # GOAL 
        # ------------------------- 
        # st.subheader("🎯 Environmental Goal") 
 
        # goal = 100.0 
        # progress = min(total_impact / goal, 1.0) 
 
        # st.progress(progress) 
 
        # st.write( 
        #     f"**{total_impact:.2f} / {goal:.0f} kg CO₂e tracked**" 
        # ) 
 
        # if total_impact < goal: 
        #     remaining = goal - total_impact 
        #     st.success( 
        #         f"🌱 {remaining:.2f} kg CO₂e remaining to reach your goal." 
        #     ) 
        # else: 
        #     st.success( 
        #         "🏆 Goal reached! Great job tracking your impact." 
        #     ) 
 
        # st.divider() 
 
        # ------------------------- 
        # LATEST ACTIVITY 
        # ------------------------- 
        st.subheader("🌱 Latest Activity") 
 
        latest = df_history.iloc[0] 
 
        col1, col2 = st.columns(2) 
 
        with col1: 
            st.write( 
                f"📅 **Date:** " 
                f"{latest['date'].strftime('%Y-%m-%d')}" 
                if pd.notna(latest["date"]) 
                else "📅 **Date:** Unknown" 
            ) 
 
            st.write( 
                f"🚗 **Transport:** {latest['vehicle']} " 
                f"({latest['distance']} km)" 
            ) 
 
            st.write( 
                f"⚡ **Electricity:** " 
                f"{latest['electricity']} kWh" 
            ) 
 
            st.write( 
                f"🚿 **Water:** " 
                f"{latest['water']} L" 
            ) 
 
        with col2: 
            st.write( 
                f"🍽️ **Meals:** {latest['meals']}" 
            ) 
 
            st.write( 
                f"🥩 **Non-vegetarian meals:** " 
                f"{latest['meat_meals']}" 
            ) 
 
            st.write( 
                f"♻️ **Plastic bottles:** " 
                f"{latest['plastic_bottles']}" 
            ) 
 
            st.metric( 
                "Total Activity Impact", 
                f"{latest['total_impact']:.2f} kg CO₂e" 
            ) 
 
        st.divider() 
 
        # ------------------------- 
        # IMPACT TREND 
        # ------------------------- 
        st.subheader("📈 Impact Trend") 
 
        st.write( 
            "Your recorded environmental impact over time:" 
        ) 
 
        trend_df = df_history[ 
            ["date", "total_impact"] 
        ].copy() 
 
        trend_df["date"] = trend_df["date"].dt.strftime( 
            "%Y-%m-%d" 
        ) 
 
        trend_df = trend_df.rename( 
            columns={ 
                "date": "Date", 
                "total_impact": "Impact (kg CO₂e)" 
            } 
        ) 
 
        st.dataframe( 
            trend_df, 
            use_container_width=True, 
            hide_index=True 
        ) 
 
        st.divider() 
 
        # ------------------------- 
        # FULL HISTORY 
        # ------------------------- 
        st.subheader("📋 Activity History") 
 
        display_df = df_history.copy() 
 
        display_df["date"] = display_df["date"].dt.strftime( 
            "%Y-%m-%d" 
        ) 
 
        display_df = display_df.rename( 
            columns={ 
                "date": "Date", 
                "distance": "Distance (km)", 
                "vehicle": "Transport", 
                "electricity": "Electricity (kWh)", 
                "water": "Water (L)", 
                "meals": "Meals", 
                "meat_meals": "Non-Veg Meals", 
                "plastic_bottles": "Plastic Bottles", 
                "total_impact": "Impact (kg CO₂e)" 
            } 
        ) 
 
        st.dataframe( 
            display_df, 
            use_container_width=True, 
            hide_index=True 
        ) 
 
        st.caption( 
            "💡 Tip: Use the Home page regularly to build a " 
            "better environmental impact history and improve " 
            "your AI prediction." 
        )
# ASK ECOAI
else:

    st.title("🤖 Ask EcoAI")

    st.write(
        "Get personalized suggestions based on your EcoTrack history."
    )

    suggestions = [
        "How can I reduce my transport impact?",
        "How can I reduce my electricity usage?",
        "How can I make my food choices more eco-friendly?",
        "How can I save water?",
        "How can I reduce plastic waste?",
        "What should I focus on first?"
    ]

    st.write("💡 Choose a question:")

    selected_question = st.selectbox(
        "Suggested questions",
        [""] + suggestions
    )

    question = st.text_input(
        "Or type your own question:",
        value=selected_question
    )

    if st.button("🤖 Ask EcoAI"):

        if question.strip():

            activities = get_activities()

            st.write("🤖 **EcoAI:**")

            if activities:

                df_ai = pd.DataFrame(
                    activities,
                    columns=columns
                )

                total = df_ai["total_impact"].sum()

                latest = df_ai.iloc[0]["total_impact"]

                st.write(
                    f"You have recorded **{len(activities)} activities** "
                    f"with a total impact of **{total:.2f} kg CO₂e**."
                )

                if "transport" in question.lower() or "travel" in question.lower() or "car" in question.lower():

                    st.info(
                        f"🚗 Your latest recorded impact was "
                        f"{latest:.2f} kg CO₂e. "
                        "Try public transport, walking, cycling, or carpooling "
                        "to reduce transport emissions."
                    )

                elif "electricity" in question.lower():

                    st.info(
                        "⚡ Reduce unnecessary electricity use by switching "
                        "off unused devices and using energy-efficient appliances."
                    )

                elif "food" in question.lower() or "meal" in question.lower() or "meat" in question.lower():

                    st.info(
                        "🍽️ Try reducing meat-based meals and increasing "
                        "plant-based meals to lower food-related impact."
                    )

                elif "water" in question.lower():

                    st.info(
                        "🚿 Take shorter showers, fix leaks, and avoid "
                        "unnecessary water usage."
                    )

                elif "plastic" in question.lower() or "waste" in question.lower():

                    st.info(
                        "♻️ Reduce single-use plastic and reuse bottles "
                        "whenever possible."
                    )

                elif "focus" in question.lower() or "first" in question.lower():

                    st.info(
                        "🎯 Start with the activity that contributes the "
                        "most to your environmental impact."
                    )

                else:

                    st.info(
                        "🌱 Based on your EcoTrack history, focus on reducing "
                        "transport, electricity, food, water, and plastic use."
                    )

            else:

                st.warning(
                    "Record some activities first so EcoAI can personalize "
                    "its suggestions."
                )

        else:

            st.warning("Please select or enter a question.")
