import streamlit as st
from passwordmanager import PasswordManager
from dashboard import render_dashboard
from forms import render_add_password
from vault_ui import render_vault


st.set_page_config(page_title="Password Manager", layout="centered")

#  SESSION STATE 
if "pm" not in st.session_state:
    st.session_state.pm = PasswordManager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

pm = st.session_state.pm

def show_success(msg):
    st.session_state.success_msg = msg
    st.rerun()
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
    #  Dashboard 
    render_dashboard(pm)


    st.markdown("### Add New Password")
    render_add_password(pm, show_success)

    st.divider()

    st.markdown("###  Stored Passwords")

    entries = pm.get_entries()
    render_vault(entries, pm)
    st.divider()

    #  Logout 
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.clear()
        st.rerun()