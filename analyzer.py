import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

data_dir = "data/raw_sessions"
files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

if not files:
    print("No sessions yet. Run tracker.py first!")
    exit()

print(f"Found {len(files)} session(s)")

# Load all data
dfs = []
for f in files:
    df = pd.read_csv(os.path.join(data_dir, f))
    if len(df) <= 1:
        continue
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["session"] = f.replace("session_", "").replace(".csv", "")
    dfs.append(df)

if not dfs:
    print("No valid data rows found.")
    exit()

data = pd.concat(dfs, ignore_index=True)

while True:
    print("\n" + "="*50)
    print("FocusSense AI Analyzer")
    print("1. Today Summary")
    print("2. All Sessions")
    print("3. Trends")
    print("4. Recommendations")
    print("5. Exit")
    choice = input("Choose (1-5): ")

    if choice == "1":   # Today
        today = datetime.now().date()
        df = data[data["date"] == today]
        if df.empty:
            print("No data today.")
            continue
        total = len(df)
        focused = len(df[df["focus_state"] == "FOCUSED"])
        score = round(focused / total * 100, 1)
        print(f"\nFocus Score Today: {score}%")
        print(f"Focused time: {focused}s | Distractions: {total-focused}s")

        # Charts
        df_plot = df.copy()
        df_plot["focus_val"] = df_plot["focus_state"].map({"FOCUSED": 100, "DISTRACTED": 0, "NO_FACE": 20})
        plt.figure(figsize=(10,4))
        plt.plot(df_plot["timestamp"], df_plot["focus_val"])
        plt.title("Focus Timeline Today")
        plt.show()

        plt.figure(figsize=(6,6))
        df["emotion"].value_counts().plot.pie(autopct='%1.0f%%')
        plt.title("Emotions Today")
        plt.show()

    elif choice == "2":   # Sessions
        for i, f in enumerate(files):
            print(f"{i+1}. {f}")
        idx = int(input("Enter number: ")) - 1
        df = pd.read_csv(os.path.join(data_dir, files[idx]))
        total = len(df)
        focused = len(df[df["focus_state"] == "FOCUSED"])
        score = round(focused / total * 100, 1)
        print(f"Focus Score: {score}%")
        plt.plot(df.index, df["focus_state"].map({"FOCUSED":100,"DISTRACTED":0,"NO_FACE":20}))
        plt.title("Session Timeline")
        plt.show()

    elif choice == "3":   # Trends
        daily = data.groupby("date").apply(
            lambda g: round(len(g[g["focus_state"]=="FOCUSED"])/len(g)*100,1) if len(g) else 0
        )
        daily.plot(kind='line', marker='o', title="Daily Focus %")
        plt.show()

    elif choice == "4":   # Recommendations
        avg = data.groupby("date").apply(
            lambda g: round(len(g[g["focus_state"]=="FOCUSED"])/len(g)*100,1) if len(g) else 0
        ).mean()
        if avg < 60:
            print("Focus is low → Try Pomodoro 25 min")
        elif avg < 75:
            print("Good, but remove phone distractions")
        else:
            print("Excellent focus!")

        sleepy = (data["emotion"] == "SLEEPY").mean() * 100
        if sleepy > 20:
            print("You look sleepy often → Take short breaks")

    elif choice == "5":
        break