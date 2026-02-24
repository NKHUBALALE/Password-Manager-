import streamlit as st
from passwordmanager import PasswordManager

st.set_page_config(page_title="Password Manager", layout="centered")

if "pm" not in st.session_state:
    st.session_state.pm = PasswordManager()

pm = st.session_state.pm

st.title("Password Manager")

tab1, tab2, tab3 = st.tabs(["Set Password", "Verify Password", "Statistics"])

# ---------------------------
# Set Password Tab
# ---------------------------
with tab1:
    new_password = st.text_input("Enter new password", type="password")

    if new_password:
        score = pm.calculate_strength(new_password)
        label = pm.strength_label(score)
        st.progress(score / 5)
        st.write(f"Strength: {label}")

    if st.button("Update Password"):
        success, message = pm.set_password(new_password)
        if success:
            st.success(message)
        else:
            st.error(message)

# ---------------------------
# Verify Password Tab
# ---------------------------
with tab2:
    attempt = st.text_input("Enter password to verify", type="password")

    if st.button("Verify"):
        if pm.verify_password(attempt):
            st.success("Password is correct.")
        else:
            st.error("Incorrect password.")

# ---------------------------
# Statistics Tab
# ---------------------------
with tab3:
    st.write("Total password changes:", pm.get_password_count())