import streamlit as st
from commands import mono

st.title("Monotonic loading with multi-surface model")
st.markdown(""" Your goal here is to get the closest possible to the blue curve on the graph.
            Give it a first run to see what the curve you need to fit is.""")

N = st.number_input("Number of surfaces", min_value=1, max_value=10, value=1, step=1)
fu = st.number_input("Ultimate force", min_value=0.0, max_value=300.0, value=100.0, step=10.0)
h = st.number_input("Hardening factor",min_value=1.0, max_value=10000.0, value=100.0, step=1.0)
b = st.number_input("Hardening exponent",min_value=0.1, max_value=5.0, value=1.0, step=0.1)
if st.button("Monotonic response simulation"):
    # Call plotting function
    fig = mono(fu,h,b,int(N))
    st.pyplot(fig)   # <-- display in Streamlit
