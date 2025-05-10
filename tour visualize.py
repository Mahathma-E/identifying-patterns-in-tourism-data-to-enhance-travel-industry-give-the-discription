

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("/content/sample_data/large_tourism_data.csv")

# Show first few rows
print("Preview of dataset:")
display(df.head())

# 1. Top 10 Countries by Tourism Revenue
top_revenue = df.sort_values(by="tourism_receipts", ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(data=top_revenue, x="tourism_receipts", y="country", palette="viridis")
plt.title("Top 10 Countries by Tourism Revenue")
plt.xlabel("Revenue (USD)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# 2. Top 10 Countries by Tourist Arrivals
top_arrivals = df.sort_values(by="tourism_arrivals", ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(data=top_arrivals, x="tourism_arrivals", y="country", palette="magma")
plt.title("Top 10 Countries by Tourist Arrivals")
plt.xlabel("Arrivals")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# 3. Tourism Revenue by Continent
continent_revenue = df.groupby("continent")["tourism_receipts"].sum().reset_index()

plt.figure(figsize=(8,5))
sns.barplot(data=continent_revenue, x="continent", y="tourism_receipts", palette="cubehelix")
plt.title("Tourism Revenue by Continent")
plt.xlabel("Continent")
plt.ylabel("Revenue (USD)")
plt.tight_layout()
plt.show()

# 4. Peak Season Distribution
season_data = df["peak_season"].value_counts()

plt.figure(figsize=(6,4))
season_data.plot(kind="pie", autopct='%1.1f%%', colors=sns.color_palette("Set3"))
plt.title("Distribution of Peak Tourism Seasons")
plt.ylabel("")
plt.tight_layout()
plt.show()
