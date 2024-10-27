import streamlit as st
import requests

# Configuração do tema
st.set_page_config(page_title="Consulta de Endereço", layout="wide")

# Adicionando estilo para a página
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f8ff;  /* Cor de fundo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título e logo
col1, col2, col3 = st.columns([1, 4, 1])  # Cria colunas para centralizar
with col2:
    st.image("busca.png", width=300)  # Ajuste a largura aqui
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>Consulta de Endereço</h1>", unsafe_allow_html=True)

# Opções de busca
option = st.selectbox("Escolha o método de busca:", ["Buscar pelo CEP", "Buscar pelo nome da rua"])

# Busca pelo CEP
if option == "Buscar pelo CEP":
    cep = st.text_input("Digite o CEP (formato: 00000-000):")
    if st.button("Buscar Endereço"):
        if cep:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url)

            if response.status_code == 200:
                endereco = response.json()
                if "erro" not in endereco:
                    st.success("Endereço encontrado:")
                    st.write(f"**Logradouro:** {endereco['logradouro']}")
                    st.write(f"**Bairro:** {endereco['bairro']}")
                    st.write(f"**Cidade:** {endereco['localidade']}")
                    st.write(f"**Estado:** {endereco['uf']}")
                else:
                    st.error("CEP não encontrado.")
            else:
                st.error("Erro ao buscar o endereço.")
        else:
            st.warning("Por favor, insira um CEP válido.")

# Busca pelo logradouro
else:
    nome_rua = st.text_input("Digite o nome da rua:")
    if st.button("Buscar Endereço"):
        if nome_rua:
            # Usando a API Nominatim do OpenStreetMap
            url = f"https://nominatim.openstreetmap.org/search?street={nome_rua}&format=json&addressdetails=1"
            headers = {'User-Agent': 'MeuApp/1.0'}  # Defina seu User-Agent aqui
            
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                endereco = response.json()
                if endereco:
                    # Exibindo todas as opções
                    st.success("Endereços encontrados:")
                    opcoes = []
                    for item in endereco:
                        opcoes.append(item['display_name'])

                    selected_option = st.selectbox("Selecione um endereço:", opcoes)

                    # Exibir detalhes do endereço selecionado
                    for item in endereco:
                        if item['display_name'] == selected_option:
                            cidade = item['address'].get('city', '') or item['address'].get('town', '') or item['address'].get('village', '')
                            estado = item['address'].get('state', '')
                            pais = item['address'].get('country', '')
                            cep = item['address'].get('postcode', 'Não disponível')

                            st.write(f"**Logradouro:** {item['display_name']}")
                            st.write(f"**CEP:** {cep}")
                            st.write(f"**Cidade:** {cidade}")
                            st.write(f"**Estado:** {estado}")
                            st.write(f"**País:** {pais}")
                else:
                    st.error("Nenhum endereço encontrado para essa rua.")
            else:
                st.error(f"Erro ao buscar o endereço. Status Code: {response.status_code}")  # Mostrar código de status
                st.error(response.text)  # Mostrar texto de erro da resposta
        else:
            st.warning("Por favor, insira o nome da rua.")
