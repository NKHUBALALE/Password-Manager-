import streamlit as st
from passwordmanager import PasswordManager

st.set_page_config(page_title="Password Manager", layout="centered")

if "pm" not in st.session_state:
    st.session_state.pm = PasswordManager()

if "verification_required" not in st.session_state:
    st.session_state.verification_required = False

if "new_password" not in st.session_state:
    st.session_state.new_password = ""

if "verify_password" not in st.session_state:
    st.session_state.verify_password = ""

pm = st.session_state.pm

st.title("Password Manager")

st.subheader("Set New Password")

# Password Input
st.session_state.new_password = st.text_input(
    "Enter new password",
    type="password",
    key="new_password_input"
)

password = st.session_state.new_password
strength_score = 0

if password:
    strength_score = pm.calculate_strength(password)
    strength_label = pm.strength_label(strength_score)

    st.progress(strength_score / 5)
    st.write(f"Strength: {strength_label}")

# Disable button unless strong enough
update_disabled = strength_score < 4

if st.button("Update Password", disabled=update_disabled):
    success, message = pm.set_password(password)

    if success:
        st.session_state.verification_required = True
        st.success("Password updated. Please verify to confirm.")
    else:
        st.error(message)

# Forced Verification Section
if st.session_state.verification_required:
    st.divider()
    st.subheader("Verify Password")

    st.session_state.verify_password = st.text_input(
        "Re-enter password to confirm",
        type="password",
        key="verify_password_input"
    )

    if st.button("Confirm Password"):
        verified, message = pm.verify_password(st.session_state.verify_password)

        if verified:
            st.success("Password confirmed successfully.")

            # Auto-clear fields
            st.session_state.new_password = ""
            st.session_state.verify_password = ""
            st.session_state.verification_required = False

            st.rerun()
        else:
            st.error(message)

st.divider()
st.subheader("Statistics")
st.write("Total password changes:", pm.get_password_count())