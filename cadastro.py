import streamlit as st

st.set_page_config(page_title='Cadastro', page_icon='👤', layout='centered')

st.title('Cadastro de Usuários')

matricula = st.text_input('Matrícula:')
nome = st.text_input('Nome:')

if st.button('Cadastrar'):
    if not matricula or not nome:
        st.error('Preencha todos os campos!')

    else:
        with open('alunos.txt', 'r', encoding='utf-8') as arquivo:
            cadastros = [linha.strip() for linha in arquivo.readlines()]

        if matricula in cadastros:
            st.error('Número de matrícula já está cadastrado!')
        else:
            with open('alunos.txt', 'a', encoding='utf-8') as arquivo:
                arquivo.write(f'{matricula}\n{nome}\n')
                st.success(f'{nome} cadastrado com sucesso!')

st.title('Alunos cadastrados')

with open('alunos.txt', 'r', encoding='utf-8') as arquivo:
    cadastros = [linha.strip() for linha in arquivo.readlines()]

if len(cadastros) > 0:
    for i in range(0, len(cadastros), 2):
        with st.container(border=False):
            coluna_info, coluna_botao = st.columns([9, 1])

            with coluna_info:
                st.info(f'{cadastros[i]} | {cadastros[i + 1]}')

            with coluna_botao:
                if st.button('🗑️', key=f'excluir_{i}'):
                    del cadastros[i:i + 2]

                    with open('alunos.txt', 'w', encoding='utf-8') as arquivo:
                        for linha in cadastros:
                            arquivo.write(linha + '\n')

                    st.rerun()