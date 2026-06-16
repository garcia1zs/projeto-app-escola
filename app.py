import streamlit as st
from supabase import create_client
from datetime import datetime
import pandas as pd

# ==================================
# CONFIGURAÇÃO
# ==================================

st.set_page_config(
    page_title="Sistema Escolar",
    page_icon="📚",
    layout="wide"
)

SUPABASE_URL = "https://tsgyaxeveplqgtyrlxiv.supabase.co"
SUPABASE_KEY = "sb_publishable_8uJUbwg6gyn_CX0o1oub5Q_HJUwbPB8"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==================================
# CSS PERSONALIZADO
# ==================================

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.metric-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 12px;
}

h1,h2,h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==================================
# FUNÇÕES
# ==================================

def contar_alunos():
    try:
        dados = supabase.table("aluno").select("*").execute()
        return len(dados.data)
    except:
        return 0

def contar_professores():
    try:
        dados = supabase.table("professor").select("*").execute()
        return len(dados.data)
    except:
        return 0

def contar_turmas():
    try:
        dados = supabase.table("turma").select("*").execute()
        return len(dados.data)
    except:
        return 0

# ==================================
# SIDEBAR
# ==================================

st.sidebar.title("📚 Sistema Escolar")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Cadastrar Aluno",
        "Cadastrar Professor",
        "Cadastrar Turma",
        "Listar Alunos",
        "Listar Professores",
        "Listar Turmas"
    ]
)

# ==================================
# DASHBOARD
# ==================================

if menu == "Dashboard":

    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Alunos",
            contar_alunos()
        )

    with col2:
        st.metric(
            "👨‍🏫 Professores",
            contar_professores()
        )

    with col3:
        st.metric(
            "🏫 Turmas",
            contar_turmas()
        )

    grafico = pd.DataFrame({
        "Quantidade": [
            contar_alunos(),
            contar_professores(),
            contar_turmas()
        ]
    },
    index=[
        "Alunos",
        "Professores",
        "Turmas"
    ])

    st.subheader("Visão Geral")

    st.bar_chart(grafico)

# ==================================
# CADASTRO ALUNO
# ==================================

elif menu == "Cadastrar Aluno":

    st.title("👨‍🎓 Cadastro de Aluno")

    with st.form("form_aluno"):

        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome")
            cpf = st.text_input("CPF")
            matricula = st.text_input("Matrícula")

        with col2:
            nascimento = st.text_input(
                "Nascimento (DD/MM/AAAA)"
            )
            endereco = st.text_input("Endereço")

        salvar = st.form_submit_button(
            "Salvar Aluno"
        )

        if salvar:

            try:

                nascimento_formatado = (
                    datetime.strptime(
                        nascimento,
                        "%d/%m/%Y"
                    )
                    .strftime("%Y-%m-%d")
                )

                pessoa = (
                    supabase
                    .table("pessoas")
                    .insert({
                        "nome": nome,
                        "cpf": cpf,
                        "nascimento": nascimento_formatado,
                        "endereco": endereco
                    })
                    .execute()
                )

                pessoa_id = pessoa.data[0]["id"]

                (
                    supabase
                    .table("aluno")
                    .insert({
                        "pessoa_id": pessoa_id,
                        "matricula": matricula
                    })
                    .execute()
                )

                st.success(
                    "Aluno cadastrado com sucesso!"
                )

            except Exception as e:
                st.error(str(e))

# ==================================
# CADASTRO PROFESSOR
# ==================================

elif menu == "Cadastrar Professor":

    st.title("👨‍🏫 Cadastro de Professor")

    with st.form("form_professor"):

        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome")
            cpf = st.text_input("CPF")
            especialidade = st.text_input(
                "Especialidade"
            )

        with col2:
            nascimento = st.text_input(
                "Nascimento"
            )
            endereco = st.text_input(
                "Endereço"
            )
            salario = st.number_input(
                "Salário",
                min_value=0.0
            )

        salvar = st.form_submit_button(
            "Salvar Professor"
        )

        if salvar:

            try:

                nascimento_formatado = (
                    datetime.strptime(
                        nascimento,
                        "%d/%m/%Y"
                    )
                    .strftime("%Y-%m-%d")
                )

                pessoa = (
                    supabase
                    .table("pessoas")
                    .insert({
                        "nome": nome,
                        "cpf": cpf,
                        "nascimento": nascimento_formatado,
                        "endereco": endereco
                    })
                    .execute()
                )

                pessoa_id = pessoa.data[0]["id"]

                (
                    supabase
                    .table("professor")
                    .insert({
                        "pessoa_id": pessoa_id,
                        "especialidade": especialidade,
                        "salario": salario
                    })
                    .execute()
                )

                st.success(
                    "Professor cadastrado!"
                )

            except Exception as e:
                st.error(str(e))

# ==================================
# CADASTRO TURMA
# ==================================

elif menu == "Cadastrar Turma":

    st.title("🏫 Cadastro de Turma")

    nome = st.text_input(
        "Nome da Turma"
    )

    ano = st.number_input(
        "Ano Letivo",
        min_value=2020,
        max_value=2100,
        step=1
    )

    if st.button("Salvar Turma"):

        try:

            (
                supabase
                .table("turma")
                .insert({
                    "nome": nome,
                    "ano_letivo": int(ano)
                })
                .execute()
            )

            st.success(
                "Turma criada!"
            )

        except Exception as e:
            st.error(str(e))

# ==================================
# LISTAR ALUNOS
# ==================================

elif menu == "Listar Alunos":

    st.title("📋 Lista de Alunos")

    alunos = (
        supabase
        .table("aluno")
        .select("*")
        .execute()
    )

    dados = []

    for aluno in alunos.data:

        pessoa = (
            supabase
            .table("pessoas")
            .select("*")
            .eq(
                "id",
                aluno["pessoa_id"]
            )
            .execute()
        )

        if pessoa.data:

            dados.append({
                "Nome": pessoa.data[0]["nome"],
                "CPF": pessoa.data[0]["cpf"],
                "Matrícula": aluno["matricula"]
            })

    st.dataframe(
        pd.DataFrame(dados),
        use_container_width=True
    )

# ==================================
# LISTAR PROFESSORES
# ==================================

elif menu == "Listar Professores":

    st.title("📋 Lista de Professores")

    professores = (
        supabase
        .table("professor")
        .select("*")
        .execute()
    )

    dados = []

    for professor in professores.data:

        pessoa = (
            supabase
            .table("pessoas")
            .select("*")
            .eq(
                "id",
                professor["pessoa_id"]
            )
            .execute()
        )

        if pessoa.data:

            dados.append({
                "Nome": pessoa.data[0]["nome"],
                "Especialidade":
                    professor["especialidade"],
                "Salário":
                    professor["salario"]
            })

    st.dataframe(
        pd.DataFrame(dados),
        use_container_width=True
    )

# ==================================
# LISTAR TURMAS
# ==================================

elif menu == "Listar Turmas":

    st.title("📋 Lista de Turmas")

    turmas = (
        supabase
        .table("turma")
        .select("*")
        .execute()
    )

    st.dataframe(
        pd.DataFrame(turmas.data),
        use_container_width=True
    )