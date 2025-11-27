import streamlit as st
import pandas as pd
import uuid
import gspread # NOVO: Importa a biblioteca para Google Sheets
from gspread.exceptions import WorksheetNotFound

# --- 🎯 CONFIGURAÇÃO E AUTENTICAÇÃO DO GOOGLE SHEETS ---

# Autentica e abre a planilha usando o st.secrets
# O nome 'gsheets' deve ser o mesmo usado em [gsheets] no secrets.toml
def get_gsheets_client():
    """Retorna o cliente gspread autenticado."""
    # O Streamlit usa automaticamente os segredos configurados em .streamlit/secrets.toml
    return gspread.service_account_info(info=st.secrets["gsheets"]["service_account"])

# Carrega o ID da planilha do secrets.toml
SHEET_ID = st.secrets["gsheets"]["sheet_id"]

# --- FUNÇÕES DE DADOS PARA PLANILHA GOOGLE ---

@st.cache_data 
def load_data(): 
    """Carrega os dados do Google Sheet."""
    try:
        # 1. Autentica e conecta ao cliente
        client = get_gsheets_client()
        
        # 2. Abre a planilha pelo ID
        spreadsheet = client.open_by_key(SHEET_ID)
        
        # 3. Abre a primeira aba (Worksheet)
        worksheet = spreadsheet.sheet1
        
        # 4. Lê todos os dados como DataFrame
        # get_all_records() ignora a primeira linha (cabeçalho) e retorna dicionários
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        # Se a planilha estiver vazia (exceto cabeçalho), cria o DF vazio com as colunas corretas
        if df.empty or 'ID' not in df.columns:
             st.error("A planilha Google está vazia ou as colunas não correspondem (ID, Item, Categoria, Status).")
             df = pd.DataFrame(columns=['ID','Item','Categoria','Status'])
        
        return df
    
    except WorksheetNotFound:
        st.error("Erro: A primeira aba da sua planilha Google não foi encontrada.")
        return pd.DataFrame(columns=['ID','Item','Categoria','Status'])
    except Exception as e:
        st.error(f"Erro de conexão com o Google Sheets. Verifique o secrets.toml. Erro: {e}")
        return pd.DataFrame(columns=['ID','Item','Categoria','Status'])


def save_data(df, novo_presente_data): 
    """Adiciona uma nova linha à planilha Google."""
    try:
        client = get_gsheets_client()
        spreadsheet = client.open_by_key(SHEET_ID)
        worksheet = spreadsheet.sheet1

        # Prepara a nova linha como uma lista de valores, na ordem das colunas
        nova_linha = [
            novo_presente_data['ID'],
            novo_presente_data['Item'],
            novo_presente_data['Categoria'],
            novo_presente_data['Status']
        ]

        # Adiciona a linha ao final da planilha
        worksheet.append_row(nova_linha)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados no Google Sheets. Erro: {e}")
        return False

# --- CONFIGURAÇÃO INICIAL E RESTO DO CÓDIGO ---

st.set_page_config(
    layout='wide',
    page_title='Lista de Presentes de Casamento | Ana & Roger',
    page_icon='🎁'
)

# --- CSS PERSONALIZADO (DESIGN POR CORES E TIPOGRAFIA) ---
# ... (Mantenha seu bloco st.markdown com o CSS) ...

# 🛑 IMPORTANTE: COLE SEU BLOCO st.markdown COM O CSS AQUI (mantido o código anterior para foco no Python)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Playfair+Display:wght@700&display=swap');

    :root {
        --primary-color: #F7D71C; 
        --secondary-color: #FFFFFF; 
        --accent-color: #E91E63; 
        --text-color-dark: #333333; 
        --text-color-light: #FFFFFF; 
        --bg-color: #36454F; 
    }
    /* Restante do seu CSS ... */
    
    [data-testid="stAppViewContainer"] { background-color: var(--bg-color) !important; }
    .st-emotion-cache-13l37u7, .stForm, .stDataFrame { background-color: #FFFFFF !important; }
    div.stText, div.stMarkdown { color: var(--text-color-light) !important; }
    /* ... (Mantenha todo o resto do CSS aqui para evitar erros) ... */
</style>
""", unsafe_allow_html=True)


# --- CORPO PRINCIPAL DO APLICATIVO ---

st.title('Lista de Presentes de Casamento\nAna & Roger')

# --- Imagens e Layout ---
df_data = load_data() # Carrega os dados da planilha

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
                if save_data(df_data, novo_presente_data):
                    st.success(f'Obrigado por adicionar "{novo_item}" à lista de presentes! 🎉')
                    st.balloons()
                    st.cache_data.clear() # Limpa o cache para forçar a leitura dos novos dados
                    st.rerun()
                # Se save_data falhou, a mensagem de erro já apareceu dentro dela.
                
            else:
                st.error('Por favor, insira o nome do presente antes de confirmar.')