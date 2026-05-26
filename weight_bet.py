import streamlit as st
import datetime
import time
import pandas as pd
import streamlit.components.v1 as components
from sqlalchemy import create_engine, text


# Set page layout to wide and give it a fun title
st.set_page_config(page_title="THE 5KG BLOOD PACT", layout="wide", page_icon="🏋️‍♂️")

# ----------------------------------------------------
# 1. LIVE BACKEND DATA ENGINE (Supabase SQL Connection)
# ----------------------------------------------------
# Fetch the connection string securely from secrets.toml
db_uri = st.secrets["postgres_uri"]

# Create an SQLAlchemy engine connection to PostgreSQL
engine = create_engine(db_uri)

# Use Pandas to run a live SQL query against your cloud database
try:
    query = "SELECT * FROM challenge_data;"
    df = pd.read_sql(query, con=engine)
except Exception as e:
    st.error(f"Database connection failed! Error: {e}")
    df = pd.DataFrame(columns=["name", "week", "weight_lost_kg", "penalty"])

# Aggregate data using Pandas
marauchi_total_lost = df[df["name"] == "Marauchi"]["weight_lost_kg"].sum()
tandukar_total_lost = df[df["name"] == "Tandukar"]["weight_lost_kg"].sum()

# Get the latest penalty status
marauchi_latest_penalty = df[df["name"] == "Marauchi"]["penalty"].iloc[-1] if not df[df["name"] == "Marauchi"].empty else "None"
tandukar_latest_penalty = df[df["name"] == "Tandukar"]["penalty"].iloc[-1] if not df[df["name"] == "Tandukar"].empty else "None"

# Calculate days remaining for the backend math
target_date = datetime.date(2026, 7, 16)
today = datetime.date.today()
days_left = (target_date - today).days
if days_left == 0:
    st.balloons()

# ----------------------------------------------------
# 2. THE HEADER & JUDGEMENT CLOCK (CENTERED)
# ----------------------------------------------------
st.markdown("<h1 style='text-align: center;'>The 5kg Blood Pact: Countdown to July 16</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Two competitors. One deadline. Total accountability.</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: silver; font-size: 12px;'>*The Referee has final authority of all disputes, excuses, technicalities, and acts of desperation.</p>", unsafe_allow_html=True)
st.write("") 

target_year = 2026
target_month = 7
target_day = 16

countdown_html = f"""
<div style="
    background-color: #e1f5fe; 
    border: 1px solid #b3e5fc; 
    padding: 20px; 
    border-radius: 10px; 
    text-align: center;
    font-family: 'Source Sans Pro', sans-serif;
    color: #0369a1;
    max-width: 600px;
    margin: 0 auto;
">
    <h3 style="margin: 0 0 10px 0; font-size: 20px;">Time Remaining Until Weigh-in</h3>
    <div id="countdown-timer" style="font-size: 28px; font-weight: bold;">Calculating time...</div>
</div>
<script>
    var countDownDate = new Date({target_year}, {target_month - 1}, {target_day}, 0, 0, 0).getTime();
    var x = setInterval(function() {{
        var now = new Date().getTime();
        var distance = countDownDate - now;
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        document.getElementById("countdown-timer").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s";
        
        if (distance < 0) {{
            clearInterval(x);
            document.getElementById("countdown-timer").innerHTML = "TIME'S UP!";
        }}
    }}, 1000);
</script>
"""
components.html(countdown_html, height=130)
st.markdown("---")

# ----------------------------------------------------
# 3. DATA ANALYTICS: REQUIRED BURN RATE CALCULATIONS
# ----------------------------------------------------
st.markdown("<h2 style='text-align: center;'>📊 Analytics Mainframe</h2>", unsafe_allow_html=True)
st.write("")

# Calculate Burn Rates (Grams needed per day)
marauchi_remaining = max(5.0 - marauchi_total_lost, 0.0)
marauchi_burn_rate = (marauchi_remaining / days_left) * 1000 if days_left > 0 else 0

tandukar_remaining = max(5.0 - tandukar_total_lost, 0.0)
tandukar_burn_rate = (tandukar_remaining / days_left) * 1000 if days_left > 0 else 0

col_spacer1, col_metrics, col_spacer2 = st.columns([0.5, 4, 0.5])

with col_metrics:
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center;'>🔥 Required Daily Deficit To Hit 5kg Goal</h4>", unsafe_allow_html=True)
        
        burn_col1, burn_col2 = st.columns(2)
        with burn_col1:
            st.metric(
                label="Marauchi's Required Burn Rate", 
                value=f"{marauchi_burn_rate:.0f} grams / day", 
                delta=f"{marauchi_remaining:.1f} kg left to lose",
                delta_color="inverse",
            )
        with burn_col2:
            st.metric(
                label="Tandukar's Required Burn Rate", 
                value=f"{tandukar_burn_rate:.0f} grams / day", 
                delta=f"{tandukar_remaining:.1f} kg left to lose",
                delta_color="inverse"
            )

st.write("")
st.markdown("---")

# ----------------------------------------------------
# 4. COMPETITOR PROGRESS
# ----------------------------------------------------
st.markdown("<h2 style='text-align: center;'>💪🏾Path to Ascension</h2>", unsafe_allow_html=True)
st.write("")

# Force the progress percentage to clamp perfectly between 0.0 and 1.0 as a sanity check for the progress bars.
marauchi_pct = max(0.0, min(marauchi_total_lost / 5.0, 1.0))  
tandukar_pct = max(0.0, min(tandukar_total_lost / 5.0, 1.0))

col1, col2, col3, col4 = st.columns([0.5, 2, 2, 0.5])

