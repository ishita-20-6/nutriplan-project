import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean visual style
sns.set_theme(style="whitegrid")


# =====================================================================
# SAMPLE INDIAN FOOD DATASET (Fallback if no external CSV is provided)
# =====================================================================
def get_sample_indian_dataset() -> pd.DataFrame:
    data = [
        # Breakfast
        {"food_name": "Idli (2 pcs)", "calories": 130, "protein_g": 4.0, "carbs_g": 26.0, "fat_g": 0.6, "fibre_g": 1.6, "diet_type": "veg", "meal_type": "breakfast"},
        {"food_name": "Masala Dosa", "calories": 250, "protein_g": 5.5, "carbs_g": 38.0, "fat_g": 8.5, "fibre_g": 2.8, "diet_type": "veg", "meal_type": "breakfast"},
        {"food_name": "Vegetable Poha", "calories": 180, "protein_g": 4.2, "carbs_g": 32.0, "fat_g": 4.0, "fibre_g": 2.5, "diet_type": "veg", "meal_type": "breakfast"},
        {"food_name": "Aloo Paratha (1 pc)", "calories": 290, "protein_g": 6.5, "carbs_g": 40.0, "fat_g": 11.5, "fibre_g": 3.4, "diet_type": "veg", "meal_type": "breakfast"},
        {"food_name": "Moong Dal Chilla (2 pcs)", "calories": 210, "protein_g": 11.5, "carbs_g": 27.0, "fat_g": 5.8, "fibre_g": 4.5, "diet_type": "veg", "meal_type": "breakfast"},
        {"food_name": "Egg Bhurji with 2 Pav", "calories": 340, "protein_g": 16.0, "carbs_g": 34.0, "fat_g": 14.5, "fibre_g": 2.0, "diet_type": "non-veg", "meal_type": "breakfast"},
        {"food_name": "Boiled Eggs (2 pcs) + Toast", "calories": 270, "protein_g": 15.5, "carbs_g": 24.0, "fat_g": 11.0, "fibre_g": 1.8, "diet_type": "non-veg", "meal_type": "breakfast"},

        # Lunch
        {"food_name": "Steamed Rice (1 cup cooked)", "calories": 205, "protein_g": 4.2, "carbs_g": 44.5, "fat_g": 0.4, "fibre_g": 0.6, "diet_type": "veg", "meal_type": "lunch"},
        {"food_name": "Tawa Roti (2 pcs)", "calories": 210, "protein_g": 6.8, "carbs_g": 42.0, "fat_g": 1.8, "fibre_g": 5.2, "diet_type": "veg", "meal_type": "lunch"},
        {"food_name": "Yellow Dal Tadka (1 bowl)", "calories": 185, "protein_g": 9.5, "carbs_g": 25.0, "fat_g": 5.0, "fibre_g": 5.8, "diet_type": "veg", "meal_type": "lunch"},
        {"food_name": "Rajma Masala (1 bowl)", "calories": 240, "protein_g": 11.0, "carbs_g": 34.0, "fat_g": 6.2, "fibre_g": 7.5, "diet_type": "veg", "meal_type": "lunch"},
        {"food_name": "Chole Masala (1 bowl)", "calories": 260, "protein_g": 11.8, "carbs_g": 36.0, "fat_g": 7.5, "fibre_g": 7.2, "diet_type": "veg", "meal_type": "lunch"},
        {"food_name": "Bhindi Masala (1 bowl)", "calories": 140, "protein_g": 3.2, "carbs_g": 14.0, "fat_g": 7.8, "fibre_g": 4.2, "diet_type": "veg", "meal_type": "lunch"},
        {"food_name": "Curd / Dahi (1 bowl)", "calories": 110, "protein_g": 5.5, "carbs_g": 7.5, "fat_g": 6.0, "fibre_g": 0.0, "diet_type": "veg", "meal_type": "lunch"},
        {"food_name": "Chicken Curry (1 bowl)", "calories": 290, "protein_g": 27.0, "carbs_g": 8.0, "fat_g": 16.0, "fibre_g": 1.5, "diet_type": "non-veg", "meal_type": "lunch"},
        {"food_name": "Fish Curry (1 bowl)", "calories": 250, "protein_g": 24.0, "carbs_g": 7.0, "fat_g": 13.5, "fibre_g": 1.2, "diet_type": "non-veg", "meal_type": "lunch"},

        # Snacks
        {"food_name": "Roasted Makhana (1 bowl)", "calories": 120, "protein_g": 3.5, "carbs_g": 21.0, "fat_g": 2.2, "fibre_g": 2.4, "diet_type": "veg", "meal_type": "snacks"},
        {"food_name": "Sprouts Chaat (1 bowl)", "calories": 150, "protein_g": 8.5, "carbs_g": 24.0, "fat_g": 2.0, "fibre_g": 5.4, "diet_type": "veg", "meal_type": "snacks"},
        {"food_name": "Masala Chai (1 cup)", "calories": 95, "protein_g": 2.5, "carbs_g": 12.0, "fat_g": 4.0, "fibre_g": 0.0, "diet_type": "veg", "meal_type": "snacks"},
        {"food_name": "Samosa (1 pc)", "calories": 260, "protein_g": 4.5, "carbs_g": 28.0, "fat_g": 14.5, "fibre_g": 2.5, "diet_type": "veg", "meal_type": "snacks"},
        {"food_name": "Roasted Peanuts & Chana (50g)", "calories": 215, "protein_g": 11.0, "carbs_g": 16.0, "fat_g": 11.5, "fibre_g": 4.8, "diet_type": "veg", "meal_type": "snacks"},
        {"food_name": "Chicken Tikka (4 pcs)", "calories": 220, "protein_g": 25.0, "carbs_g": 4.0, "fat_g": 11.0, "fibre_g": 0.8, "diet_type": "non-veg", "meal_type": "snacks"},

        # Dinner
        {"food_name": "Palak Paneer (1 bowl)", "calories": 255, "protein_g": 13.5, "carbs_g": 11.0, "fat_g": 17.5, "fibre_g": 4.6, "diet_type": "veg", "meal_type": "dinner"},
        {"food_name": "Paneer Bhurji (1 bowl)", "calories": 270, "protein_g": 15.0, "carbs_g": 9.0, "fat_g": 19.0, "fibre_g": 2.2, "diet_type": "veg", "meal_type": "dinner"},
        {"food_name": "Mixed Veg Sabzi (1 bowl)", "calories": 155, "protein_g": 4.5, "carbs_g": 18.0, "fat_g": 7.2, "fibre_g": 4.4, "diet_type": "veg", "meal_type": "dinner"},
        {"food_name": "Dal Khichdi (1 bowl)", "calories": 230, "protein_g": 8.2, "carbs_g": 38.0, "fat_g": 4.8, "fibre_g": 4.1, "diet_type": "veg", "meal_type": "dinner"},
        {"food_name": "Multigrain Roti (2 pcs)", "calories": 220, "protein_g": 7.5, "carbs_g": 41.0, "fat_g": 2.2, "fibre_g": 6.2, "diet_type": "veg", "meal_type": "dinner"},
        {"food_name": "Grilled Chicken Breast (150g)", "calories": 248, "protein_g": 46.0, "carbs_g": 0.0, "fat_g": 5.4, "fibre_g": 0.0, "diet_type": "non-veg", "meal_type": "dinner"},
        {"food_name": "Egg Curry (1 bowl)", "calories": 235, "protein_g": 14.5, "carbs_g": 9.0, "fat_g": 15.5, "fibre_g": 1.6, "diet_type": "non-veg", "meal_type": "dinner"},
    ]
    return pd.DataFrame(data)


