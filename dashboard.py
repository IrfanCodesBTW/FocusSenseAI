import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

data_dir = "data/raw_sessions"
files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

if not files:
    print("No sessions yet. Run tracker.py first!")
    exit()

print(f"Found {len(files)} session(s)\n")

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
    print("FocusSense AI Dashboard")
    print("="*50)
    print("1. Focus Pie Chart (All Sessions)")
    print("2. Focus Pie Chart (Today Only)")
    print("3. Session-wise Breakdown")
    print("4. Emotion Distribution")
    print("5. Exit")
    choice = input("Choose (1-5): ")

    if choice == "1":  # All sessions pie chart
        focus_counts = data["focus_state"].value_counts()
        colors = {'FOCUSED': '#2ecc71', 'DISTRACTED': '#e74c3c', 'NO_FACE': '#95a5a6'}
        colors_list = [colors.get(state, '#333') for state in focus_counts.index]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Pie chart
        ax1.pie(focus_counts.values, labels=focus_counts.index, autopct='%1.1f%%', 
               colors=colors_list, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
        ax1.set_title('Focus Distribution (All Sessions)', fontsize=14, weight='bold')
        
        # Stats table
        total = len(data)
        focused = len(data[data["focus_state"] == "FOCUSED"])
        distracted = len(data[data["focus_state"] == "DISTRACTED"])
        no_face = len(data[data["focus_state"] == "NO_FACE"])
        
        focus_score = round(focused / total * 100, 1)
        
        stats_text = f"""
        Total Records: {total}
        
        FOCUSED: {focused} ({round(focused/total*100, 1)}%)
        DISTRACTED: {distracted} ({round(distracted/total*100, 1)}%)
        NO_FACE: {no_face} ({round(no_face/total*100, 1)}%)
        
        Focus Score: {focus_score}%
        """
        
        ax2.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax2.axis('off')
        
        plt.tight_layout()
        plt.show()

    elif choice == "2":  # Today's pie chart
        today = datetime.now().date()
        df_today = data[data["date"] == today]
        
        if df_today.empty:
            print("❌ No data for today yet.")
            continue
        
        focus_counts = df_today["focus_state"].value_counts()
        colors = {'FOCUSED': '#2ecc71', 'DISTRACTED': '#e74c3c', 'NO_FACE': '#95a5a6'}
        colors_list = [colors.get(state, '#333') for state in focus_counts.index]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Pie chart
        ax1.pie(focus_counts.values, labels=focus_counts.index, autopct='%1.1f%%',
               colors=colors_list, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
        ax1.set_title(f'Focus Distribution - Today ({today})', fontsize=14, weight='bold')
        
        # Stats
        total = len(df_today)
        focused = len(df_today[df_today["focus_state"] == "FOCUSED"])
        distracted = len(df_today[df_today["focus_state"] == "DISTRACTED"])
        no_face = len(df_today[df_today["focus_state"] == "NO_FACE"])
        
        focus_score = round(focused / total * 100, 1)
        
        stats_text = f"""
        Total Records: {total}
        
        FOCUSED: {focused} ({round(focused/total*100, 1)}%)
        DISTRACTED: {distracted} ({round(distracted/total*100, 1)}%)
        NO_FACE: {no_face} ({round(no_face/total*100, 1)}%)
        
        Daily Focus Score: {focus_score}%
        """
        
        ax2.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        ax2.axis('off')
        
        plt.tight_layout()
        plt.show()

    elif choice == "3":  # Session breakdown
        print("\nAvailable sessions:")
        for i, f in enumerate(files, 1):
            print(f"{i}. {f}")
        
        try:
            idx = int(input("Select session (number): ")) - 1
            df_session = pd.read_csv(os.path.join(data_dir, files[idx]))
            
            focus_counts = df_session["focus_state"].value_counts()
            colors = {'FOCUSED': '#2ecc71', 'DISTRACTED': '#e74c3c', 'NO_FACE': '#95a5a6'}
            colors_list = [colors.get(state, '#333') for state in focus_counts.index]
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            ax1.pie(focus_counts.values, labels=focus_counts.index, autopct='%1.1f%%',
                   colors=colors_list, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
            session_name = files[idx].replace("session_", "").replace(".csv", "")
            ax1.set_title(f'Session Focus Distribution\n{session_name}', fontsize=14, weight='bold')
            
            total = len(df_session)
            focused = len(df_session[df_session["focus_state"] == "FOCUSED"])
            distracted = len(df_session[df_session["focus_state"] == "DISTRACTED"])
            no_face = len(df_session[df_session["focus_state"] == "NO_FACE"])
            
            focus_score = round(focused / total * 100, 1)
            
            stats_text = f"""
            Total Records: {total}
            
            FOCUSED: {focused} ({round(focused/total*100, 1)}%)
            DISTRACTED: {distracted} ({round(distracted/total*100, 1)}%)
            NO_FACE: {no_face} ({round(no_face/total*100, 1)}%)
            
            Session Focus Score: {focus_score}%
            """
            
            ax2.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                    family='monospace', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
            ax2.axis('off')
            
            plt.tight_layout()
            plt.show()
        except (ValueError, IndexError):
            print("❌ Invalid selection")

    elif choice == "4":  # Emotion distribution
        emotion_counts = data["emotion"].value_counts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        colors_emotion = {'HAPPY': '#f1c40f', 'NEUTRAL': '#3498db', 'STRESSED': '#e74c3c', 'SLEEPY': '#9b59b6'}
        colors_list = [colors_emotion.get(emotion, '#333') for emotion in emotion_counts.index]
        
        ax1.pie(emotion_counts.values, labels=emotion_counts.index, autopct='%1.1f%%',
               colors=colors_list, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
        ax1.set_title('Emotion Distribution (All Sessions)', fontsize=14, weight='bold')
        
        total = len(data)
        stats_text = f"""
        Total Recordings: {total}
        
        HAPPY: {len(data[data['emotion']=='HAPPY'])} ({round(len(data[data['emotion']=='HAPPY'])/total*100, 1)}%)
        NEUTRAL: {len(data[data['emotion']=='NEUTRAL'])} ({round(len(data[data['emotion']=='NEUTRAL'])/total*100, 1)}%)
        STRESSED: {len(data[data['emotion']=='STRESSED'])} ({round(len(data[data['emotion']=='STRESSED'])/total*100, 1)}%)
        SLEEPY: {len(data[data['emotion']=='SLEEPY'])} ({round(len(data[data['emotion']=='SLEEPY'])/total*100, 1)}%)
        """
        
        ax2.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
        ax2.axis('off')
        
        plt.tight_layout()
        plt.show()

    elif choice == "5":
        print("Goodbye! 👋")
        break
    else:
        print("❌ Invalid choice. Try again.")
