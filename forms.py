import streamlit as st

def render_add_password(pm, show_success):

    if "success_msg" not in st.session_state:
        st.session_state.success_msg = ""

    if st.session_state.success_msg:
        st.success(st.session_state.success_msg)
        st.session_state.success_msg = ""
    
    if "generate_clicked" not in st.session_state:
        st.session_state.generate_clicked = False

    if "confirm_update" not in st.session_state:
        st.session_state.confirm_update = False

    if st.session_state.generate_clicked:
        generated = pm.generate_password()
        st.session_state["password_input"] = generated
        st.session_state["generated_pwd"] = generated
        st.session_state.generate_clicked = False

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
                return

            strength = pm.calculate_strength(password)
            label = pm.strength_label(strength)

            if strength <= 2:
                 st.error("Weak password. Add uppercase letters, numbers, or symbols.")
                 return
    
            if strength < 4:
                st.error(f"Password is too weak ({label}). Please choose a stronger password.")
                return

            if pm.entry_exists(site, username) and not st.session_state.confirm_update:
                st.session_state.confirm_update = True
                st.warning("This account already exists. Click save again to confirm update.")
                return

            success, msg = pm.add_entry(site, username, password)

            if success:
                st.session_state.confirm_update = False
                if strength == 5:
                    show_success("Strong password saved.")
                elif strength == 4:
                    show_success("Good password saved. Still room to improve.")
                else:
                    show_success(msg)

    if "generated_pwd" in st.session_state:
        st.info(f"Generated: {st.session_state['generated_pwd']}")