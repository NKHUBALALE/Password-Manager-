import streamlit as st
from datetime import datetime

def render_vault(entries, pm):
    password_counts = {}

    for entry in entries:
        pwd = entry["password"]
        password_counts[pwd] = password_counts.get(pwd, 0) + 1

    if not entries:
        st.info("No passwords saved yet.")
        return

    for i, entry in enumerate(entries):
        with st.expander(f"{entry['site']} ({entry['username']})"):

            st.write(f"Username: {entry['username']}")

            if entry.get("updated_at"):
                updated_time = datetime.strptime(entry["updated_at"], "%Y-%m-%d %H:%M:%S")
                days_ago = (datetime.now() - updated_time).days

                st.write(f"Last updated: {days_ago} days ago")

                if days_ago > 90:
                    st.warning("This password is old — consider updating")

            strength = pm.calculate_strength(entry["password"])
            label = pm.strength_label(strength)

            st.write(f"Strength: {label}")

            if strength <= 2:
                st.warning("Weak password — consider updating")
            elif strength in (3, 4):
                st.info("Medium strength — could be stronger")
            else:
                st.success("Strong password")

            if password_counts[entry["password"]] > 1:
                st.error("Password reused across multiple accounts")

            toggle_key = f"toggle_{i}"
            state_key = f"show_state_{i}"

            if state_key not in st.session_state:
                st.session_state[state_key] = False

            if st.button("Show / Hide Password", key=toggle_key):
                st.session_state[state_key] = not st.session_state[state_key]

            if st.session_state[state_key]:
                st.code(entry["password"])
            else:
                st.write("********")