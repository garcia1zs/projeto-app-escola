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

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

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

h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# FUNÇÕES
# ==================================

def contar_alunos():
    try:
        dados = (
            supabase
            .table("aluno")
            .select("*")
            .execute()
        )

        return len(dados.data or [])

    except Exception:
        return 0


def contar_professores():
    try:
        dados = (
            supabase
            .table("professor")
            .select("*")
            .execute()
        )

        return len(dados.data or [])

    except Exception:
        return 0


def contar_turmas():
    try:
        dados = (
            supabase
            .table("turma")
            .select("*")
            .execute()
        )

        return len(dados.data or [])

    except Exception:
        return 0


def buscar_alunos():
    try:
        resultado = (
            supabase
            .table("aluno")
            .select("*")
            .execute()
        )

        return resultado.data or []

    except Exception:
        return []


def buscar_pessoas():
    try:
        resultado = (
            supabase
            .table("pessoas")
            .select("*")
            .execute()
        )

        return resultado.data or []

    except Exception:
        return []


def buscar_professores():
    try:
        resultado = (
            supabase
            .table("professor")
            .select("*")
            .execute()
        )

        return resultado.data or []

    except Exception:
        return []


def buscar_turmas():
    try:
        resultado = (
            supabase
            .table("turma")
            .select("*")
            .order("nome")
            .execute()
        )

        return resultado.data or []

    except Exception:
        return []


def buscar_disciplinas():
    try:
        resultado = (
            supabase
            .table("disciplina")
            .select("*")
            .eq("ativo", True)
            .order("nome")
            .execute()
        )

        return resultado.data or []

    except Exception:
        return []


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
        "Listar Turmas",
        "Registrar Nota",
        "Listar Notas",
        "Registrar Frequência",
        "Listar Frequências"
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

    grafico = pd.DataFrame(
        {
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
        ]
    )

    st.subheader("Visão Geral")

    st.bar_chart(grafico)


# ==================================
# CADASTRAR ALUNO
# ==================================

elif menu == "Cadastrar Aluno":

    st.title("👨‍🎓 Cadastro de Aluno")

    with st.form("form_aluno"):

        col1, col2 = st.columns(2)

        with col1:

            nome = st.text_input("Nome")

            cpf = st.text_input("CPF")

            matricula = st.text_input(
                "Matrícula"
            )

        with col2:

            nascimento = st.text_input(
                "Nascimento (DD/MM/AAAA)"
            )

            endereco = st.text_input(
                "Endereço"
            )

        salvar = st.form_submit_button(
            "💾 Salvar Aluno"
        )

        if salvar:

            if not nome:
                st.warning("Digite o nome do aluno.")

            elif not matricula:
                st.warning("Digite a matrícula.")

            elif not nascimento:
                st.warning("Digite a data de nascimento.")

            else:

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
                        "Aluno cadastrado com sucesso! ✅"
                    )

                except Exception as e:

                    st.error(
                        "Erro ao cadastrar aluno."
                    )

                    st.code(
                        repr(e)
                    )


# ==================================
# CADASTRAR PROFESSOR
# ==================================

elif menu == "Cadastrar Professor":

    st.title("👨‍🏫 Cadastro de Professor")

    with st.form("form_professor"):

        col1, col2 = st.columns(2)

        with col1:

            nome = st.text_input(
                "Nome"
            )

            cpf = st.text_input(
                "CPF"
            )

            especialidade = st.text_input(
                "Especialidade"
            )

        with col2:

            nascimento = st.text_input(
                "Nascimento (DD/MM/AAAA)"
            )

            endereco = st.text_input(
                "Endereço"
            )

            salario = st.number_input(
                "Salário",
                min_value=0.0,
                step=100.0
            )

        salvar = st.form_submit_button(
            "💾 Salvar Professor"
        )

        if salvar:

            if not nome:
                st.warning("Digite o nome do professor.")

            elif not nascimento:
                st.warning("Digite a data de nascimento.")

            else:

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
                            "salario": float(salario)
                        })
                        .execute()
                    )

                    st.success(
                        "Professor cadastrado com sucesso! ✅"
                    )

                except Exception as e:

                    st.error(
                        "Erro ao cadastrar professor."
                    )

                    st.code(
                        repr(e)
                    )


# ==================================
# CADASTRAR TURMA
# ==================================

