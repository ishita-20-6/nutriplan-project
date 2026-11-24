import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from nutriplan_india import (
    DataCleaningModule,
    CalorieTargetModule,
    MealPlannerModule,
    NutritionAnalysisModule,
)

st.set_page_config(
    page_title="NutriPlan India — Indian Diet Planner",
    page_icon="🥗",
    layout="wide",
)
sns.set_theme(style="whitegrid")


@st.cache_data
def get_cleaned_dataset(csv_path: str = "indian_food_nutrition.csv") -> pd.DataFrame:
    cleaner = DataCleaningModule(csv_path=csv_path)
    df = cleaner.load_and_clean()

    # Exclude non-meal items (sauces, jams, oils, powders) for cleaner meal plans
    exclude_keywords = [
        "sauce", "jam", "murabba", "pickle", "chutney", "ghee",
        "oil", "butter", "sugar", "syrup", "squash", "powder"
    ]
    mask_exclude = df["food_name"].str.lower().apply(lambda name: any(k in name for k in exclude_keywords))
    filtered_df = df[~mask_exclude].reset_index(drop=True)
    return filtered_df if not filtered_df.empty else df


def main() -> None:
    st.title("🥗 NutriPlan India")
    st.caption(
        "A Python-Based Indian Diet Planner Using Calorie Targets and Nutritional Data Analysis "
        "(For general nutritional information only; not medical advice)"
    )

    clean_df = get_cleaned_dataset("indian_food_nutrition.csv")

    # Sidebar Controls
    st.sidebar.header("⚙️ Calorie & Diet Settings")
    target_mode = st.sidebar.radio(
        "How do you want to set daily calories?",
        ["Estimate from Profile (TDEE)", "Enter Direct Calorie Goal"],
    )

    if target_mode == "Enter Direct Calorie Goal":
        direct_cal = st.sidebar.number_input(
            "Daily Calorie Goal (kcal)", min_value=1200, max_value=4500, value=2000, step=50
        )
        target_calories = CalorieTargetModule.get_calorie_target(direct_calories=float(direct_cal))
    else:
        age = st.sidebar.slider("Age (years)", 16, 75, 21)
        gender = st.sidebar.selectbox("Gender", ["female", "male"])
        height_cm = st.sidebar.number_input("Height (cm)", 130.0, 210.0, 162.0, step=1.0)
        weight_kg = st.sidebar.number_input("Weight (kg)", 35.0, 150.0, 56.0, step=0.5)
        activity_level = st.sidebar.selectbox(
            "Activity Level",
            ["sedentary", "light", "moderate", "active", "very_active"],
            index=2,
        )
        goal = st.sidebar.selectbox(
            "Goal",
            ["maintain", "lose", "gain"],
        )
        target_calories = CalorieTargetModule.get_calorie_target(
            profile={
                "age": age,
                "gender": gender,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "activity_level": activity_level,
                "goal": goal,
            }
        )
        st.sidebar.info(f"Estimated Daily Target: **{target_calories} kcal**")

    preference = st.sidebar.selectbox("Food Preference", ["veg", "non-veg"])

    if "plan_seed" not in st.session_state:
        st.session_state.plan_seed = 42
    if st.sidebar.button("🔄 Generate New Plan", use_container_width=True):
        st.session_state.plan_seed = int(np.random.randint(1, 100000))

    # Generate & Analyze Plan using existing modules
    planner = MealPlannerModule(clean_df)
    plan = planner.generate_plan(
        target_calories=target_calories,
        preference=preference,
        seed=st.session_state.plan_seed,
    )
    analysis = NutritionAnalysisModule.analyze_plan(plan, target_calories)
    totals = analysis["totals"]
    combined_df = analysis["combined_df"]

    # Top KPI Row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Calories", f"{totals['calories']} kcal", f"Target: {target_calories}")
    c2.metric("Protein", f"{totals['protein_g']} g")
    c3.metric("Carbohydrates", f"{totals['carbs_g']} g")
    c4.metric("Fats", f"{totals['fat_g']} g")
    c5.metric("Fibre", f"{totals['fibre_g']} g")

    tab1, tab2, tab3 = st.tabs(["🍽️ One-Day Meal Plan", "📊 Visualisations", "📈 Dataset Insights"])

    with tab1:
        st.subheader(f"One-Day Indian Meal Plan ({preference.upper()})")
        for meal in ["Breakfast", "Lunch", "Snacks", "Dinner"]:
            meal_items = combined_df[combined_df["meal"] == meal]
            subtotal = round(meal_items["calories"].sum(), 1) if not meal_items.empty else 0.0
            with st.expander(f"**{meal}** — Subtotal: {subtotal} kcal", expanded=True):
                if meal_items.empty:
                    st.write("No dishes selected for this meal.")
                else:
                    st.dataframe(
                        meal_items[["food_name", "diet_type", "calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]],
                        use_container_width=True,
                        hide_index=True,
                    )

        st.subheader("Macronutrient Split vs Recommended Range")
        st.dataframe(analysis["comparison_df"], use_container_width=True, hide_index=True)

    with tab2:
        left_col, right_col = st.columns(2)

        with left_col:
            fig_pie, ax_pie = plt.subplots(figsize=(6, 4.5))
            meal_summary = analysis["meal_summary"]
            ax_pie.pie(
                meal_summary["calories"],
                labels=meal_summary.index,
                autopct="%1.1f%%",
                startangle=140,
            )
            ax_pie.set_title("Calorie Share by Meal")
            st.pyplot(fig_pie)

        with right_col:
            fig_bar, ax_bar = plt.subplots(figsize=(6, 4.5))
            labels = list(analysis["actual_pct"].keys())
            actual_vals = [analysis["actual_pct"][k] for k in labels]
            rec_midpoints = [sum(NutritionAnalysisModule.RECOMMENDED_RANGES[k]) / 2.0 for k in labels]
            x = np.arange(len(labels))
            width = 0.35

            ax_bar.bar(x - width / 2, actual_vals, width, label="Actual (%)")
            ax_bar.bar(x + width / 2, rec_midpoints, width, label="Rec. Midpoint (%)", alpha=0.75)
            ax_bar.set_xticks(x)
            ax_bar.set_xticklabels(labels)
            ax_bar.set_ylabel("Percentage (%)")
            ax_bar.set_title("Macronutrient Split")
            ax_bar.legend()
            st.pyplot(fig_bar)

        st.subheader("Selected Dishes Nutrient Heatmap")
        fig_heat, ax_heat = plt.subplots(figsize=(10, 4.5))
        heatmap_cols = ["calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]
        heat_df = combined_df.set_index("food_name")[heatmap_cols]
        norm_heat = (heat_df - heat_df.min()) / (heat_df.max() - heat_df.min() + 1e-9)
        sns.heatmap(norm_heat, annot=heat_df.round(1), fmt="g", cmap="YlGnBu", ax=ax_heat)
        st.pyplot(fig_heat)

    with tab3:
        st.subheader(f"Cleaned Dataset Overview ({len(clean_df)} Dishes)")
        i1, i2, i3 = st.columns(3)
        with i1:
            st.markdown("**Top 5 Highest-Protein Foods**")
            st.dataframe(
                clean_df.nlargest(5, "protein_g")[["food_name", "diet_type", "protein_g", "calories"]],
                use_container_width=True,
                hide_index=True,
            )
        with i2:
            st.markdown("**Top 5 Lowest-Calorie Foods**")
            st.dataframe(
                clean_df.nsmallest(5, "calories")[["food_name", "diet_type", "calories", "fibre_g"]],
                use_container_width=True,
                hide_index=True,
            )
        with i3:
            st.markdown("**Top 5 Highest-Fibre Foods**")
            st.dataframe(
                clean_df.nlargest(5, "fibre_g")[["food_name", "diet_type", "fibre_g", "calories"]],
                use_container_width=True,
                hide_index=True,
            )

        st.subheader("Dataset Nutrient Correlation Matrix")
        fig_corr, ax_corr = plt.subplots(figsize=(7, 4.5))
        corr = clean_df[["calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]].corr().round(2)
        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax_corr)
        st.pyplot(fig_corr)


if __name__ == "__main__":
    main()