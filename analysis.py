"""UK online retail customer analytics (UCI Online Retail II, public data).
Cleaning, monthly revenue, repeat-purchase rate, RFM segmentation, cohort retention,
Pareto concentration, product pairs. Prints markdown tables. Run in Google Colab."""
import io, zipfile, urllib.request, numpy as np, pandas as pd
URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
raw = urllib.request.urlopen(URL, timeout=120).read()
z = zipfile.ZipFile(io.BytesIO(raw)); name = [n for n in z.namelist() if n.endswith(".xlsx")][0]
df = pd.concat(pd.read_excel(z.open(name), sheet_name=None, engine="openpyxl").values(), ignore_index=True)
df.columns = ["invoice","stock","desc","qty","date","price","cust","country"]
n0 = len(df)
df["date"] = pd.to_datetime(df["date"])
df = df[~df["invoice"].astype(str).str.startswith("C")]           # cancellations
df = df[(df.qty > 0) & (df.price > 0)]
df["rev"] = df.qty * df.price
print(f"Rows: {n0:,} raw -> {len(df):,} after removing cancellations and non-positive qty/price; {df.date.min().date()} to {df.date.max().date()}\n")
d = df.dropna(subset=["cust"]).copy(); d["cust"] = d.cust.astype(int)
print(f"Rows with a customer id: {len(d):,} ({len(d)/len(df):.0%}); customers: {d.cust.nunique():,}; invoices: {d.invoice.nunique():,}\n")

m = df.set_index("date").rev.resample("MS").sum()
print("## Monthly revenue (GBP)"); print(m.round(0).astype(int).to_frame("revenue").to_markdown(), "\n")
q4 = df[df.date.dt.month.isin([10,11,12])].rev.sum() / df.rev.sum()
print(f"Share of revenue in Oct-Dec: {q4:.1%}\n")
c = df.groupby("country").rev.sum().sort_values(ascending=False)
print(f"UK share of revenue: {c.get('United Kingdom',0)/c.sum():.1%}; top 5 countries:\n", (c.head(5)/c.sum()).round(3).to_frame("share").to_markdown(), "\n")

inv = d.groupby(["cust","invoice"]).agg(date=("date","min"), rev=("rev","sum")).reset_index()
per = inv.groupby("cust").agg(orders=("invoice","nunique"), revenue=("rev","sum"), last=("date","max"), first=("date","min"))
print(f"AOV (per invoice): GBP {inv.rev.mean():.2f} (median {inv.rev.median():.2f}); repeat-customer rate (2+ invoices): {(per.orders>=2).mean():.1%}\n")
top = per.revenue.sort_values(ascending=False); k = int(len(top)*0.2)
print(f"Top 20% of customers generate {top.head(k).sum()/top.sum():.1%} of customer revenue\n")

snap = d.date.max() + pd.Timedelta(days=1)
r = pd.DataFrame({"R": (snap - per["last"]).dt.days, "F": per.orders, "M": per.revenue})
r["Rs"] = pd.qcut(r.R, 5, labels=[5,4,3,2,1]).astype(int)
r["Fs"] = pd.qcut(r.F.rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
r["Ms"] = pd.qcut(r.M.rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
def seg(x):
    if x.Rs >= 4 and x.Fs >= 4: return "Champions"
    if x.Rs >= 3 and x.Fs >= 3: return "Loyal"
    if x.Rs >= 4 and x.Fs <= 2: return "New / promising"
    if x.Rs <= 2 and x.Fs >= 3: return "At risk"
    return "Lost / low value"
r["segment"] = r.apply(seg, axis=1)
s = r.groupby("segment").agg(customers=("M","size"), revenue=("M","sum"), avg_recency_days=("R","mean"), avg_orders=("F","mean"))
s["revenue_share"] = (s.revenue / s.revenue.sum()).round(3); s["customer_share"] = (s.customers / s.customers.sum()).round(3)
print("## RFM segments"); print(s.round(1).sort_values("revenue", ascending=False).to_markdown(), "\n")

inv["cohort"] = inv.groupby("cust").date.transform("min").dt.to_period("M")
inv["period"] = inv.date.dt.to_period("M")
inv["idx"] = (inv.period - inv.cohort).apply(lambda x: x.n)
coh = inv.groupby(["cohort","idx"]).cust.nunique().unstack(fill_value=0)
ret = coh.div(coh[0], axis=0)
print("## Average cohort retention (share of a cohort's customers who buy again N months later)")
print(ret[[1,2,3,6]].mean().round(3).to_frame("avg_retention").rename(index=lambda i: f"month {i}").to_markdown(), "\n")

dd = d[d.desc.notna()]; topd = dd.groupby("desc").rev.sum().sort_values(ascending=False)
print("## Top 10 products by revenue"); print(topd.head(10).round(0).astype(int).to_frame("revenue").to_markdown(), "\n")
keep = set(dd.groupby("desc").invoice.nunique().sort_values(ascending=False).head(150).index)
b = dd[dd.desc.isin(keep)].drop_duplicates(["invoice","desc"])
pairs = {}
for _, g in b.groupby("invoice").desc:
    items = sorted(g.tolist())
    if 2 <= len(items) <= 12:
        for i in range(len(items)):
            for j in range(i+1, len(items)): pairs[(items[i], items[j])] = pairs.get((items[i], items[j]), 0) + 1
print("## Most frequent product pairs (invoices containing both)")
print(pd.DataFrame(sorted(pairs.items(), key=lambda kv: -kv[1])[:8], columns=["pair","invoices"]).to_markdown(index=False))
