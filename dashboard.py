import streamlit as st

def render_dashboard(pm):
    entries = pm.get_entries()

    total_passwords = len(entries)

    weak_count = 0
    medium_count = 0
    strong_count = 0

    for entry in entries:
        strength = pm.calculate_strength(entry["password"])

        if strength <= 2:
            weak_count += 1
        elif strength in (3, 4):
            medium_count += 1
        else:
            strong_count += 1

    if total_passwords > 0:
        security_score = int((strong_count / total_passwords) * 100)
    else:
        security_score = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total_passwords)
    col2.metric("Weak", weak_count)
    col3.metric("Medium", medium_count)
    col4.metric("Strong", strong_count)

    st.metric("Security Score", f"{security_score}%")

    if security_score < 50:
        st.error("Your passwords are mostly weak. Improve your security.")
    elif security_score < 80:
        st.warning("Your security is moderate. Consider strengthening passwords.")
    else:
        st.success("Your password security is strong.")

    st.divider()