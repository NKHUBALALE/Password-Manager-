import streamlit as st
from passwordmanager import PasswordManager

st.set_page_config(page_title="Password Manager", layout="centered")

#  SESSION STATE 
if "pm" not in st.session_state:
    st.session_state.pm = PasswordManager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

pm = st.session_state.pm

#  TITLE 
st.title(" Password Manager")

#  AUTH SECTION 
if not st.session_state.logged_in:

    st.subheader("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Master Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register"):
            success, msg = pm.register_user(username, password)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    with col2:
        if st.button("Login"):
            success, msg = pm.login(username, password)
            if success:
                st.session_state.logged_in = True
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

#  VAULT SECTION 
else:

    st.markdown("### Add New Password")

    if "generate_clicked" not in st.session_state:
        st.session_state.generate_clicked = False

    if st.session_state.generate_clicked:
        generated = pm.generate_password()
        st.session_state["password_input"] = generated
        st.session_state["generated_pwd"] = generated
        st.session_state.generate_clicked = False

    #  Inputs 
    site = st.text_input("Site (e.g. gmail.com)")
    username = st.text_input("Username / Email")
    password = st.text_input("Password", type="password", key="password_input")

    if password:
        strength = pm.calculate_strength(password)
        label = pm.strength_label(strength)

        st.progress(strength / 5)
        st.write(f"Strength: {label}")

        if strength <= 2:
            st.warning("Weak password. Add uppercase letters, numbers, or symbols.")
        elif strength == 3:
            st.info("Medium strength. Consider making it stronger.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Auto-Generate Strong Password"):
            st.session_state.generate_clicked = True
            st.rerun()

    with col2:
        if st.button("Save Password"):
            if not site or not username or not password:
                st.error("All fields are required.")
            else:
                strength = pm.calculate_strength(password)
                label = pm.strength_label(strength)

                if strength < 4:
                    st.error(f"Password is too weak ({label}). Please choose a stronger password.")
                else:
                    success, msg = pm.add_entry(site, username, password)

                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    if "generated_pwd" in st.session_state:
        st.info(f"Generated: {st.session_state['generated_pwd']}")

    st.divider()

    st.markdown("###  Stored Passwords")

    entries = pm.get_entries()

    if not entries:
        st.info("No passwords saved yet.")
    else:
        for i, entry in enumerate(entries):
            with st.expander(f" {entry['site']} ({entry['username']})"):

                st.write(f" Username: {entry['username']}")

                # Mask password by default
                toggle_key = f"toggle_{i}"
                state_key = f"show_state_{i}"

                if state_key not in st.session_state:
                    st.session_state[state_key] = False

                if st.button(" Show / Hide Password", key=toggle_key):
                    st.session_state[state_key] = not st.session_state[state_key]

                if st.session_state[state_key]:
                    st.success(f" {entry['password']}")
                else:
                    st.write(" ********")

    st.divider()

    #  Logout 
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.clear()
        st.rerun()