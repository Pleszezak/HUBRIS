import streamlit as st
import openai
import os
import time
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Configuração da página
st.set_page_config(
    page_title="HUBRIS - Conselho Estratégico",
    page_icon="🔗",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1F4E79;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}
.user-message {
    background-color: #E8F4FD;
    border-left: 4px solid #2196F3;
}
.assistant-message {
    background-color: #F0F8F0;
    border-left: 4px solid #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>🔗 HUBRIS - Conselho Estratégico</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Orquestração de ecossistemas de inovação</p>", unsafe_allow_html=True)

# Inicializar estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# Função para enviar mensagem ao assistente
def send_message_to_assistant(message):
    try:
        # Adiciona mensagem ao thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=message
        )
        
        # Executa o assistente
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID
        )
        
        # Aguarda conclusão
        with st.spinner("HUBRIS está orquestrando..."):
            while run.status in ["queued", "in_progress"]:
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )
        
        if run.status == "completed":
            # Busca as mensagens
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            
            # Retorna a última mensagem do assistente
            for msg in messages.data:
                if msg.role == "assistant":
                    return msg.content[0].text.value
                    
        else:
            return f"Erro: {run.status}"
            
    except Exception as e:
        return f"Erro na comunicação: {str(e)}"

# Interface principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Conversa com HUBRIS")
    
    # Exibe histórico de mensagens
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>Você:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>HUBRIS:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.subheader("🎯 Comandos Rápidos")
    
    quick_commands = [
        "Conselho, como orquestrar um novo ecossistema",
        "Conselho, qual o consenso para maximizar impacto sistêmico",
        "Conselho, ativem 5 perspectivas para este challenge institucional",
        "Conselho, como transformar esta iniciativa em modelo replicável"
    ]
    
    for i, cmd in enumerate(quick_commands):
        if st.button(f"💡 {cmd[:30]}...", key=f"cmd_{i}"):
            st.session_state.user_input = cmd

# Input do usuário
user_input = st.chat_input("Digite sua mensagem para HUBRIS...")

# Processa mensagem do usuário
if user_input:
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Envia para o assistente e recebe resposta
    response = send_message_to_assistant(user_input)
    
    # Adiciona resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun para atualizar a interface
    st.rerun()

# Sidebar com informações
with st.sidebar:
    st.subheader("📋 Sobre HUBRIS")
    st.write("""
    HUBRIS é seu conselho estratégico virtual para orquestração de ecossistemas, 
    especializado em conectar corporações, startups, academia e governo para 
    acelerar transformação sistêmica.
    """)
    
    st.subheader("🎯 Como Usar")
    st.write("""
    - Use comandos como "Conselho, como orquestrar..."
    - Pense em impacto sistêmico e ecossistemas
    - Peça perspectivas de múltiplos stakeholders
    - Solicite modelos replicáveis
    """)
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.rerun()
