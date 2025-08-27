
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the CSV log
df = pd.read_csv("detection_log.csv")

# Convert Timestamp to datetime object
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Show total counts
summary = df['Prediction'].value_counts()
print("\n Detection Summary:")
print(summary)

# Plot pie chart
plt.figure(figsize=(6, 6))
colors = ['#8BC34A', '#FF5722']
summary.plot.pie(autopct='%1.1f%%', colors=colors, startangle=140)
plt.title("Mold Detection Results")
plt.ylabel("")
plt.tight_layout()
plt.savefig("mold_detection_pie_chart.png")
plt.show()

# Plot detection confidence over time
plt.figure(figsize=(10, 5))
df_sorted = df.sort_values("Timestamp")
plt.plot(df_sorted["Timestamp"], df_sorted["Confidence"], marker='o')
plt.title("Detection Confidence Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Confidence (%)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("confidence_over_time.png")
plt.show()
