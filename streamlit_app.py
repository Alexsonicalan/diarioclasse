import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Sistema de Gestão Acadêmica", layout="wide")

# Inicializando variáveis para simulação
cursos = []
disciplinas = []
instrutores = []
alunos = []

# Navegação entre páginas
menu = st.sidebar.radio("Navegação", ["Login", "Cadastro", "Retirada de Faltas"])

# Página 1: Login
if menu == "Login":
    st.title("Login")
    user_type = st.radio("Selecione o tipo de usuário:", ["Administrador", "Usuário Comum"])
    username = st.text_input("Usuário:")
    password = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        st.success(f"Bem-vindo, {username}! (Tipo: {user_type})")

# Página 2: Cadastro
elif menu == "Cadastro":
    st.title("Cadastro de Cursos, Disciplinas, Instrutores e Alunos")

    # Cadastro de Cursos
    st.subheader("Cadastro de Cursos")
    course_name = st.text_input("Nome do Curso:")
    class_group = st.text_input("Turma:")
    course_hours = st.number_input("Carga Horária Total:", min_value=1)
    year = st.number_input("Ano:", min_value=1900, max_value=2100, step=1)
    if st.button("Cadastrar Curso"):
        cursos.append({
            "Nome do Curso": course_name,
            "Turma": class_group,
            "Carga Horária": course_hours,
            "Ano": year
        })
        st.success(f"Curso '{course_name}' cadastrado com sucesso!")

    # Cadastro de Disciplinas
    st.subheader("Cadastro de Disciplinas")
    subject_name = st.text_input("Nome da Disciplina:")
    subject_hours = st.number_input("Carga Horária da Disciplina:", min_value=1)
    if st.button("Cadastrar Disciplina"):
        disciplinas.append({
            "Nome da Disciplina": subject_name,
            "Carga Horária": subject_hours
        })
        st.success(f"Disciplina '{subject_name}' cadastrada com sucesso!")

    # Cadastro de Instrutores
    st.subheader("Cadastro de Instrutores")
    instructor_id = st.text_input("Matrícula do Instrutor:")
    instructor_name = st.text_input("Nome do Instrutor:")
    if st.button("Cadastrar Instrutor"):
        instrutores.append({
            "Matrícula": instructor_id,
            "Nome": instructor_name
        })
        st.success(f"Instrutor '{instructor_name}' cadastrado com sucesso!")

    # Cadastro de Alunos
    st.subheader("Cadastro de Alunos")
    student_id = st.text_input("Matrícula do Aluno:")
    student_name = st.text_input("Nome do Aluno:")
    if st.button("Cadastrar Aluno"):
        alunos.append({
            "Matrícula": student_id,
            "Nome": student_name
        })
        st.success(f"Aluno '{student_name}' cadastrado com sucesso!")

    # Upload de Alunos em Lote
    st.subheader("Cadastro de Alunos em Lote (Upload de CSV)")
    # Link para baixar modelo
    model_data = {
        "Matrícula": ["123", "124"],
        "Nome": ["Aluno Exemplo 1", "Aluno Exemplo 2"]
    }
    df_model = pd.DataFrame(model_data)
    st.download_button(
        label="Baixar modelo de planilha",
        data=df_model.to_csv(index=False).encode("utf-8"),
        file_name="modelo_alunos.csv",
        mime="text/csv"
    )
    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Faça upload de um arquivo CSV com os alunos", type=["csv"])
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            alunos.extend(df_uploaded.to_dict(orient="records"))
            st.write("Prévia do arquivo enviado:")
            st.dataframe(df_uploaded)
            st.success("Alunos carregados com sucesso!")
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")

    # Botão para salvar dados em Excel
    if st.button("Salvar Dados em Excel"):
        with pd.ExcelWriter("dados_cadastrados.xlsx") as writer:
            pd.DataFrame(cursos).to_excel(writer, sheet_name="Cursos", index=False)
            pd.DataFrame(disciplinas).to_excel(writer, sheet_name="Disciplinas", index=False)
            pd.DataFrame(instrutores).to_excel(writer, sheet_name="Instrutores", index=False)
            pd.DataFrame(alunos).to_excel(writer, sheet_name="Alunos", index=False)
        st.success("Dados salvos em 'dados_cadastrados.xlsx'!")

# Página 3: Retirada de Faltas
elif menu == "Retirada de Faltas":
    st.title("Retirada de Faltas")
    
    # Seleção do Curso
    st.subheader("Selecionar Curso")
    selected_course = st.selectbox("Curso:", [c["Nome do Curso"] for c in cursos])
    
    # Seleção do Instrutor
    st.subheader("Selecionar Instrutor")
    selected_instructor = st.selectbox("Instrutor:", [i["Nome"] for i in instrutores])
    
    # Seleção da Disciplina
    st.subheader("Selecionar Disciplina")
    selected_subject = st.selectbox("Disciplina:", [d["Nome da Disciplina"] for d in disciplinas])

    # Seleção de Alunos e Registro de Faltas
    st.subheader("Registrar Faltas")
    st.write("Selecione o status de presença para cada aluno:")
    if alunos:
        for student in alunos:
            status = st.selectbox(
                f"{student['Nome']} ({student['Matrícula']})", 
                ["0 falta", "1 falta", "2 faltas", "3 faltas", "4 faltas", "Atrasado"],
                key=student["Matrícula"]
            )
    else:
        st.warning("Nenhum aluno cadastrado.")
    
    if st.button("Salvar Faltas"):
        st.success("Faltas registradas com sucesso!")
