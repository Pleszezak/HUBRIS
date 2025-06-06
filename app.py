import streamlit as st

st.title("🔗 HUBRIS - Teste Simples")

# Verificar se conseguimos pegar as variáveis
api_key = st.secrets.get("OPENAI_API_KEY", "Não encontrada")
assistant_id = st.secrets.get("ASSISTANT_ID", "Não encontrado")

st.write(f"API Key: {api_key[:10]}... (primeiros 10 chars)")
st.write(f"Assistant ID: {assistant_id}")

if st.button("Testar Importação OpenAI"):
    try:
        import openai
        st.success("✅ OpenAI importado com sucesso!")
        
        if api_key != "Não encontrada":
            try:
                client = openai.OpenAI(api_key=api_key)
                st.success("✅ Cliente OpenAI criado!")
            except Exception as e:
                st.error(f"❌ Erro no cliente: {e}")
        else:
            st.error("❌ API Key não encontrada")
            
    except Exception as e:
        st.error(f"❌ Erro na importação: {e}")