elif menu == "Cadastrar Turma":

    st.title("🏫 Cadastro de Turma")

    with st.form("form_turma"):

        nome = st.text_input(
            "Nome da Turma"
        )

        ano = st.number_input(
            "Ano Letivo",
            min_value=2020,
            max_value=2100,
            value=datetime.now().year,
            step=1
        )

        salvar = st.form_submit_button(
            "💾 Salvar Turma"
        )

        if salvar:

            if not nome:

                st.warning(
                    "Digite o nome da turma."
                )

            else:

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
                        "Turma criada com sucesso! ✅"
                    )

                except Exception as e:

                    st.error(
                        "Erro ao cadastrar turma."
                    )

                    st.code(
                        repr(e)
                    )


# ==================================
# LISTAR ALUNOS
# ==================================

elif menu == "Listar Alunos":

    st.title("📋 Lista de Alunos")

    try:

        alunos = buscar_alunos()

        pessoas = buscar_pessoas()

        pessoas_dict = {
            pessoa["id"]: pessoa
            for pessoa in pessoas
        }

        dados = []

        for aluno in alunos:

            pessoa = pessoas_dict.get(
                aluno.get("pessoa_id"),
                {}
            )

            dados.append({
                "ID": aluno.get(
                    "id"
                ),
                "Nome": pessoa.get(
                    "nome",
                    "—"
                ),
                "CPF": pessoa.get(
                    "cpf",
                    "—"
                ),
                "Nascimento": pessoa.get(
                    "nascimento",
                    "—"
                ),
                "Endereço": pessoa.get(
                    "endereco",
                    "—"
                ),
                "Matrícula": aluno.get(
                    "matricula",
                    "—"
                )
            })

        if dados:

            st.dataframe(
                pd.DataFrame(dados),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Nenhum aluno cadastrado."
            )

    except Exception as e:

        st.error(
            "Erro ao carregar alunos."
        )

        st.code(
            repr(e)
        )


# ==================================
# LISTAR PROFESSORES
# ==================================

elif menu == "Listar Professores":

    st.title("📋 Lista de Professores")

    try:

        professores = buscar_professores()

        pessoas = buscar_pessoas()

        pessoas_dict = {
            pessoa["id"]: pessoa
            for pessoa in pessoas
        }

        dados = []

        for professor in professores:

            pessoa = pessoas_dict.get(
                professor.get("pessoa_id"),
                {}
            )

            dados.append({
                "Nome": pessoa.get(
                    "nome",
                    "—"
                ),
                "CPF": pessoa.get(
                    "cpf",
                    "—"
                ),
                "Nascimento": pessoa.get(
                    "nascimento",
                    "—"
                ),
                "Endereço": pessoa.get(
                    "endereco",
                    "—"
                ),
                "Especialidade": professor.get(
                    "especialidade",
                    "—"
                ),
                "Salário": professor.get(
                    "salario",
                    0
                )
            })

        if dados:

            st.dataframe(
                pd.DataFrame(dados),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Nenhum professor cadastrado."
            )

    except Exception as e:

        st.error(
            "Erro ao carregar professores."
        )

        st.code(
            repr(e)
        )


# ==================================
# LISTAR TURMAS
# ==================================

elif menu == "Listar Turmas":

    st.title("📋 Lista de Turmas")

    try:

        turmas = buscar_turmas()

        if turmas:

            dados = []

            for turma in turmas:

                dados.append({
                    "ID": turma.get(
                        "id"
                    ),
                    "Turma": turma.get(
                        "nome",
                        "—"
                    ),
                    "Ano Letivo": turma.get(
                        "ano_letivo",
                        "—"
                    )
                })

            st.dataframe(
                pd.DataFrame(dados),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Nenhuma turma cadastrada."
            )

    except Exception as e:

        st.error(
            "Erro ao carregar turmas."
        )

        st.code(
            repr(e)
        )


# ==================================
# REGISTRAR NOTA
# ==================================

