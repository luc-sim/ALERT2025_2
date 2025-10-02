import streamlit as st
from commands import mono

st.title("Monotonic loading with multi-surface model")

N = st.slider("Number of surfaces", 1, 10, 1)
fu = st.slider("Ultimate force", 0, 300, 10)
h = st.slider("Hardening factor",1,10000,1)
b = st.slider("Hardening exponent",0.1,5,0.1)
if st.button("Calculate"):

    # Call plotting function
    fig = mono(fu,h,b,NN)
    st.pyplot(fig)   # <-- display in Streamlit
