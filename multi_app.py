import streamlit as st
from commands import mono
from commands import cyclic

st.title("Monotonic loading with multi-surface model")
st.markdown(""" Your goal here is to get the closest possible to the black curve on the graph.
            Give it a first run to see what the curve you need to fit is.""")
st.markdown(""" Here we are looking at a Von-Mises type multi-surface model in triaxial space with pure deviatoric plasticity.
            It is defined in hyperplasticity, using a linear elastic with pure deviatoric gibbs energy, and yield surfaces written:""")
st.latex(r""" 
y^{(n)} = \frac{ \left( N \chi_q - 3 H^{(n)} \alpha^{(n)} \right)^2 }
               { \left( \frac{n}{N} f_u \right)^2  }
               -1
""")
st.markdown(""" Here the hardening moduli are given by $H=h*(1-n/N)^b$ where h is the hardening factor,
            N the number of surfaces and n the index of a surface (from 1 to N), and b """)

col1, col2 = st.columns([2,1])
with col1:
    st.markdown("**Number of surfaces:**")
with col2:
    N = st.number_input("", min_value=1, max_value=10, value=1, step=1, label_visibility="collapsed")
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("**Ultimate force (kN):**")
with col2:
    fu = st.number_input("", min_value=0.0, max_value=300.0, value=100.0, step=10.0, label_visibility="collapsed")
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("**Hardening factor:**")
with col2:
    h = st.number_input("", min_value=1.0, max_value=10000.0, value=100.0, step=1.0, label_visibility="collapsed")
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("**Hardening exponent:**")
with col2:
    b = st.number_input("", min_value=0.1, max_value=5.0, value=1.0, step=0.1, label_visibility="collapsed")

if st.button("Monotonic response simulation"):
    # Call plotting function
    fig = mono(fu,h,b,int(N))
    st.pyplot(fig)   # <-- display in Streamlit

if st.button("Cyclic response simulation"):
    # Call plotting function
    fig = cyclic(fu,h,b,int(N))
    st.pyplot(fig)   # <-- display in Streamlit