elif menu == "Registrar Nota":

    st.title("📝 Registrar Nota")

    alunos = buscar_alunos()

    pessoas = buscar_pessoas()

    disciplinas = buscar_disciplinas()

    pessoas_dict = {
        pessoa["id"]: pessoa
        for pessoa in pessoas
    }

    if not alunos:

        st.warning(
            "Nenhum aluno cadastrado."
        )

    elif not disciplinas:

        st.warning(
            "Nenhuma disciplina ativa cadastrada."
        )

    else:

        opcoes_alunos = {}

        for aluno in alunos:

            pessoa = pessoas_dict.get(
                aluno.get("pessoa_id"),
                {}
            )

            nome = pessoa.get(
                "nome",
                "Aluno sem nome"
            )

            matricula = aluno.get(
                "matricula",
                "Sem matrícula"
            )

            texto = (
                f"{matricula} — {nome}"
            )

            opcoes_alunos[texto] = aluno["id"]

        opcoes_disciplina = {}

        for disciplina in disciplinas:

            nome_disciplina = disciplina.get(
                "nome",
                "Sem nome"
            )

            opcoes_disciplina[
                nome_disciplina
            ] = nome_disciplina

        with st.form("form_nota"):

            aluno_escolhido = st.selectbox(
                "Aluno",
                list(
                    opcoes_alunos.keys()
                )
            )

            disciplina_escolhida = st.selectbox(
                "Disciplina",
                list(
                    opcoes_disciplina.keys()
                )
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                nota = st.number_input(
                    "Nota",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.1
                )

            with col2:

                bimestre = st.selectbox(
                    "Bimestre",
                    [
                        1,
                        2,
                        3,
                        4
                    ]
                )

            with col3:

                ano_letivo = st.number_input(
                    "Ano Letivo",
                    min_value=2020,
                    max_value=2100,
                    value=datetime.now().year,
                    step=1
                )

            salvar = st.form_submit_button(
                "💾 Salvar Nota"
            )

            if salvar:

                try:

                    aluno_id = (
                        opcoes_alunos[
                            aluno_escolhido
                        ]
                    )

                    (
                        supabase
                        .table("nota")
                        .insert({
                            "aluno_id": aluno_id,
                            "disciplina": disciplina_escolhida,
                            "nota": float(nota),
                            "bimestre": int(bimestre),
                            "ano_letivo": int(ano_letivo)
                        })
                        .execute()
                    )

                    st.success(
                        "Nota registrada com sucesso! ✅"
                    )

                except Exception as e:

                    st.error(
                        "Erro ao registrar nota."
                    )

                    st.code(
                        repr(e)
                    )


# ==================================
# LISTAR NOTAS
# ==================================

elif menu == "Listar Notas":

    st.title("📋 Notas dos Alunos")

    try:

        notas = (
            supabase
            .table("nota")
            .select("*")
            .order(
                "id",
                desc=True
            )
            .execute()
        )

        alunos = buscar_alunos()

        pessoas = buscar_pessoas()

        alunos_dict = {
            aluno["id"]: aluno
            for aluno in alunos
        }

        pessoas_dict = {
            pessoa["id"]: pessoa
            for pessoa in pessoas
        }

        dados = []

        for registro in notas.data or []:

            aluno = alunos_dict.get(
                registro.get(
                    "aluno_id"
                ),
                {}
            )

            pessoa = pessoas_dict.get(
                aluno.get(
                    "pessoa_id"
                ),
                {}
            )

            dados.append({
                "Aluno": pessoa.get(
                    "nome",
                    "—"
                ),
                "Matrícula": aluno.get(
                    "matricula",
                    "—"
                ),
                "Disciplina": registro.get(
                    "disciplina",
                    "—"
                ),
                "Nota": registro.get(
                    "nota",
                    0
                ),
                "Bimestre": registro.get(
                    "bimestre",
                    "—"
                ),
                "Ano Letivo": registro.get(
                    "ano_letivo",
                    "—"
                )
            })

        if dados:

            df_notas = pd.DataFrame(
                dados
            )

            st.dataframe(
                df_notas,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Nenhuma nota cadastrada."
            )

    except Exception as e:

        st.error(
            "Erro ao carregar notas."
        )

        st.code(
            repr(e)
        )


# ==================================
# REGISTRAR FREQUÊNCIA
# ==================================

elif menu == "Registrar Frequência":

    st.title(
        "📅 Registrar Frequência"
    )

    alunos = buscar_alunos()

    pessoas = buscar_pessoas()

    turmas = buscar_turmas()

    pessoas_dict = {
        pessoa["id"]: pessoa
        for pessoa in pessoas
    }

    if not alunos:

        st.warning(
            "Nenhum aluno cadastrado."
        )

    elif not turmas:

        st.warning(
            "Nenhuma turma cadastrada."
        )

    else:

        opcoes_alunos = {}

        for aluno in alunos:

            pessoa = pessoas_dict.get(
                aluno.get(
                    "pessoa_id"
                ),
                {}
            )

            nome = pessoa.get(
                "nome",
                "Aluno sem nome"
            )

            matricula = aluno.get(
                "matricula",
                "Sem matrícula"
            )

            texto = (
                f"{matricula} — {nome}"
            )

            opcoes_alunos[
                texto
            ] = aluno["id"]

        opcoes_turmas = {}

        for turma in turmas:

            nome_turma = turma.get(
                "nome",
                "Sem nome"
            )

            ano = turma.get(
                "ano_letivo",
                "—"
            )

            texto_turma = (
                f"{nome_turma} - {ano}"
            )

            opcoes_turmas[
                texto_turma
            ] = turma["id"]

        with st.form(
            "form_frequencia"
        ):

            aluno_escolhido = st.selectbox(
                "Aluno",
                list(
                    opcoes_alunos.keys()
                )
            )

            turma_escolhida = st.selectbox(
                "Turma",
                list(
                    opcoes_turmas.keys()
                )
            )

            data_frequencia = st.date_input(
                "Data da Aula"
            )

            presente = st.radio(
                "Presença",
                [
                    "Presente",
                    "Ausente"
                ],
                horizontal=True
            )

            salvar = st.form_submit_button(
                "💾 Registrar Frequência"
            )

            if salvar:

                try:

                    aluno_id = (
                        opcoes_alunos[
                            aluno_escolhido
                        ]
                    )

                    turma_id = (
                        opcoes_turmas[
                            turma_escolhida
                        ]
                    )

                    (
                        supabase
                        .table("frequencia")
                        .insert({
                            "aluno_id": aluno_id,
                            "turma_id": turma_id,
                            "data": data_frequencia.isoformat(),
                            "presente": (
                                presente == "Presente"
                            )
                        })
                        .execute()
                    )

                    st.success(
                        "Frequência registrada com sucesso! ✅"
                    )

                except Exception as e:

                    st.error(
                        "Erro ao registrar frequência."
                    )

                    st.code(
                        repr(e)
                    )


# ==================================
# LISTAR FREQUÊNCIAS
# ==================================

elif menu == "Listar Frequências":

    st.title(
        "📋 Frequência dos Alunos"
    )

    try:

        frequencias = (
            supabase
            .table("frequencia")
            .select("*")
            .order(
                "data",
                desc=True
            )
            .execute()
        )

        alunos = buscar_alunos()

        pessoas = buscar_pessoas()

        turmas = buscar_turmas()

        alunos_dict = {
            aluno["id"]: aluno
            for aluno in alunos
        }

        pessoas_dict = {
            pessoa["id"]: pessoa
            for pessoa in pessoas
        }

        turmas_dict = {
            turma["id"]: turma
            for turma in turmas
        }

        dados = []

        for frequencia in frequencias.data or []:

            aluno = alunos_dict.get(
                frequencia.get(
                    "aluno_id"
                ),
                {}
            )

            pessoa = pessoas_dict.get(
                aluno.get(
                    "pessoa_id"
                ),
                {}
            )

            turma = turmas_dict.get(
                frequencia.get(
                    "turma_id"
                ),
                {}
            )

            presente = frequencia.get(
                "presente"
            )

            dados.append({
                "Aluno": pessoa.get(
                    "nome",
                    "—"
                ),
                "Matrícula": aluno.get(
                    "matricula",
                    "—"
                ),
                "Turma": turma.get(
                    "nome",
                    "—"
                ),
                "Ano": turma.get(
                    "ano_letivo",
                    "—"
                ),
                "Data": frequencia.get(
                    "data",
                    "—"
                ),
                "Presença": (
                    "✅ Presente"
                    if presente
                    else "❌ Ausente"
                )
            })

        if dados:

            df_frequencias = pd.DataFrame(
                dados
            )

            st.dataframe(
                df_frequencias,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Nenhuma frequência cadastrada."
            )

    except Exception as e:

        st.error(
            "Erro ao carregar frequências."
        )

        st.code(
            repr(e)
        )