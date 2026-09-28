import pandas as pd
import os

CSV_FILE = "RMS.csv"  # aapki file ka naam

df = pd.read_csv(CSV_FILE)

# Aapke Totals - Ek baar yahan apne total sites likh do (jo pehle report me the)
TOTAL_SITES = {
    "Muazzam Ali Bhatti": 53,
    "Shahid Ahmed": 70,
    "Saqlain Ali Shah": 51,
    "Abdul Waheed": 49,
    "Mohsin Ali": 90,
    "Ali Muhammad": 22,
    "Abdul Rasool": 70,
    "Saif ul Islam": 90
}

# 1. POC Wise Report
poc_summary = []
for poc, g in df.groupby("Engro POC"):
    total = TOTAL_SITES.get(poc, len(g)+40)
    offline = len(g)
    online = total - offline
    pct = round(online/total*100,1)
    r_r = (g['Summarised'] == 'R&R').sum()
    blocked = (g['Summarised'] == 'Area NW Blocked').sum()
    others = offline - r_r - blocked
    poc_summary.append([poc, total, online, offline, pct, r_r, blocked, others])

pd.DataFrame(poc_summary, columns=["POC","Total","Online","Offline","Online%","R&R","Area NW Blocked","Others"]).to_excel("POC_Wise_Report.xlsx", index=False)

# 2. Region/Cluster Wise
region_summary = df.groupby("Region").size().reset_index(name="Offline")
region_summary.to_excel("Cluster_Wise_Report.xlsx", index=False)

# 3. Sub Region Wise
sub_summary = df.groupby(["Sub Region","Summarised"]).size().unstack(fill_value=0)
sub_summary.to_excel("SubRegion_Wise_Report.xlsx")

# 4. Prolong > 3 Days (Color ke liye sorted)
prolong = df[df["Days Passed"] >= 3].sort_values("Days Passed", ascending=False)
prolong.to_excel("Prolong_03_Days_Report.xlsx", index=False)

print("4 Reports Generated: POC_Wise, Cluster_Wise, SubRegion_Wise, Prolong_03_Days")
