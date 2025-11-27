import streamlit as st
import pandas as pd
import uuid

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('lista_presentes.csv')
    except Exception:
        df = pd.DataFrame(columns=['ID','Item','Categoria','Status'])
    return df

def save_data(df):
    df.to_csv('lista_presentes.csv', index=False)

# --- CSS PERSONALIZADO (DESIGN E FONTES) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Playfair+Display:wght@700&display=swap');

    :root {
        --primary-color: #F7D71C; /* Dourado */
        --secondary-color: #000000; /* Preto */
        --accent-color: #E91E63; /* Rosa das fotos */
        --text-color: #333333;
        --bg-color: #F8F9FA;
    }

    body {
        font-family: 'Montserrat', sans-serif;
        color: var(--text-color);
        background-color: var(--bg-color);
    }

    h1, h2, h3, .st-emotion-cache-10trblm { 
        font-family: 'Playfair Display', serif;
        color: var(--secondary-color);
        text-align: center;
        margin-bottom: 30px;
    }

    h1 {
        font-size: 3.5em; 
        color: var(--accent-color); 
    }

    h2 {
        font-size: 2.2em;
        color: var(--secondary-color);
    }

    .stButton > button {
        background-color: var(--accent-color);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #C2185B; 
        transform: translateY(-2px);
    }

    .stTextInput > label, .stSelectbox > label {
        font-weight: 600;
        color: var(--text-color);
    }

    .stForm {
        background-color: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }

    .stAlert {
        border-radius: 8px;
    }

    /* Estilo para a imagem de cabeçalho */
    .header-image {
        width: 100%;
        max-height: 400px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 40px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    }

    .couple-images {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 40px;
        margin-bottom: 40px;
    }

    .couple-images img {
        width: 45%; 
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    }

</style>
""", unsafe_allow_html=True)

# --- CORPO PRINCIPAL DO APLICATIVO ---

st.title('Lista de Presentes de Casamento\nAna & Roger')

# --- Imagem de Cabeçalho (Retorna ao uso nativo do Streamlit) ---
try:
    #  O Streamlit carrega a imagem do diretório do script
    st.image("ana3.jpg", use_container_width=True) 
except Exception as e:
    st.warning("Não foi possível carregar a imagem de cabeçalho (ana3.jpg). Verifique se o arquivo está na pasta.")

df_data = load_data()

coluna_lista, coluna_form = st.columns([2, 1])

#=== Coluna da Lista de Presentes ===
with coluna_lista:
    st.header("🎉 Presentes Confirmados")

    df_ganhos = df_data[df_data['Status'] == 'Ganho'][['Item', 'Categoria']]

    if df_ganhos.empty:
        st.info('Ainda não há presentes confirmados. Adicione um presente no formulário ao lado!') 
    else:
        st.dataframe(
            df_ganhos[['Item', 'Categoria']],
            hide_index=True,
            use_container_width=True,
        )

    st.markdown("---")

  # --- Seção com as outras imagens do casal ---
    st.subheader('Nosso Momento Especial')

    # 🛑 Usa o layout de coluna nativo do Streamlit para as duas imagens
    col1, col2 = st.columns(2)
    try:
        with col1:
            st.image("ana2.jpg", use_container_width=True)
        with col2:
            st.image("ana1.jpg", use_container_width=True)
    except Exception as e:
        st.warning("Não foi possível carregar as imagens menores (ana2.jpg ou ana1.jpg).")

    st.markdown("---")

    # === Coluna do Formulário de Contribuição ===
with coluna_form:
    st.header("Adicione o seu Presente à Lista")

    with st.form('form_Presente', clear_on_submit=True):
        novo_item = st.text_input('Nome do Presente', help='Exemplo: "Jogo de Panelas" ou "Vale Presente"...')
        
        nova_categoria = st.selectbox(
            'Categoria',
            options=['Cozinha', 'Decoração', 'Eletrodomésticos', 'Utensílios Domésticos', 'Vale Presente', 'Enxoval', 'Outros'],
            help='Selecione a categoria que melhor descreve o presente.'
        )
        
        submited = st.form_submit_button('Confirmar Presente')

        if submited:
            if novo_item:
                novo_id = str(uuid.uuid4())  # Gera um ID único
                novo_presente = pd.DataFrame({
                    'ID': [novo_id],
                    'Item': [novo_item],
                    'Categoria': [nova_categoria],
                    'Status': ['Ganho']  # Novo presente começa como Pendente
                })
                df_atualizado = pd.concat([df_data, novo_presente], ignore_index=True)
                save_data(df_data)
                st.success(f'Presente "{novo_item}" adicionado com sucesso! Obrigado por contribuir! 🎉')
                st.balloons()
            else:
                st.error('Por favor, insira o nome do presente antes de confirmar.')
    

