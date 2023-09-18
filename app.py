# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit



import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="ukraine_shells.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:H",
        nrows=10,
    )
     
df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
manufacturer = st.sidebar.multiselect(
    "Select the Manufacturer:",
    options=df["Manufacturer"].unique(),
    default=df["Manufacturer"].unique()
)

shell = st.sidebar.multiselect(
    "Select the Shell Type:",
    options=df["Shell"].unique(),
    default=df["Shell"].unique(),
)

df_selection = df.query(
    "Manufacturer == @manufacturer"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart: Artillery shells production dashboard")
st.markdown("##")

# TOP KPI's
total_production22 = int(df_selection["Pre-invasion yearly production"].sum())
total_production23 = int(df_selection["2023 yearly production"].sum())
total_production24 = int(df_selection["2024 yearly production"].sum())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Pre-invasion production:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("2023 yearly production:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("2024 announced production:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
total_production23 = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_production23 = px.bar(
    total_production23,
    x="Total",
    y=total_production23.index,
    orientation="h",
    title="<b>Current production by manufacturer</b>",
    color_discrete_sequence=["#0083B8"] * len(total_production23),
    template="plotly_white",
)
fig_production23.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)



left_column, right_column = st.columns(2)
right_column.plotly_chart(fig_production23, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