# =====================================================================
# 1. DATA CLEANING MODULE
# =====================================================================
class DataCleaningModule:
    """Handles missing values, duplicates, data types, unit/name standardization,
    and tagging vegetarian/non-vegetarian and meal types."""

    REQUIRED_COLS = ["food_name", "calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]
    NON_VEG_KEYWORDS = ["chicken", "fish", "egg", "mutton", "prawn", "shrimp", "keema", "meat", "lamb", "tuna", "omelette"]

    def __init__(self, csv_path: str = "indian_food_nutrition.csv"):
        self.csv_path = csv_path

    def load_and_clean(self) -> pd.DataFrame:
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            print(f"[Data Cleaning] Loaded external dataset from '{self.csv_path}' ({len(df)} rows).")
        else:
            df = get_sample_indian_dataset()
            print(f"[Data Cleaning] '{self.csv_path}' not found. Using built-in Indian food dataset ({len(df)} rows).")

        # Standardize column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Map exact columns from your Kaggle CSV and common variants
        col_aliases = {
            "dish_name": "food_name",
            "food": "food_name",
            "dish": "food_name",
            "name": "food_name",
            "calories_(kcal)": "calories",
            "kcal": "calories",
            "energy_kcal": "calories",
            "energy_(kcal)": "calories",
            "protein_(g)": "protein_g",
            "protein": "protein_g",
            "carbohydrates_(g)": "carbs_g",
            "carbohydrates": "carbs_g",
            "carbs_(g)": "carbs_g",
            "carbs": "carbs_g",
            "fats_(g)": "fat_g",
            "fat_(g)": "fat_g",
            "fats": "fat_g",
            "fat": "fat_g",
            "fibre_(g)": "fibre_g",
            "fiber_(g)": "fibre_g",
            "fibre": "fibre_g",
            "fiber": "fibre_g",
        }
        df = df.rename(columns={k: v for k, v in col_aliases.items() if k in df.columns and v not in df.columns})

        if "calories" not in df.columns:
            raise ValueError(f"'calories' column missing after mapping. Found columns: {list(df.columns)}")

        # Ensure required columns exist
        for col in self.REQUIRED_COLS:
            if col not in df.columns:
                df[col] = 0.0

        # Standardize food names and remove duplicates
        df["food_name"] = df["food_name"].astype(str).str.strip().str.title()
        df = df[df["food_name"].str.len() > 0]
        df = df.drop_duplicates(subset=["food_name"], keep="first").reset_index(drop=True)

        # Convert numeric columns cleanly and handle missing values
        numeric_cols = ["calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Drop rows missing core calories, impute missing macros with median
        df = df.dropna(subset=["calories"])
        df = df[df["calories"] > 0]
        for col in ["protein_g", "carbs_g", "fat_g", "fibre_g"]:
            df[col] = df[col].fillna(df[col].median()).clip(lower=0.0)

        # Tag diet_type ('veg' or 'non-veg')
        if "diet_type" in df.columns:
            df["diet_type"] = (
                df["diet_type"]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace({"vegetarian": "veg", "non vegetarian": "non-veg", "nonveg": "non-veg"})
            )
            missing_diet = ~df["diet_type"].isin(["veg", "non-veg"])
            df.loc[missing_diet, "diet_type"] = df.loc[missing_diet, "food_name"].apply(self._infer_diet_type)
        else:
            df["diet_type"] = df["food_name"].apply(self._infer_diet_type)

        # Tag meal_type ('breakfast', 'lunch', 'snacks', 'dinner')
        if "meal_type" in df.columns:
            df["meal_type"] = df["meal_type"].astype(str).str.strip().str.lower()
            valid_meals = {"breakfast", "lunch", "snacks", "dinner"}
            invalid_mask = ~df["meal_type"].isin(valid_meals)
            df.loc[invalid_mask, "meal_type"] = df.loc[invalid_mask, :].apply(self._infer_meal_type, axis=1)
        else:
            df["meal_type"] = df.apply(self._infer_meal_type, axis=1)

        print(f"[Data Cleaning] Cleaned dataset ready: {len(df)} unique dishes.")
        return df

    def _infer_diet_type(self, food_name: str) -> str:
        name_lower = food_name.lower()
        if any(kw in name_lower for kw in self.NON_VEG_KEYWORDS):
            return "non-veg"
        return "veg"

    @staticmethod
    def _infer_meal_type(row: pd.Series) -> str:
        name = str(row["food_name"]).lower()
        cal = float(row["calories"])
        if any(k in name for k in ["idli", "dosa", "poha", "paratha", "chilla", "upma", "toast", "bhurji"]):
            return "breakfast"
        if any(k in name for k in ["chai", "tea", "coffee", "samosa", "makhana", "chaat", "sprouts", "tikka", "pakora", "snack"]):
            return "snacks"
        if any(k in name for k in ["paneer", "khichdi", "grilled", "palak"]):
            return "dinner"
        if cal < 170:
            return "snacks"
        return "lunch"


# =====================================================================
# 2. CALORIE TARGET MODULE
# =====================================================================
class CalorieTargetModule:
    """Takes a direct daily calorie goal OR estimates BMR (Mifflin-St Jeor)
    and TDEE from age, gender, height, weight, and activity level."""

    ACTIVITY_MULTIPLIERS = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }

    @classmethod
    def estimate_tdee(
        cls,
        age: int,
        gender: str,
        height_cm: float,
        weight_kg: float,
        activity_level: str = "moderate",
        goal: str = "maintain",
    ) -> float:
        gender_clean = gender.strip().lower()
        if gender_clean in ["male", "m"]:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        multiplier = cls.ACTIVITY_MULTIPLIERS.get(activity_level.strip().lower(), 1.55)
        tdee = bmr * multiplier

        goal_clean = goal.strip().lower()
        if goal_clean in ["lose", "weight_loss", "cut"]:
            tdee -= 400
        elif goal_clean in ["gain", "weight_gain", "bulk"]:
            tdee += 350

        return round(max(1200.0, tdee), 1)

    @staticmethod
    def get_calorie_target(direct_calories: float | None = None, profile: dict | None = None) -> float:
        if direct_calories is not None and direct_calories > 0:
            return float(direct_calories)
        if profile:
            return CalorieTargetModule.estimate_tdee(**profile)
        return 2000.0


# =====================================================================
# 3. MEAL PLANNER MODULE
# =====================================================================
class MealPlannerModule:
    """Splits daily calories across breakfast, lunch, snacks, and dinner
    and selects dishes within each meal's calorie budget."""

    DEFAULT_MEAL_SPLIT = {
        "breakfast": 0.25,
        "lunch": 0.35,
        "snacks": 0.15,
        "dinner": 0.25,
    }

    def __init__(self, df: pd.DataFrame, meal_split: dict[str, float] | None = None):
        self.df = df.copy()
        self.meal_split = meal_split or self.DEFAULT_MEAL_SPLIT

    def generate_plan(
        self,
        target_calories: float,
        preference: str = "veg",
        seed: int = 42,
    ) -> dict[str, pd.DataFrame]:
        rng = np.random.default_rng(seed)
        pref = preference.strip().lower()

        if pref == "veg":
            allowed_df = self.df[self.df["diet_type"] == "veg"]
        else:
            # Non-veg users can eat both non-veg and veg dishes
            allowed_df = self.df[self.df["diet_type"].isin(["veg", "non-veg"])]

        if allowed_df.empty:
            allowed_df = self.df

        plan: dict[str, pd.DataFrame] = {}

        for meal, share in self.meal_split.items():
            meal_budget = target_calories * share
            pool = allowed_df[allowed_df["meal_type"] == meal]
            if pool.empty:
                pool = allowed_df

            # Shuffle pool and greedily pick items while respecting meal budget (+15% tolerance)
            shuffled = pool.sample(frac=1.0, random_state=int(rng.integers(0, 100000))).reset_index(drop=True)
            selected_rows = []
            current_cals = 0.0

            for _, row in shuffled.iterrows():
                item_cal = float(row["calories"])
                if not selected_rows:
                    selected_rows.append(row)
                    current_cals += item_cal
                elif current_cals + item_cal <= meal_budget * 1.15 and len(selected_rows) < 3:
                    selected_rows.append(row)
                    current_cals += item_cal

                if current_cals >= meal_budget * 0.85 and len(selected_rows) >= 1:
                    break

            meal_df = pd.DataFrame(selected_rows)
            meal_df.insert(0, "meal", meal.capitalize())
            plan[meal] = meal_df

        return plan


# =====================================================================
# 4. NUTRITION ANALYSIS MODULE
# =====================================================================
class NutritionAnalysisModule:
    """Calculates total nutrients of the generated plan and compares
    macronutrient splits with standard recommended ranges."""

    # Recommended macro % of total calories:
    # Protein: 15-30%, Carbs: 45-65%, Fat: 20-35%
    RECOMMENDED_RANGES = {
        "Protein (%)": (15.0, 30.0),
        "Carbs (%)": (45.0, 65.0),
        "Fat (%)": (20.0, 35.0),
    }

    @classmethod
    def analyze_plan(cls, plan: dict[str, pd.DataFrame], target_calories: float) -> dict:
        combined = pd.concat(plan.values(), ignore_index=True)

        totals = {
            "calories": round(combined["calories"].sum(), 1),
            "protein_g": round(combined["protein_g"].sum(), 1),
            "carbs_g": round(combined["carbs_g"].sum(), 1),
            "fat_g": round(combined["fat_g"].sum(), 1),
            "fibre_g": round(combined["fibre_g"].sum(), 1),
        }

        macro_cals = {
            "protein": totals["protein_g"] * 4.0,
            "carbs": totals["carbs_g"] * 4.0,
            "fat": totals["fat_g"] * 9.0,
        }
        total_macro_cals = sum(macro_cals.values()) or 1.0

        actual_pct = {
            "Protein (%)": round((macro_cals["protein"] / total_macro_cals) * 100, 1),
            "Carbs (%)": round((macro_cals["carbs"] / total_macro_cals) * 100, 1),
            "Fat (%)": round((macro_cals["fat"] / total_macro_cals) * 100, 1),
        }

        comparison_rows = []
        for label, (low, high) in cls.RECOMMENDED_RANGES.items():
            actual = actual_pct[label]
            if actual < low:
                status = "Below Range"
            elif actual > high:
                status = "Above Range"
            else:
                status = "Within Range"
            comparison_rows.append({
                "Macro": label,
                "Actual (%)": actual,
                "Recommended (%)": f"{low:.0f}% - {high:.0f}%",
                "Status": status,
            })

        meal_summary = (
            combined.groupby("meal", sort=False)[["calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]]
            .sum()
            .round(1)
        )

        return {
            "combined_df": combined,
            "totals": totals,
            "target_calories": target_calories,
            "actual_pct": actual_pct,
            "comparison_df": pd.DataFrame(comparison_rows),
            "meal_summary": meal_summary,
        }


# =====================================================================
# 5. VISUALISATION MODULE
# =====================================================================
class VisualisationModule:
    """Generates meal calorie share pie chart, macronutrient split chart,
    food comparison bar chart, and correlation/nutrient heatmap."""

    @staticmethod
    def plot_plan_charts(analysis: dict, save_prefix: str | None = None) -> None:
        combined = analysis["combined_df"]
        meal_summary = analysis["meal_summary"]
        actual_pct = analysis["actual_pct"]

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("NutriPlan India — One-Day Meal Plan Nutritional Breakdown", fontsize=15, fontweight="bold")

        # 1. Meal-wise Calorie Share (Pie Chart)
        axes[0, 0].pie(
            meal_summary["calories"],
            labels=meal_summary.index,
            autopct="%1.1f%%",
            startangle=140,
        )
        axes[0, 0].set_title("Calorie Share by Meal")

        # 2. Macronutrient Split vs Recommended Midpoint (Bar Chart)
        labels = list(actual_pct.keys())
        actual_vals = [actual_pct[k] for k in labels]
        rec_midpoints = [
            sum(NutritionAnalysisModule.RECOMMENDED_RANGES[k]) / 2.0 for k in labels
        ]
        x = np.arange(len(labels))
        width = 0.35

        axes[0, 1].bar(x - width / 2, actual_vals, width, label="Actual (%)")
        axes[0, 1].bar(x + width / 2, rec_midpoints, width, label="Rec. Midpoint (%)", alpha=0.75)
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(labels)
        axes[0, 1].set_ylabel("Percentage of Macro Calories")
        axes[0, 1].set_title("Macronutrient Split")
        axes[0, 1].legend()

        # 3. Dish-wise Calories & Protein Comparison (Horizontal Bar Chart)
        dish_plot_df = combined.set_index("food_name")[["calories", "protein_g"]].sort_values("calories")
        dish_plot_df["calories"].plot(kind="barh", ax=axes[1, 0])
        axes[1, 0].set_xlabel("Calories (kcal)")
        axes[1, 0].set_title("Selected Dishes by Calorie Content")

        # 4. Nutrient Heatmap Across Selected Dishes
        heatmap_cols = ["calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]
        heat_df = combined.set_index("food_name")[heatmap_cols]
        # Normalize columns (0-1) so different scales are readable on a single heatmap
        norm_heat = (heat_df - heat_df.min()) / (heat_df.max() - heat_df.min() + 1e-9)
        sns.heatmap(
            norm_heat,
            annot=heat_df.round(1),
            fmt="g",
            cmap="YlGnBu",
            cbar_kws={"label": "Normalized Scale (0-1)"},
            ax=axes[1, 1],
        )
        axes[1, 1].set_title("Dish Nutrient Comparison (Raw Values Annotated)")

        plt.tight_layout(rect=[0, 0.02, 1, 0.95])
        if save_prefix:
            plt.savefig(f"{save_prefix}_plan_overview.png", dpi=150)
        plt.show()


# =====================================================================
# 6. DATASET INSIGHTS MODULE
# =====================================================================
class DatasetInsightsModule:
    """Surfaces top protein, lowest calorie, top fibre dishes,
    and nutritional correlation insights from the full dataset."""

    @staticmethod
    def show_insights(df: pd.DataFrame, top_n: int = 5, save_heatmap_path: str | None = None) -> None:
        print("\n" + "=" * 60)
        print("DATASET INSIGHTS")
        print("=" * 60)

        print(f"\nTop {top_n} Highest-Protein Indian Foods:")
        print(df.nlargest(top_n, "protein_g")[["food_name", "diet_type", "protein_g", "calories"]].to_string(index=False))

        print(f"\nTop {top_n} Lowest-Calorie Indian Foods:")
        print(df.nsmallest(top_n, "calories")[["food_name", "diet_type", "calories", "fibre_g"]].to_string(index=False))

        print(f"\nTop {top_n} Highest-Fibre Indian Foods:")
        print(df.nlargest(top_n, "fibre_g")[["food_name", "diet_type", "fibre_g", "calories"]].to_string(index=False))

        num_cols = ["calories", "protein_g", "carbs_g", "fat_g", "fibre_g"]
        corr = df[num_cols].corr().round(2)
        print("\nNutrient Correlation Matrix:")
        print(corr.to_string())

        plt.figure(figsize=(7, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Dataset Nutrient Correlation Heatmap")
        plt.tight_layout()
        if save_heatmap_path:
            plt.savefig(save_heatmap_path, dpi=150)
        plt.show()


# =====================================================================
# APPLICATION RUNNER
# =====================================================================
def print_report(analysis: dict) -> None:
    totals = analysis["totals"]
    print("\n" + "=" * 60)
    print("NUTRIPLAN INDIA — ONE-DAY MEAL PLAN")
    print("=" * 60)

    for meal, meal_df in analysis["meal_summary"].iterrows():
        print(f"\n--- {meal} (Subtotal: {meal_df['calories']} kcal) ---")
        items = analysis["combined_df"][analysis["combined_df"]["meal"] == meal]
        for _, item in items.iterrows():
            print(
                f"  • {item['food_name']} | {item['calories']} kcal | "
                f"P: {item['protein_g']}g, C: {item['carbs_g']}g, F: {item['fat_g']}g, Fibre: {item['fibre_g']}g"
            )

    print("\n" + "-" * 60)
    print(
        f"Total Planned Calories: {totals['calories']} kcal "
        f"(Target: {analysis['target_calories']} kcal)"
    )
    print(
        f"Total Macros -> Protein: {totals['protein_g']}g | "
        f"Carbs: {totals['carbs_g']}g | Fat: {totals['fat_g']}g | Fibre: {totals['fibre_g']}g"
    )
    print("\nMacronutrient Split vs Recommended Range:")
    print(analysis["comparison_df"].to_string(index=False))
    print("-" * 60)


def main() -> None:
    # Step 1: Clean dataset
    cleaner = DataCleaningModule(csv_path="indian_food_nutrition.csv")
    clean_df = cleaner.load_and_clean()

    # Step 2: Determine daily calorie target
    # Option A: Direct target -> target_cals = CalorieTargetModule.get_calorie_target(direct_calories=2000)
    # Option B: Estimate from user profile
    user_profile = {
        "age": 21,
        "gender": "female",
        "height_cm": 162,
        "weight_kg": 56,
        "activity_level": "moderate",
        "goal": "maintain",
    }
    target_calories = CalorieTargetModule.get_calorie_target(profile=user_profile)
    preference = "veg"  # "veg" or "non-veg"

    # Step 3: Generate meal plan
    planner = MealPlannerModule(clean_df)
    plan = planner.generate_plan(target_calories=target_calories, preference=preference, seed=42)

    # Step 4: Analyze nutrition & print summary
    analysis = NutritionAnalysisModule.analyze_plan(plan, target_calories)
    print_report(analysis)

    # Step 5: Visualise meal plan
    VisualisationModule.plot_plan_charts(analysis)

    # Step 6: Show overall dataset insights
    DatasetInsightsModule.show_insights(clean_df, top_n=5)


if __name__ == "__main__":
    main()