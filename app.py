import streamlit as st
import os

# Teste das variáveis de ambiente
st.title("🔧 Debug - Variáveis de Ambiente")

# Verificar se as variáveis existem
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

st.write("**Teste das Variáveis:**")
st.write(f"OPENAI_API_KEY existe: {api_key is not None}")
if api_key:
    st.write(f"OPENAI_API_KEY primeiros 10 chars: {api_key[:10]}...")
else:
    st.error("OPENAI_API_KEY não encontrada!")

st.write(f"ASSISTANT_ID: {assistant_id}")

# Teste de importação
try:
    import openai
    st.success("✅ OpenAI importado com sucesso")
    
    if api_key:
        try:
            client = openai.OpenAI(api_key=api_key)
            st.success("✅ Cliente OpenAI criado com sucesso")
        except Exception as e:
            st.error(f"❌ Erro ao criar cliente: {str(e)}")
    
except Exception as e:
    st.error(f"❌ Erro na importação: {str(e)}")

# Mostrar todas as variáveis de ambiente (sem valores sensíveis)
st.write("**Variáveis de ambiente disponíveis:**")
env_vars = list(os.environ.keys())
st.write(f"Total: {len(env_vars)} variáveis")
for var in sorted(env_vars):
    if 'OPENAI' in var or 'ASSISTANT' in var:
        st.write(f"- {var}: {'✅ Definida' if os.getenv(var) else '❌ Vazia'}")
