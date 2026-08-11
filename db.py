
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )

supabase = get_supabase()

@st.cache_data(ttl=30)
def get_pessoas():
    return supabase.table("pessoas").select("*").order("nome").execute().data or []

@st.cache_data(ttl=30)
def get_alunos():
    return supabase.table("aluno").select(
        "id, pessoa_id, matricula, pessoas!inner(nome, cpf, nascimento, endereco)"
    ).order("matricula").execute().data or []

@st.cache_data(ttl=30)
def get_professores():
    return supabase.table("professor").select(
        "id, pessoa_id, especialidade, salario, pessoas!inner(nome, cpf, nascimento, endereco)"
    ).order("id").execute().data or []

@st.cache_data(ttl=30)
def get_turmas():
    return supabase.table("turma").select("*").order("ano_letivo", desc=True).order("nome").execute().data or []

@st.cache_data(ttl=30)
def get_matriculas():
    return supabase.table("matricula").select("*").order("id", desc=True).execute().data or []

@st.cache_data(ttl=30)
def get_notas():
    return supabase.table("nota").select("*").order("id", desc=True).execute().data or []

@st.cache_data(ttl=30)
def get_frequencias():
    return supabase.table("frequencia").select("*").order("data", desc=True).execute().data or []

@st.cache_data(ttl=60)
def get_disciplinas():
    return supabase.table("disciplina").select("*").eq("ativo", True).order("nome").execute().data or []

def clear_cache():
    st.cache_data.clear()
