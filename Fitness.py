import os
import pandas as pd
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import numpy as np

class FitnessAndHealth:
    def __init__(self, user_id, workout_data, food_data):
        self.user_id = user_id
        self.steps_data = pd.DataFrame(columns=['User_ID', 'Date', 'Steps', 'Burned Calories'])
        self.water_intake_data = pd.DataFrame(columns=['User_ID', 'Date', 'Water Intake'])
        self.workout_data = pd.DataFrame(columns=['User_ID', 'Date', 'Workout_Type', 'Duration', 'Burned Calories', 'Weight'])
        self.food_intake_data = pd.DataFrame(columns=['User_ID', 'Date','Food', 'Calories', 'Protein', 'Carbs', 'Fats'])

        self.food_data = pd.read_csv(food_data)
        self.workout_calories_data = pd.read_csv(workout_data)

    def record_steps(self, user_id, steps, date):
        calories = steps * 0.4  # Fixed decimal point
        new_data = pd.DataFrame({'User_ID': [user_id], 'Date': [date], 'Steps': [steps], 'Burned Calories': [calories]})
        self.steps_data = pd.concat([self.steps_data, new_data], ignore_index=True)

    def record_workout(self, user_id, workout_type, duration, weight, date):
        workout_info = self.workout_calories_data[self.workout_calories_data['Workout Type'] == workout_type]

        if not workout_info.empty:
            burned_calories = workout_info['Calories'].values[0] * weight * duration
            new_data = pd.DataFrame({
                'User_ID': [user_id],
                'Date': [date],
                'Workout_Type': [workout_type],
                'Duration': [duration],
                'Burned Calories': [burned_calories],
                'Weight': [weight]
            })
            self.workout_data = pd.concat([self.workout_data, new_data], ignore_index=True)
        else:
            print("Information not found for this workout type")

    def record_food(self, user_id, food_item, date):
        food_nutrition = self.food_data[self.food_data['Food'] == food_item]
        if not food_nutrition.empty:
            food_nutrition = food_nutrition.iloc[0]
            new_data = pd.DataFrame({
                'User_ID': [user_id],
                'Date': [date],
                'Food': [food_item],
                'Calories': [food_nutrition['Calories']],
                'Protein': [food_nutrition['Protein']],
                'Carbs': [food_nutrition['Carbs']],
                'Fats': [food_nutrition['Fats']]
            })
            self.food_intake_data = pd.concat([self.food_intake_data, new_data], ignore_index=True)
        else:
            print("Information not found in food data")

    def record_water(self, user_id, water_intake, date):
        new_data = pd.DataFrame({'User_ID': [user_id], 'Date': [date], 'Water Intake': [water_intake]})
        self.water_intake_data = pd.concat([self.water_intake_data, new_data], ignore_index=True)

    def get_steps_data(self):
        return self.steps_data

    def get_workout_data(self):
        return self.workout_data

    def get_food_intake_data(self):
        return self.food_intake_data

    def get_water_intake_data(self):
        return self.water_intake_data


# Simulating data
users = ['User1', 'User2', 'User3', 'User4', 'User5']
fitness_data = FitnessAndHealth(user_id=users, food_data='food_data.csv', workout_data='workout_data.csv')

workout_types = ["Wrestling", "Badminton", "Boxing, punching bag", "Bowling", "Croquet"]
food_types  = ["Lobster","Broccoli","French-fried","Blueberries","Strawberries","Muffins"]

start_date = datetime.strptime('2023-11-20', '%Y-%m-%d')
for user in users:
    current_date = start_date
    for _ in range(7):  # 1 week simulation
        chosen_workout = np.random.choice(workout_types)
        chosen_food = np.random.choice(food_types)
        fitness_data.record_steps(user, np.random.randint(5000, 15000), current_date.strftime('%d-%m-%Y'))
        fitness_data.record_workout(user, chosen_workout, np.random.randint(30, 90), np.random.randint(70, 80), current_date.strftime('%d-%m-%Y'))
        fitness_data.record_food(user, chosen_food, current_date.strftime('%d-%m-%Y'))
        fitness_data.record_water(user, np.random.randint(4, 8), current_date.strftime('%d-%m-%Y'))
        current_date += timedelta(days=1)  # Move to the next day


steps_data = fitness_data.get_steps_data()
workout_data = fitness_data.get_workout_data()
food_intake_data = fitness_data.get_food_intake_data()
water_intake_data = fitness_data.get_water_intake_data()



