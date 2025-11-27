import streamlit as st
import pandas as pd
import uuid

# --- 🎯 CONFIGURAÇÃO E AUTENTICAÇÃO DO GOOGLE SHEETS ---

# O Streamlit agora usa st.connection para autenticar e gerenciar o gspread
conn = st.connection("gsheets", type="spreadsheet") 

# --- FUNÇÕES DE DADOS PARA PLANILHA GOOGLE ---

@st.cache_data 
def load_data(): 
    """Carrega os dados do Google Sheet usando a conexão nativa."""
    try:
        # Usa o método read() do Streamlit Connection para carregar a primeira aba
        df = conn.read(worksheet="Página1", ttl=5) # 'ttl=5' define o tempo de cache (5 segundos)
        
        # O Streamlit Connection retorna um DataFrame. Se estiver vazio, cria o DF vazio.
        if df.empty or 'ID' not in df.columns:
             # Retorna um DataFrame vazio com as colunas esperadas
             df = pd.DataFrame(columns=['ID','Item','Categoria','Status'])
        
        return df
    
    except Exception as e:
        st.error(f"Erro ao carregar dados do Google Sheets. Verifique o SHEET_ID e o nome da ABA (deve ser 'Página1'). Erro: {e}")
        return pd.DataFrame(columns=['ID','Item','Categoria','Status'])


def save_data(novo_presente_data): 
    """Adiciona uma nova linha à planilha Google usando a conexão nativa."""
    try:
        # Puxa os dados existentes (para garantir a estrutura)
        df_existente = conn.read(worksheet="Página1")
        
        # Cria um novo DataFrame com os novos dados
        novo_df = pd.DataFrame([novo_presente_data])
        
        # Concatena e escreve de volta na planilha
        conn.write(df=novo_df, worksheet="Página1", append=True)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados no Google Sheets. Verifique as permissões de EDITOR. Erro: {e}")
        return False

# --- CONFIGURAÇÃO INICIAL E RESTO DO CÓDIGO ---

st.set_page_config(
    layout='wide',
    page_title='Lista de Presentes de Casamento | Ana & Roger',
    page_icon='🎁'
)

# --- CSS PERSONALIZADO (DESIGN: FUNDO ESCURO E LETRAS BRANCAS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;400;700&family=Playfair+Display:wght@700&display=swap');

    :root {
        --primary-color: #F7D71C; /* Dourado */
        --secondary-color: #FFFFFF; /* Branco para texto principal/títulos */
        --accent-color: #E91E63; /* Rosa de Destaque */
        --text-color-dark: #333333; /* Texto escuro para formulário/lista */
        --text-color-light: #FFFFFF; /* Texto claro para o fundo escuro */
        --bg-color: #36454F; /* Cinza Chumbo */
    }

    /* 1. Fundo da Aplicação: Forçando o cinza chumbo */
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-color) !important;
    }
    
    /* 2. Conteúdo Central (Lista e Formulário) - Fundo Branco */
    .st-emotion-cache-13l37u7, .stForm, .stDataFrame { 
        background-color: #FFFFFF !important; 
    }
    .st-emotion-cache-13l37u7 { 
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 3. CORREÇÃO CRÍTICA: Texto Principal (fora dos blocos brancos) deve ser CLARO */
    .stText, .stMarkdown, [data-testid="stVerticalBlock"] > div > div > div > div.stMarkdown > div, .st-emotion-cache-1l09y6f {
        color: var(--text-color-light) !important; /* CORREÇÃO APLICADA AQUI */
    }
    
    /* Estilo Geral do Corpo */
    body {
        font-family: 'Montserrat', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-color-light); 
    }

    h1, h2, h3 { 
        font-family: 'Playfair Display', serif;
        color: var(--secondary-color);
        text-align: center;
        margin-bottom: 30px;
    }

    h1 {
        font-size: 3.5em; 
        color: var(--accent-color); 
        padding-top: 20px;
        letter-spacing: 2px;
    }
    
    h2 {
        font-size: 2.2em;
        color: var(--secondary-color);
        margin-bottom: 15px;
    }

    /* Formulário (Texto Interno Escuro) */
    .stForm label, .stForm input, .stForm select, .stForm div:not(.stButton) {
        color: var(--text-color-dark) !important; 
    }

    /* Estilo da Tabela (Texto Interno Escuro) */
    .stDataFrame > div > div > div > div:nth-child(2) > div:nth-child(1) {
        font-weight: 700 !important; 
        color: var(--text-color-dark) !important; 
        background-color: #f0f0f0 !important; 
        border-bottom: 3px solid var(--accent-color) !important; 
    }
    .stDataFrame {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }

    /* Outros estilos omitidos para brevidade, mas devem ser mantidos no seu arquivo */

</style>
""", unsafe_allow_html=True)


# --- CORPO PRINCIPAL DO APLICATIVO ---

st.title('Lista de Presentes de Casamento\nAna & Roger')

# --- Imagem de Cabeçalho (Uso nativo) ---
try:
    st.image("ana1.jpg", use_container_width=True) 
except Exception:
    st.warning("Não foi possível carregar a imagem de cabeçalho (ana1.jpg).")

df_data = load_data() 

coluna_lista, coluna_form = st.columns([2,1]) 

# === Coluna da Lista de Presentes ===
with coluna_lista:
    st.header("🎉 Presentes Confirmados")
    
    df_ganhos = df_data[df_data['Status'] == 'Ganho']

    if df_ganhos.empty:
        st.info('Ainda não há presentes confirmados. Adicione um presente no formulário ao lado!')
    else:
        st.dataframe(
            df_ganhos[['Item', 'Categoria']],
            hide_index=True,
            use_container_width=True,
        )
    
    st.markdown("---")

    st.subheader("Nosso Momento Especial")
    col1, col2 = st.columns(2)
    try:
        with col1:
            st.image("ana2.jpg", use_container_width=True)
        with col2:
            st.image("ana3.jpg", use_container_width=True)
    except Exception:
        st.warning("Não foi possível carregar as imagens menores.")

    st.markdown("---")


# === Coluna do Formulário de Contribuição ===
with coluna_form:
    st.header('Adicione o seu presente à lista')

    with st.form('form_Presente', clear_on_submit=True):
        novo_item = st.text_input('Nome do Presente:', help='Exemplo: "Jogo de Panelas" ou "Vale-Presente"')

        nova_categoria = st.selectbox(
            'Categoria:',
            ['Eletrônicos', 'Eletrodomésticos', 'Utensílios Domésticos', 'Móveis', 'Decoração', 'Vale-Presente', 'Enxoval', 'Outros'],
            help='Selecione a categoria que melhor descreve o presente.'
        )

        submitted = st.form_submit_button('Confirmar Presente')

        if submitted:
            if novo_item:
                novo_id = str(uuid.uuid4())
                
                # Dados para salvar na planilha
                novo_presente_data = {
                    'ID': novo_id,
                    'Item': novo_item,
                    'Categoria': nova_categoria,
                    'Status': 'Ganho'
                }
                
                # Chama a nova função save_data
                if save_data(novo_presente_data):
                    st.success(f'Obrigado por adicionar "{novo_item}" à lista de presentes! 🎉')
                    st.balloons()
                    st.cache_data.clear() # Limpa o cache para forçar a leitura dos novos dados
                    st.rerun()
                # Se save_data falhou, a mensagem de erro já apareceu dentro dela.
                
            else:
                st.error('Por favor, insira o nome do presente antes de confirmar.')
