import streamlit as st
import requests

API_URL = "http://backend-service:8000"

st.title("Client Registry CRM")

# Добавление клиента
st.header("Добавить клиента")
name = st.text_input("Имя")
phone = st.text_input("Телефон")
email = st.text_input("Email")
status = st.selectbox("Статус", ["new", "in_progress", "closed"])

if st.button("Добавить"):
    requests.post(f"{API_URL}/clients", json={
        "name": name,
        "phone": phone,
        "email": email,
        "status": status
    })

# Отображение
st.header("Список клиентов")
data = requests.get(f"{API_URL}/clients").json()
st.table(data)
