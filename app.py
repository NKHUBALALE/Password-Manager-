import streamlit as st
from passwordmanager import PasswordManager

st.set_page_config(page_title="Password Manager", layout="centered")

if "pm" not in st.session_state:
    st.session_state.pm = PasswordManager()

if "verification_required" not in st.session_state:
    st.session_state.verification_required = False

pm = st.session_state.pm

st.title("Password Manager")

st.subheader("Set New Password")

new_password = st.text_input("Enter new password", type="password")

if new_password:
    score = pm.calculate_strength(new_password)
    label = pm.strength_label(score)
    st.progress(score / 5)
    st.write(f"Strength: {label}")

if st.button("Update Password"):
    success, message = pm.set_password(new_password)
    if success:
        st.session_state.verification_required = True
        st.success("Password updated. Please verify to confirm.")
    else:
        st.error(message)

if st.session_state.verification_required:
    st.divider()
    st.subheader("Verify Password")

    attempt = st.text_input("Re-enter password to confirm", type="password")

    if st.button("Confirm Password"):
        verified, message = pm.verify_password(attempt)

        if verified:
            st.success("Password confirmed successfully.")
            st.session_state.verification_required = False
        else:
            st.error(message)

st.divider()
st.subheader("Statistics")
st.write("Total password changes:", pm.get_password_count())