import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model_dir = r"C:\Users\Dell\Downloads\Auto_Complete_NLP\gpt-2\GPT2-model-fine-tuning.ipynb.ipynb"
model = GPT2LMHeadModel.from_pretrained(model_dir)
tokenizer = GPT2Tokenizer.from_pretrained(model_dir)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


st.set_page_config(page_title="كيبورد تنبؤي", layout="centered")
st.markdown("<h1 style='text-align: center;'>⌨️ GPT-2 كيبورد تنبؤي باستخدام </h1>", unsafe_allow_html=True)


if "current_text" not in st.session_state:
    st.session_state.current_text = ""
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []


st.markdown("### 📝 :النص الحالي")
st.text_area("", value=st.session_state.current_text, height=150, disabled=True, label_visibility="collapsed")


if st.button("🔁 إعادة تعيين النص"):
    st.session_state.current_text = ""
    st.session_state.suggestions = ""
    st.rerun()


def generate_suggestions(prompt, num_suggestions=3):
    suggestions = []
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    for _ in range(num_suggestions * 2):
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_new_tokens=1,
                do_sample=True,
                top_k=20,
                pad_token_id=tokenizer.eos_token_id
            )
        new_token_id = output[0][input_ids.shape[-1]:]
        word = tokenizer.decode(new_token_id, skip_special_tokens=True).strip()
        if word and word not in suggestions:
            suggestions.append(word)
        if len(suggestions) >= num_suggestions:
            break
    return suggestions


start_input = st.text_input("✏️ : ابدأ الكتابة", value="", disabled=bool(st.session_state.current_text))
if start_input and not st.session_state.current_text:
    st.session_state.current_text = start_input.strip()
    st.session_state.suggestions = generate_suggestions(start_input.strip())
    st.rerun()


if st.session_state.current_text:
    st.markdown("### 💡: الكلمات المقترحة")
    cols = st.columns(3)
    for i, word in enumerate(st.session_state.suggestions):
        if cols[i].button(word):
            st.session_state.current_text += " " + word
            st.session_state.suggestions = generate_suggestions(st.session_state.current_text)
            st.rerun()