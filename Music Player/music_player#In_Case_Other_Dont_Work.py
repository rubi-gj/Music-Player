import numpy as np
from scipy.stats import norm

# Given data
mean_marketing = 60000     # Sample mean of Marketing
mean_sales = 57500         # Sample mean of Sales
std_marketing = 5000       # Population standard deviation of Marketing
std_sales = 4500           # Population standard deviation of Sales
n_marketing = n_sales = 50 # Sample sizes
alpha = 0.05               # Significance level

# Step 1: Calculate the standard error of the difference in means
se = np.sqrt((std_marketing**2 / n_marketing) + (std_sales**2 / n_sales))

# Step 2: Calculate the Z statistic
z = (mean_marketing - mean_sales) / se

# Step 3: Critical value for right-tailed test at alpha = 0.05
z_critical = norm.ppf(1 - alpha)

# Step 4: Calculate the p-value
p_value = 1 - norm.cdf(z)

# Step 5: Decision
print(f"Z statistic: {z:.3f}")
print(f"Critical Z value: {z_critical:.3f}")
print(f"P-value: {p_value:.4f}")

if z > z_critical:
    print("✅ Reject the null hypothesis: Marketing earns significantly more.")
else:
    print("❌ Fail to reject the null hypothesis: Not enough evidence.")
