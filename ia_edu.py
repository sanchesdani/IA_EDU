import streamlit as st
import random
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações da página
st.set_page_config(
    page_title="IA na Educação - Vieses",
    page_icon="🧠",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main { background-color: #f5f9fc; }
    .title { 
        color: #2c3e50; 
        text-align: center; 
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    .header {
        color: #2980b9;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .stButton>button {
        background-color: #bd3d3f;
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #674448;
        transform: scale(1.05);
    }
    .highlight {
        background-color: #efd7cf;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #deae9f;
        margin: 15px 0;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    .tab-content {
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Dados de exemplos de vieses
exemplos_vieses = {
    "Gênero": {
        "exemplo": "IA associando profissões STEM a homens e cuidados a mulheres",
        "impacto": "Pode influenciar as escolhas profissionais dos alunos",
        "atividade": "Analisar imagens de busca por 'cientista' e discutir a representação",
        "solucao": "Balancear conjuntos de dados e incluir exemplos diversos"
    },
    "Raça/Etnia": {
        "exemplo": "Reconhecimento facial com menor precisão para peles escuras",
        "impacto": "Pode levar a identificações equivocadas em sistemas escolares",
        "atividade": "Testar diferentes filtros de fotos em diversos tons de pele",
        "solucao": "Diversidade nos dados de treinamento e times de desenvolvimento"
    },
    "Cultural": {
        "exemplo": "Chatbots que não entendem expressões regionais ou gírias",
        "impacto": "Desvalorização de variações linguísticas válidas",
        "atividade": "Comparar respostas do chatbot a perguntas em diferentes dialetos",
        "solucao": "Incluir diversidade linguística nos dados de treinamento"
    },
    "Socioeconômico": {
        "exemplo": "Sistemas de recomendação que sugerem menos oportunidades para alunos de escolas públicas",
        "impacto": "Reprodução de desigualdades estruturais",
        "atividade": "Mapear oportunidades sugeridas para diferentes perfis de alunos",
        "solucao": "Auditoria regular dos algoritmos e inclusão de contextos diversos"
    }
}

# Dados para simulação de viés
def gerar_dados_viés():
    np.random.seed(42)
    dados = pd.DataFrame({
        'Gênero': np.random.choice(['Masculino', 'Feminino', 'Não-binário'], 300, p=[0.45, 0.45, 0.1]),
        'Raça': np.random.choice(['Branca', 'Preta', 'Parda', 'Amarela', 'Indígena'], 300, p=[0.45, 0.25, 0.2, 0.05, 0.05]),
        'Nível Socioeconômico': np.random.choice(['Alto', 'Médio', 'Baixo'], 300, p=[0.2, 0.5, 0.3]),
        'Nota Recomendada': np.random.normal(7, 1.5, 300),
        'Nota Real': np.random.normal(7, 1.5, 300)
    })
    
    # Adicionar vieses artificiais para demonstração
    dados.loc[dados['Gênero'] == 'Feminino', 'Nota Recomendada'] *= 0.95
    dados.loc[dados['Gênero'] == 'Não-binário', 'Nota Recomendada'] *= 0.90
    dados.loc[dados['Raça'].isin(['Preta', 'Parda']), 'Nota Recomendada'] *= 0.93
    dados.loc[dados['Nível Socioeconômico'] == 'Baixo', 'Nota Recomendada'] *= 0.92
    
    return dados

# Sistema de planos de aula na sessão
if 'planos_aula' not in st.session_state:
    st.session_state.planos_aula = []

def salvar_plano(plano):
    plano['id'] = len(st.session_state.planos_aula) + 1
    plano['data'] = str(datetime.now())
    st.session_state.planos_aula.append(plano)
    st.success("Plano de aula sobre vieses salvo com sucesso!")

# Barra lateral
with st.sidebar:
    st.title("🧠 IA na Educação")
    st.markdown("### Menu Principal")
    pagina = st.radio("Navegação", 
                     ["Início", 
                      "O que são Vieses?", 
                      "Casos Reais", 
                      "Simulador de Vieses", 
                      "Planos de Aula", 
                      "Recursos"])
    
    st.markdown("---")
    st.markdown("## Plataforma voltada para a identificação e discussão de vieses em IA")
    st.markdown("""
    #### Autora: Danielle Sanches  
    <a href="https://www.linkedin.com/in/danielle-sanches-de-almeida-2a225a107/" target="_blank">LinkedIn</a> |
    <a href="http://lattes.cnpq.br/1290893382232095" target="_blank">Lattes</a>
    """, unsafe_allow_html=True)
    st.markdown("""
    #### Como citar a plataforma:
    Identificando Vieses em IA. Plataforma de Inteligência Artificial Aplicada à Educação Básica. Versão 1.0, 2023. Disponível em: https://ia-para-educadores.streamlit.app. Acesso em: 16 mai. 2025.""")

# Páginas principais
if pagina == "Início":
    st.title("Identificando Vieses em IA")
    st.markdown("""
    <div class="highlight">
    <b>Vieses em IA</b> são tendências indesejadas que sistemas de inteligência artificial podem aprender com dados humanos, 
    reforçando estereótipos e preconceitos. Esta ferramenta ajuda educadores a entender e ensinar sobre esse tema crucial.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>📚 Para Professores</h3>
            <p>Recursos para identificar vieses em ferramentas educacionais que você já usa</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>👩‍🏫 Planos de Aula</h3>
            <p>Atividades prontas para discutir ética em IA com seus alunos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>🔍 Casos Reais</h3>
            <p>Exemplos concretos de como vieses aparecem na educação</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Como usar esta ferramenta?")
    st.markdown("""
    1. Explore a seção **"O que são Vieses?"** para entender os conceitos básicos
    2. Analise **Casos Reais** de vieses em sistemas educacionais
    3. Experimente o **Simulador de Vieses** com seus alunos
    4. Adapte nossos **Planos de Aula** para sua realidade
    5. Compartilhe seus achados com outros educadores
    """)

elif pagina == "O que são Vieses?":
    st.title("O que são Vieses em Inteligência Artificial?")
    
    st.markdown("""
    <div class="highlight">
    <b>Definição:</b> Vieses em IA são distorções sistemáticas nos sistemas de inteligência artificial que podem levar a 
    decisões injustas ou discriminatórias, muitas vezes refletindo preconceitos presentes nos dados de treinamento ou no 
    design dos algoritmos.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Como os vieses surgem na IA?")
    
    tab1, tab2, tab3 = st.tabs(["Fontes de Vieses", "Ciclo do Viés", "Por que importa na Educação?"])
    
    with tab1:
        st.markdown("""
        #### Principais fontes de vieses:
        
        - **Dados de treinamento**: 
          - Sub-representação de certos grupos
          - Dados históricos que refletem desigualdades
          - Amostras não diversificadas
        
        - **Design do sistema**:
          - Premissas equivocadas dos desenvolvedores
          - Métricas de desempenho inadequadas
          - Falta de diversidade nas equipes
        
        - **Implementação**:
          - Uso em contextos diferentes do pretendido
          - Interpretação equivocada dos resultados
          - Falta de acompanhamento contínuo
        """)
    with tab2:
       st.markdown("""#### Os vieses em sistemas de IA se perpetuam através de um ciclo vicioso. Entenda cada etapa:""")
       st.markdown("""    """)
       st.markdown("""    """)
       st.markdown("""    """)

 # Criando um layout em etapas
       col1, col2, col3, col4, col5 = st.columns(5)

       with col1:
          st.markdown("""
          <div class="card">
              <h3>📊 Dados Enviesados</h3>
              <p>Dados com sub-representação de grupos ou padrões históricos discriminatórios</p>
          </div>
          """, unsafe_allow_html=True)

       with col2:
          st.markdown("""
          <div class="card">
              <h3>🤖 Modelo Distorcido</h3>
              <p>O algoritmo aprende e amplifica os padrões enviesados presentes nos dados</p>
          </div>
          """, unsafe_allow_html=True)

       with col3:
          st.markdown("""
          <div class="card">
              <h3>⚖️ Decisões Tendenciosas</h3>
              <p>O sistema produz resultados que favorecem certos grupos em detrimento de outros</p>
          </div>
          """, unsafe_allow_html=True)

       with col4:
          st.markdown("""
          <div class="card">
              <h3>🔍 Reforço de Desigualdades</h3>
              <p>As decisões enviesadas afetam oportunidades e perpetuam estereótipos</p>
          </div>
          """, unsafe_allow_html=True)

       with col5:
          st.markdown("""
          <div class="card">
              <h3>📥 Novos Dados Contaminados</h3>
              <p>Os resultados do sistema são coletados como novos dados, reiniciando o ciclo</p>
          </div>
          """, unsafe_allow_html=True)
 
    with tab3:
        st.markdown("""
        #### Impacto na Educação:
        
        - Ferramentas educacionais com IA estão cada vez mais presentes nas escolas
        - Alunos expostos a sistemas enviesados podem internalizar estereótipos
        - Professores precisam de alfabetização crítica sobre tecnologia
        - Oportunidade para discutir ética tecnológica com os alunos
        
        > "Ensinar sobre vieses em IA desenvolve pensamento crítico e cidadania digital"
        """)

elif pagina == "Casos Reais":
    st.title("Casos Reais de Vieses em IA na Educação")
    
    st.markdown("""
    ### Exemplos documentados de como vieses aparecem em contextos educacionais
    """)
    
    for categoria, dados in exemplos_vieses.items():
        with st.expander(f"🔍 Viés de {categoria}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                **Exemplo concreto**:  
                {dados['exemplo']}
                
                **Impacto na educação**:  
                {dados['impacto']}
                """)
            
            with col2:
                st.markdown(f"""
                **Atividade para sala de aula**:  
                - {dados['atividade']}
                
                **Como mitigar**:  
                - {dados['solucao']}
                """)
    
    st.markdown("---")
    st.markdown("### Relato de Professores")
    
    relatos = [
        "Sistema de correção automática penalizava expressões regionais dos alunos",
        "Plataforma de recomendação de cursos sugeria humanas para meninas e exatas para meninos",
        "Software de gestão de comportamento marcava mais alunos negros como 'problemáticos'"
    ]
    
    st.write("📢 " + random.choice(relatos))
    st.button("Compartilhe seu relato")

elif pagina == "Simulador de Vieses":
    st.title("Simulador de Vieses em Sistemas Educacionais")
    
    st.markdown("""
    ### Experimente como vieses podem aparecer em dados educacionais
    """)
    
    dados = gerar_dados_viés()
    
    tab1, tab2, tab3 = st.tabs(["Visualização", "Análise", "Sugestões Pedagógicas"])
    
    with tab1:
        st.markdown("#### Dados de Notas Recomendadas vs. Reais")
        st.write("Estes dados simulam um sistema de IA que recomenda notas para alunos:")
        st.dataframe(dados.sample(10))
        
        opcao_analise = st.selectbox("Visualizar distribuição por:", 
                                    ['Gênero', 'Raça', 'Nível Socioeconômico'])
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(data=dados, x=opcao_analise, y='Nota Recomendada', ax=ax)
        ax.set_title(f"Distribuição das Notas Recomendadas por {opcao_analise}")
        st.pyplot(fig)
    
    with tab2:
        st.markdown("#### Identificando Vieses")
        
        st.markdown("""
        Analise as diferenças entre grupos:
        - Há grupos com notas recomendadas sistematicamente menores?
        - Como isso se compara com as notas reais?
        """)
        
        grupo1 = st.selectbox("Comparar grupo 1:", dados[opcao_analise].unique())
        grupo2 = st.selectbox("Comparar grupo 2:", dados[opcao_analise].unique())
        
        if grupo1 and grupo2:
            media_grupo1 = dados[dados[opcao_analise] == grupo1]['Nota Recomendada'].mean()
            media_grupo2 = dados[dados[opcao_analise] == grupo2]['Nota Recomendada'].mean()
            
            st.metric(f"Média {grupo1}", round(media_grupo1, 2))
            st.metric(f"Média {grupo2}", round(media_grupo2, 2))
            
            diferenca = abs(media_grupo1 - media_grupo2)
            if diferenca > 0.5:
                st.warning(f"Diferença significativa encontrada: {round(diferenca, 2)} pontos")
                st.markdown("Isso pode indicar um possível viés no sistema!")
    
    with tab3:
        st.markdown("#### Como usar esta simulação em aula")
        
        st.markdown("""
        1. **Introdução conceitual**: Explique o que são vieses em IA
        2. **Análise dos dados**: Peça aos alunos para identificarem padrões
        3. **Discussão**: Como esses vieses poderiam afetar os alunos?
        4. **Solução criativa**: Que mudanças fariam no sistema?
        
        **Perguntas para reflexão**:
        - Por que esses vieses podem surgir?
        - Que consequências isso teria na vida real?
        - Como podemos criar tecnologia mais justa?
        """)

elif pagina == "Planos de Aula":
    st.title("Planos de Aula sobre Vieses em IA")
    
    tab1, tab2 = st.tabs(["Criar Novo Plano", "Meus Planos Salvos"])
    
    with tab1:
        st.markdown("### Desenvolva sua aula sobre vieses em IA")
        
        with st.form("plano_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nivel_ensino = st.selectbox("Nível de Ensino*", 
                                           ["Fundamental I", "Fundamental II", "Ensino Médio"])
                duracao = st.slider("Duração (minutos)*", 30, 120, 60)
                tema = st.text_input("Tema da Aula*", placeholder="Ex: Reconhecimento facial e vieses")
            
            with col2:
                objetivos = st.text_area("Objetivos de Aprendizagem*")
                recursos = st.text_area("Recursos Necessários")
                conecta_curriculo = st.multiselect("Conecta com:", 
                                                 ["Língua Portuguesa", "Matemática", 
                                                  "Ciências", "História", "Geografia"])
            
            if st.form_submit_button("Gerar Plano de Aula"):
                if tema and objetivos:
                    plano = {
                        "nivel": nivel_ensino,
                        "tema": tema,
                        "objetivos": objetivos,
                        "duracao": duracao,
                        "recursos": recursos if recursos else "Computador, projetor, planilhas impressas",
                        "conteudo": f"""
                        ## Plano de Aula: {tema}
                        
                        **Nível**: {nivel_ensino}  
                        **Duração**: {duracao} minutos  
                        **Áreas conectadas**: {', '.join(conecta_curriculo) if conecta_curriculo else 'Interdisciplinar'}
                        
                        ### Objetivos
                        {objetivos}
                        
                        ### Desenvolvimento
                        
                        1. **Introdução (15 min)**
                           - Vídeo curto sobre vieses em IA
                           - Discussão inicial: "O que é justiça algorítmica?"
                        
                        2. **Atividade Prática ({duracao-35} min)**
                           - Análise de {random.choice([
                               "casos reais",
                               "dados simulados",
                               "ferramentas que usam"
                           ])}
                           - {random.choice([
                               "Produção de cartazes",
                               "Debate estruturado",
                               "Criação de propostas"
                           ])}
                        
                        3. **Conclusão (20 min)**
                           - Síntese dos aprendizados
                           - Reflexão: "Como podemos ser usuários críticos de IA?"
                        
                        **Recursos**: {recursos if recursos else "Materiais básicos"}
                        """
                    }
                    salvar_plano(plano)
                    st.markdown(plano["conteudo"])
                else:
                    st.warning("Preencha os campos obrigatórios (*)")
    
    with tab2:
        st.markdown("### Planos Salvos")
        
        if st.session_state.planos_aula:
            for i, plano in enumerate(st.session_state.planos_aula, 1):
                with st.expander(f"Aula {i}: {plano['tema']} ({plano['nivel']})"):
                    st.markdown(plano['conteudo'])
                    if st.button(f"Remover Plano {i}"):
                        st.session_state.planos_aula.pop(i-1)
                        st.rerun()
        else:
            st.info("Nenhum plano salvo ainda. Crie seu primeiro plano!")

elif pagina == "Recursos":
    st.title("Recursos para Educadores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Materiais Didáticos
        
        📚 [Guia de Ética em IA para Escolas](https://unesdoc.unesco.org)  
        🎥 [Série de vídeos "IA Justa"](https://www.youtube.com)  
        📝 [Planos de aula prontos sobre tecnologia](https://code.org)  
        🧩 [Atividades práticas para alunos](https://csunplugged.org)
        
        ### Ferramentas de Análise
        
        🔍 [Teste de vieses em conjuntos de dados](https://aif360.mybluemix.net)  
        📊 [Tutoriais de análise de dados para educadores](https://www.kaggle.com)  
        🤖 [Simulador de decisões algorítmicas](https://algorithmwatch.org)
        """)
    
    with col2:
        st.markdown("""
        ### Formação Continuada
        
        🎓 [Curso gratuito "IA para Educadores"](https://www.coursera.org)  
        📅 [Eventos sobre tecnologia e educação](https://www.example.com/eventos)  
        👩‍🏫 [Comunidade de professores de tecnologia](https://www.example.com/comunidade)
        
        ### Pesquisas e Referências
        
        📄 [Relatório "Vieses em Sistemas Educacionais"](https://www.example.com/relatorio)  
        📖 [Livro "Algoritmos de Destruição em Massa"](https://www.example.com/livro)  
        🎧 [Podcast "Tecnologia com Ética"](https://www.example.com/podcast)
        """)
    
        
# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 3px;">
    <p>© 2025 Plataforma para Identificação de Vieses em Dados</p>
    <p>Plataforma Desenvolvida por educadores para educadores</p>
<p style="font-size: small;">Versão 1.0 | Atualizado em Maio 2025</p>
</div>
""", unsafe_allow_html=True)