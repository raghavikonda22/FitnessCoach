import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import ollama  # Assuming you're running llama3 via Ollama

st.title("Personalized Fitness Coach!! 💪🏻")
tab1, tab2, tab3,tab4 = st.tabs(["Meal Plan", "Exercise Plan", "Tracking and Progress", "Feedback"])

with tab1:
    st.sidebar.header("Plan Your Goal")

    gender = st.radio("Gender", ["Female", "Male", "Other"])
    age = st.number_input("Age", min_value=10, max_value=100, value=25)

    height_unit = st.radio("Height Unit", ["cm", "ft/in"])
    if height_unit == "cm":
        height = st.number_input("Height (cm)", min_value=120, max_value=250, value=165)
    else:
        height_ft = st.number_input("Feet", min_value=3, max_value=8, value=5)
        height_in = st.number_input("Inches", min_value=0, max_value=11, value=5)
        height = round((height_ft * 30.48) + (height_in * 2.54), 1)

    weight_unit = st.radio("Weight Unit", ["kg", "lbs"])
    if weight_unit == "kg":
        weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        target_weight = st.number_input("Target Weight (kg)", min_value=30.0, max_value=200.0, value=60.0)
    else:
        weight_lbs = st.number_input("Current Weight (lbs)", min_value=66.0, max_value=440.0, value=154.0)
        target_weight_lbs = st.number_input("Target Weight (lbs)", min_value=66.0, max_value=440.0, value=132.0)
        weight = round(weight_lbs * 0.453592, 1)
        target_weight = round(target_weight_lbs * 0.453592, 1)

    diet_type = st.radio("Diet Type", ["Calorie Deficit", "Keto", "Balanced"])
    food_preference = st.radio("Food Preference", ["Vegetarian", "Ovo-Lacto Vegetarian", "Vegan", "Non-Vegetarian"])
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])

    allergens = st.text_input("List Any Allergens to Avoid (comma-separated, e.g., gluten, soy, dairy)", placeholder="e.g., gluten, dairy, nuts").split(',')
    allergens = [a.strip() for a in allergens if a.strip()]

    instructions = st.text_input("List any special instructions (comma-separated, e.g., coffee is mandatory)", placeholder="coffee").split(',')
    instructions = [a.strip() for a in instructions if a.strip()]

    cook_freq = st.radio("How many times do you want to cook per day?", ["Once", "Twice", "Three Times"])
    cuisine_type = st.selectbox("Preferred Cuisine Type", ["Any", "American", "Mexican", "Italian", "Indian"])

    submit = st.button(label="Generate AI Meal Plan")

    def build_prompt(gender, age, height, weight, target_weight, diet_type, food_preference, activity_level, allergens, instructions, cook_freq, cuisine_type):
        allergen_note = "None" if not allergens or "None" in allergens else ", ".join(allergens)
        instruction_note = "None" if not instructions else ", ".join(instructions)
        cook_info = cook_freq.lower()
        return f"""
    You are a meal planning assistant. Create a detailed 7-day meal plan (breakfast, lunch, dinner) for the following person:

    - Gender: {gender}
    - Age: {age}
    - Height: {height} cm
    - Current Weight: {weight} kg
    - Target Weight: {target_weight} kg
    - Diet Goal: {diet_type}
    - Food Preference: {food_preference}
    - Activity Level: {activity_level}
    - Allergens to Avoid: {allergen_note}
    - Special instructions by the user: {instruction_note}

    Include portion sizes and basic meal prep suggestions.
    Respond in markdown table format with one row per day.
    Make sure none of the meals contain the allergens listed.
    Include or eliminate items in instructions as suggested by the user.
    Include calories after every meal.
    Include the list of groceries that users should buy in the week.
    Preferred cuisine type is {cuisine_type}. The user wants to cook {cook_info} per day. Plan meals accordingly to minimize cooking effort.
    Also include total estimated cooking time (in minutes) for all meals combined per day.
    """

    def generate_meal_plan(prompt):
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']

    if submit:
        st.subheader("Your AI-Generated Meal Plan")
        prompt = build_prompt(gender, age, height, weight, target_weight, diet_type, food_preference, activity_level, allergens, instructions, cook_freq, cuisine_type)
        meal_plan_md = generate_meal_plan(prompt)
        st.markdown(meal_plan_md, unsafe_allow_html=True)
        st.markdown("Please consult a professional before following the diet plan")

with tab2:
    st.subheader("🏋 Personalized Exercise Plan")

    exercise_goal = st.radio("What's your goal?", ["Lose Fat", "Build Muscle", "Improve Endurance", "Stay Active"])
    workout_days = st.slider("How many days per week can you exercise?", 1, 7, 3)
    experience_level = st.radio("What's your experience level?", ["Beginner", "Intermediate", "Advanced"])
    hours_per_day = st.slider("How many hours can you spend per day?", 1, 2, 1)
    workout_preference = st.radio("What do you love the most", ["Yoga", "Cardio", "Strength Training", "Cardio and Strength Training", "No preference"])

    if st.button("Generate Exercise Plan"):
        prompt = f"""
        You are a fitness coach. Create a {workout_days}-day per week exercise plan for someone who wants to {exercise_goal.lower()} and based on their workout preferences {workout_preference}.
        The workout plan should be based on the hours {hours_per_day} as specified by the user. The user is a {experience_level}.
        The plan should include exercises, sets, reps and rest time. Include a mix of exercises for different muscle groups.
        Give the Exercise plan in markdown table format.
        Also include generalized suggestions for staying active throughout the day like walking, taking stairs, etc.
        """
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        st.markdown(response['message']['content'], unsafe_allow_html=True)
with tab3:
    st.subheader("📊 Tracking and Progress")
    excerccise_progress = st.number_input("How many days did you exercise this week?", min_value=0, max_value=7, value=3)

with tab4:
    st.subheader("Any Questions?? Ask your AI!! 💬")

    comment = st.text_input("Add your comments, questions, or updates about your fitness journey:")

    if st.button("Get AI Feedback"):
        prompt = f"""
        You are a smart and supportive AI personal trainer and fitness coach. Based on the user’s comment: {comment}, provide thoughtful feedback or answer any questions they may have.

        If the user is asking to adjust something (like the diet or workout), respond with helpful, personalized suggestions.

        Always encourage them to stay consistent with their healthy lifestyle. Be kind, uplifting, and positive in your tone.
        """
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        st.markdown(response['message']['content'], unsafe_allow_html=True)