with col2:
    st.markdown(f"### 🏃‍♂️ Marauchi's Journey")
    if marauchi_total_lost > 5:
        st.metric(label="Total Weight Lost", value=f"{marauchi_total_lost:.1f} kg", delta=f"Exceeded goal by {marauchi_total_lost - 5.0:.1f} kg", delta_color="normal")
    else:    
        st.metric(label="Total Weight Lost", value=f"{marauchi_total_lost:.1f} kg", delta=f"Needs {5.0 - marauchi_total_lost:.1f} kg more", delta_color="inverse")
    st.progress(marauchi_pct)
    st.caption(f"Marauchi is {marauchi_pct*100:.0f}% of the way there.")

with col3:
    st.markdown(f"### 🏃‍♂️ Tandukar's Journey")
    if tandukar_total_lost > 5:
        st.metric(label="Total Weight Lost", value=f"{tandukar_total_lost:.1f} kg", delta=f"Exceeded goal by {tandukar_total_lost - 5.0:.1f} kg", delta_color="normal")
    else:
        st.metric(label="Total Weight Lost", value=f"{tandukar_total_lost:.1f} kg", delta=f"Needs {5.0 - tandukar_total_lost:.1f} kg more", delta_color="inverse")
    st.progress(tandukar_pct)
    st.caption(f"Tandukar is {tandukar_pct*100:.0f}% of the way there.")

st.markdown("---")

# ----------------------------------------------------
# 5. REFEREE FEED & SIDE BETS
# ----------------------------------------------------
col_feed, col_bets = st.columns([2, 1])

with col_feed:
    st.markdown("### 📢 The Referee's Notice Board")
    st.error("🚨 **May 25:** Marauchi ate 3 burgers, 2 hashed browns, 5 pieces of nuggets, an udon and 3 tempuras without the referee. The referee compensated by having Cheetos.")
    st.success("🍏 **May 24:** A deep gut-cleanse was done by all parties.")
    st.warning("⚠️ **May 22:** Tandukar lied about sharing food and made his younger brother take the burden. These kinds of antics are discouraged.")
    
    st.markdown("### 🪵 Match History logs")
    with st.expander("Expand Full History"):    
        for index, row in df.iterrows():
            if row['weight_lost_kg'] > 0:
                st.success(f"📈 **{row['week']}:** {row['name']} deserves a メロンパン! {row['name']} lost **{row['weight_lost_kg']} kg**! (Penalty Status: {row['penalty']})")
            else:
                st.error(f"📉 **{row['week']}:** {row['name']} slipped up and gained **{abs(row['weight_lost_kg'])} kg**. (Penalty Status: {row['penalty']})")

with col_bets:
    st.markdown("### 💰 Active Stipulations")
    with st.container(border=True):
        st.markdown("""
        **🍕 The Ebi-Mayo Clause:** Whoever over achieves by 1kg or more will need to eat ebi-mayo and ichigo milk in one sitting. 
        
        **📲 The Final Stakes:** Participants who fail the challenge will need to abide by the forfeit set in the inital blood pact.
        """)

col_spacer3, col_footer, col_spacer4 = st.columns([1, 2, 1])

with col_footer:
    st.markdown("")  # optional spacing
    st.markdown("")  # optional spacing
    st.markdown(
        "<p style='text-align:center;'>Try to buy the Referee, and you will answer for it."
        "<br>All participants are bound by the terms of the blood pact and accept that the referee is the sole owner of the Modulus.</p>", unsafe_allow_html=True)

# ----------------------------------------------------
# 6. REFEREE ADMINISTRATION PANEL (PASSWORD PROTECTED)
# ----------------------------------------------------

with st.sidebar:

    st.markdown("### 🔒 Referee Mainframe")

    ref_password = st.text_input("Enter Referee Master Password to unlock controls:", type="password", key="ref_pass_box")

    if ref_password == st.secrets["ref_master_pass"]: 
        st.success("🔓 Access Granted. Welcome, Referee.")
        
        # Create an organized form layout container
        with st.form("ref_data_entry_form", clear_on_submit=True):
            st.markdown("#### 📝 Log Weekly Weigh-In Metrics")
            
            # Form Input Fields matching your schema
            input_name = st.selectbox("Select Competitor:", ["Marauchi", "Tandukar"])
            input_week = st.number_input("Which week number is this?", min_value=1, max_value=52, step=1)
            input_weight = st.number_input("Weight Lost this week (use negative if they GAINED weight):", value=0.0, step=0.1)
            input_penalty = st.selectbox("Issue Penalty Status:", ["None", "Yellow Card", "Red Card", "Kebab", "Cheese Dog", "Olive Chicken"])
            formatted_week = f"Week {input_week}"
            
            # The submit button
            submit_button = st.form_submit_button("Commit to Cloud Database")
            
            if submit_button:
                try:
                    with engine.begin() as connection:
                        insert_query = text("""
                            INSERT INTO challenge_data (name, week, weight_lost_kg, penalty) 
                            VALUES (:name, :week, :weight_lost_kg, :penalty)
                        """)
                        connection.execute(insert_query, {
                            "name": input_name,
                            "week": formatted_week,
                            "weight_lost_kg": input_weight,
                            "penalty": input_penalty
                        })
                    st.success(f"Data for {input_name} in Week {input_week} has been successfully logged!")
                    time.sleep(1.5)
                    # if "ref_pass_box" in st.session_state:
                    #     del st.session_state["ref_pass_box"]
                    st.rerun(scope="app")

                except Exception as e:
                        st.error(f"Failed to write to database! Error: {e}")
    else:
        st.warning("Only the Referee can access the mainframe.")