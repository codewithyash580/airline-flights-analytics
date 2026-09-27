import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Airline Flights Dashboard",
    page_icon="✈️",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("../data/raw/airline_flights_dataset.csv")


df = load_data()

# Title
st.title("✈️ Airline Flights Analytics Dashboard")
st.write("Explore flight prices, airlines, routes and duration.")

st.divider()

# Sidebar
st.sidebar.header("Filters")

# Airline filter
if "Airline" in df.columns:

    airline_list = df["Airline"].dropna().unique()

    selected_airlines = st.sidebar.multiselect(
        "Select Airline",
        airline_list,
        default=airline_list
    )

    data = df[df["Airline"].isin(selected_airlines)]

else:
    data = df.copy()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Flights",
        len(data)
    )

with col2:
    if "Airline" in data.columns:
        st.metric(
            "Total Airlines",
            data["Airline"].nunique()
        )

with col3:
    if "Ticket_Price_INR" in data.columns:
        st.metric(
            "Average Price",
            f"₹{data['Ticket_Price_INR'].mean():,.0f}"
        )

with col4:
    if "Scheduled_Duration_Min" in data.columns:
        st.metric(
            "Average Duration",
            f"{data['Scheduled_Duration_Min'].mean():.2f}"
        )


st.divider()


st.subheader("✈️ Flights by Airline")

if "Airline" in data.columns:

    airline_data = (
        data["Airline"]
        .value_counts()
        .reset_index()
    )

    airline_data.columns = [
        "Airline",
        "Flight_ID"
    ]

    fig = px.bar(
        airline_data,
        x="Airline",
        y="Flight_ID",
        title="Number of Flights by Airline"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.subheader("📊 Airline Distribution")

if "Airline" in data.columns:

    fig = px.pie(
        data,
        names="Airline",
        title="Flight Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.subheader("💰 Price Analysis")

col1, col2 = st.columns(2)

with col1:

    if "Ticket_Price_INR" in data.columns:

        fig = px.histogram(
            data,
            x="Ticket_Price_INR",
            nbins=30,
            title="Price Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


with col2:

    if "Airline" in data.columns and "Ticket_Price_INR" in data.columns:

        price_data = (
            data.groupby("Airline")["Ticket_Price_INR"]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            price_data,
            x="Airline",
            y="Ticket_Price_INR",
            title="Average Price by Airline"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.subheader("⏱️ Flight Duration Analysis")

if "Duration" in data.columns:

    fig = px.histogram(
        data,
        x="Scheduled_Duration_Min",
        nbins=30,
        title="Flight Duration Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


if "Source" in data.columns:

    st.subheader("🛫 Top Source Cities")

    source_data = (
        data["Source"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    source_data.columns = [
        "Source",
        "Flights"
    ]

    fig = px.bar(
        source_data,
        x="Source",
        y="Flights",
        title="Top 10 Source Cities"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


if "Destination_City" in data.columns:

    st.subheader("🛬 Top Destination Cities")

    destination_data = (
        data["Destination_City"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    destination_data.columns = [
        "Destination_City",
        "Flights"
    ]

    fig = px.bar(
        destination_data,
        x="Destination_City",
        y="Flights",
        title="Top 10 Destination Cities"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()

st.subheader("📋 Dataset Preview")

st.dataframe(
    data.head(100),
    use_container_width=True
)


csv_data = data.to_csv(index=False)

st.download_button(
    "⬇️ Download Filtered Data",
    csv_data,
    "filtered_airline_data.csv",
    "text/csv"
)