import streamlit as st
from PIL import Image
import streamlit_extras
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Projet Interpromo 2025 - Groupe 1",
    page_icon="📊",
    layout="wide"
)
button_style = """button{
    opacity: 0  ;
    padding-top: 50%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    margin: 0;
    float: none;
}
"""
container_style = """{
    z-index: 0;
    background_color: #171717;
    border-top: 2px solid #373737;
}
"""
# ---------- Load images ----------
imgtit = Image.open("images/logos.png")
gen_profile = Image.open("images/pp_generic.png")
pp_amine = Image.open("images/IMG_3710.jpeg")
pp_sekou = Image.open("images/pp-sekou.jfif")
pp_em = Image.open("images/pp-emeline.jfif")
pp_kim = Image.open("images/pp-kim.jfif")

# ---------- Page title ----------

left_co, cent_co,last_co = st.columns(3)
with last_co:
    st.image(imgtit, width=300)
st.write('')
st.title("Projet Interpromo 2025 - Groupe 1")
st.markdown("### Présentation des membres du groupe")

# ---------- Page ----------

st.markdown('## Promo M2')
st.markdown("""
  <style>
    img{
      border-radius: 50%;
    }
  </style>
""", unsafe_allow_html=True)
col1, col2, col3, col4= st.columns(4)
with col1:
    st.markdown("<a style = 'line-height:10px;font-size : 30px; font-weight : 100;' href='https://www.linkedin.com/in/amine-nouacer-7092b3266/'>Amine\n\n NOUACER</a>",unsafe_allow_html=True)
    st.image(pp_amine, width=200)
with col2:
    st.markdown("<a style = 'line-height:10px;font-size : 30px; font-weight : 100;' href='https://www.linkedin.com/in/justin-massabie-078927282/'>Justin\n\n MASSABIE</a>",unsafe_allow_html=True)
    st.image(gen_profile, width=200)
with col3:
    st.markdown("<a style = 'line-height:10px;font-size : 30px; font-weight : 100;' href='https://www.linkedin.com/in/nicolas-pham-hoang/'>Nicolas\n\n PHAM</a>",unsafe_allow_html=True)
    st.image(gen_profile, width=200)
st.write('')
st.markdown('## Promo M1')
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<a style = 'line-height:10px;font-size : 30px; font-weight : 100;' href='https://www.linkedin.com/in/s%C3%A9kou-oular%C3%A9-a3297b2ba/'>Sékou\n\n OULARÉ</a>",unsafe_allow_html=True)
    st.image(pp_sekou   , width=200)
with col2:
    st.markdown("<a style = 'line-height:10px;font-size : 30px; font-weight : 100;' href='https://www.linkedin.com/in/emeline-kleinhans-4002712b7/'>Emeline\n\n KLEINHANS</a>",unsafe_allow_html=True)
    st.image(pp_em, width=200)
with col3:
    st.markdown("<a style = 'line-height:10px;font-size : 30px; font-weight : 100;' href='https://www.linkedin.com/in/kim-ishimwe-3964602a0/'>Kim\n\n ISHIMWE</a>",unsafe_allow_html=True)
    st.image(pp_kim, width=200)
with col4:
    st.markdown("<a style = 'line-height:10px;font-size : 30px; font-weight : 100;' href='https://www.linkedin.com/in/géraud-hermann-nougbodohoue-86aa60347/'>Hermann\n\n NOUGBODOHOUE</a>",unsafe_allow_html=True)
    st.image(gen_profile, width=200)