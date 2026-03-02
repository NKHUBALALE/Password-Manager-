import streamlit as st
import time
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

if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""

pm = st.session_state.pm

st.title("Password Manager")

st.subheader("Set New Password")

st.info(
    "Password rules:\n"
    "- Minimum 8 characters\n"
    "- At least one lowercase letter\n"
    "- At least one uppercase letter\n"
    "- At least one number\n"
    "- At least one special character\n"
    "- Must satisfy at least 4 of the rules"
)

st.markdown("### Need help?")

if st.button("Generate strong password"):
    pwd = pm.generate_password()
    st.session_state.new_password = pwd
    st.session_state.generated_password = pwd

if st.session_state.generated_password:
    st.success(
        f"Generated password: {st.session_state.generated_password}"
    )

st.text_input(
    "Enter new password",
    type="password",
    key="new_password"
)

password = st.session_state.new_password
strength_score = 0

if password:
    strength_score = pm.calculate_strength(password)
    strength_label = pm.strength_label(strength_score)

    st.progress(strength_score / 5)
    st.write(f"Strength: {strength_label}")

update_disabled = strength_score < 4

if st.button("Update Password", disabled=update_disabled):

    success, message = pm.set_password(password)

    if success:
        st.success("Password updated successfully")

        st.session_state.verification_required = True

        time.sleep(1)

        st.rerun()

    else:
        st.error(message)


if st.session_state.verification_required:

    st.divider()
    st.subheader("Verify Password")

    st.text_input(
        "Re-enter password to confirm",
        type="password",
        key="verify_password"
    )

    if st.button("Confirm Password"):

        verified, message = pm.verify_password(
            st.session_state.verify_password
        )

        if verified:

            st.success("Password confirmed successfully")

            time.sleep(1.5)

            st.session_state.clear()

            st.rerun()

        else:
            st.error(message)


st.divider()
st.subheader("Statistics")
st.write("Total password changes:", pm.get_password_count())