user_data = {user: {
    'Steps Data': steps_data[steps_data['User_ID'] == user],
    'Workout Data': workout_data[workout_data['User_ID'] == user],
    'Food Intake Data': food_intake_data[food_intake_data['User_ID'] == user],
    'Water Intake Data': water_intake_data[water_intake_data['User_ID'] == user]
} for user in users}

# Printing data for each user
for user, data in user_data.items():
    print(f"\nData for {user}:")
    print("Steps Data:")
    print(data['Steps Data'])
    print("\nWorkout Data:")
    print(data['Workout Data'])
    print("\nFood Intake Data:")
    print(data['Food Intake Data'])
    print("\nWater Intake Data:")
    print(data['Water Intake Data'])
# Creating each user folder and file
for user, data in user_data.items():
    user_folder = f"{user}_data"
    os.makedirs(user_folder, exist_ok=True)

    steps_data = data['Steps Data']
    workout_data = data['Workout Data']
    food_intake_data = data['Food Intake Data']
    water_intake_data = data['Water Intake Data']

    # Save user data to CSV files in their respective folders
    steps_data.to_csv(f"{user_folder}/steps_data.csv", index=False)
    workout_data.to_csv(f"{user_folder}/workout_data.csv", index=False)
    food_intake_data.to_csv(f"{user_folder}/food_intake_data.csv", index=False)
    water_intake_data.to_csv(f"{user_folder}/water_intake_data.csv", index=False)

#  creating Visualizations of each user data

num_users = len(user_data)
num_plots_per_user = 4

total_rows = num_users * num_plots_per_user
fig, axes = plt.subplots(total_rows // num_plots_per_user, num_plots_per_user, figsize=(15, 25))


if num_users > 1:
    axes = axes.flatten()

labels = ["Steps", "Burned Calories", "Water Intake", "Calories Intake"]

fig.legend(labels, loc='upper center', bbox_to_anchor=(0.5, 0.04), fancybox=True, shadow=True, ncol=5)

for idx, (user, data) in enumerate(user_data.items()):
    steps_data = data['Steps Data']
    workout_data = data['Workout Data']
    food_intake_data = data['Food Intake Data']
    water_intake_data = data['Water Intake Data']

    # Steps Data Visualization
    axes[idx * num_plots_per_user].plot(steps_data['Date'], steps_data['Steps'], marker='o', linestyle='-')
    axes[idx * num_plots_per_user].set_title(f"Steps Data for {user}")
    axes[idx * num_plots_per_user].set_xlabel("Date")
    axes[idx * num_plots_per_user].set_ylabel("Steps")
    axes[idx * num_plots_per_user].tick_params(axis='x', rotation=45)

    # Workout Data Visualization
    axes[idx * num_plots_per_user + 1].bar(workout_data['Date'], workout_data['Burned Calories'], color='skyblue')
    axes[idx * num_plots_per_user + 1].set_title(f"Workout Data for {user}")
    axes[idx * num_plots_per_user + 1].set_xlabel("Date")
    axes[idx * num_plots_per_user + 1].set_ylabel("Burned Calories")
    axes[idx * num_plots_per_user + 1].tick_params(axis='x', rotation=45)

    # Water Intake Data Visualization
    axes[idx * num_plots_per_user + 2].plot(water_intake_data['Date'], water_intake_data['Water Intake'],
                                            marker='o', linestyle='--', color='green')
    axes[idx * num_plots_per_user + 2].set_title(f"Water Intake Data for {user}")
    axes[idx * num_plots_per_user + 2].set_xlabel("Date")
    axes[idx * num_plots_per_user + 2].set_ylabel("Water Intake")
    axes[idx * num_plots_per_user + 2].tick_params(axis='x', rotation=45)

    # Food Intake Data Visualization with Secondary Y-axis
    ax_food_intake = axes[idx * num_plots_per_user + 3].twinx()
    ax_food_intake.bar(food_intake_data['Date'], food_intake_data['Calories'], color='salmon', alpha=0.5)
    ax_food_intake.set_ylabel("Calories Intake", color='salmon')
    ax_food_intake.tick_params(axis='y', labelcolor='salmon')

    axes[idx * num_plots_per_user + 3].set_title(f"Food Intake & Calories Data for {user}")
    axes[idx * num_plots_per_user + 3].set_xlabel("Date")
    axes[idx * num_plots_per_user + 3].set_ylabel("Food Items", color='salmon')
    axes[idx * num_plots_per_user + 3].tick_params(axis='x', rotation=45)




plt.tight_layout()
plt.subplots_adjust(bottom=0.3)  # Adjusting the bottom margin to accommodate the legend
plt.savefig("combined_data_visualizations.png", bbox_inches='tight')  # Ensure the legend is saved properly
plt.show()


