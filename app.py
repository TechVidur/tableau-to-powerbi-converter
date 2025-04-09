import streamlit as st
import openai
from openai import OpenAIError, RateLimitError, AuthenticationError

# ❗️ WARNING: This is for demo only — DO NOT hardcode keys in production
client = openai.OpenAI(api_key="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")

def convert_formula_tableau_to_dax(tableau_formula, model="gpt-3.5-turbo"):
    prompt = f"""
    Convert the following Tableau formula to Power BI DAX. Only return the formula itself, no explanation.

    Tableau Formula:
    {tableau_formula}

    Power BI DAX:
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except AuthenticationError:
        return "❌ Invalid API key or no access to the model."
    except RateLimitError:
        return "❌ Rate limit exceeded. Please check your quota."
    except OpenAIError as e:
        return f"❌ OpenAI Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Tableau → Power BI DAX Converter", layout="centered")
st.title("🔁 Tableau → Power BI DAX Converter")

tableau_formula = st.text_area("📋 Enter your Tableau formula here:")

if st.button("✨ Convert"):
    if not tableau_formula.strip():
        st.warning("Please enter a Tableau formula.")
    else:
        with st.spinner("Converting..."):
            dax_result = convert_formula_tableau_to_dax(tableau_formula)
        st.success("✅ Power BI DAX Equivalent:")
        st.code(dax_result, language="DAX")
