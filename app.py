import streamlit as st

def ler_usuarios(arquivo='users.txt'):
    with open('users.txt', 'r', encoding='utf-8') as arquivo:
        return [usuario.strip() for usuario in arquivo.readlines()]

st.set_page_config(page_title='Login simples', layout='centered')

if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'dados_usuario' not in st.session_state:
    st.session_state.dados_usuario = {}

if not st.session_state.logado:
    aba_login, aba_cadastro = st.tabs(['Login', 'Cadastro'])

    with aba_cadastro:
        st.subheader('Cadastre-se aqui')

        with st.form('form_cadastro'):
            nome = st.text_input('Nome', placeholder='Seu nome aqui')
            email = st.text_input('Email', type='email')
            senha = st.text_input('Senha', type='password')
            cadastrar = st.form_submit_button('Cadastrar', use_container_width=True)

        if cadastrar:
            if not nome.split() or not email or not senha.split():
                st.error('Preencha todos os campos!')

            else:
                usuarios = ler_usuarios()

                if email in usuarios:
                    st.error('Email já cadastrado no sistema!')
                else:
                    with open('users.txt', 'a', encoding='utf-8') as arquivo:
                        arquivo.write(f'{email}\n{senha}\n{nome}\n')
                        st.success('Usuário cadastrado com sucesso!')

    with aba_login:
        st.subheader('Login de usuário')

        with st.form('form_login'):
            email = st.text_input('Email', type='email')
            senha = st.text_input('Senha', type='password')
            entrar = st.form_submit_button('Entrar', use_container_width=True)

        if entrar:
            if not email.split() or not senha.split():
                st.error('Preencha todos os campos!')
            else:
                usuarios = ler_usuarios()

                if email in usuarios:
                    indice = usuarios.index(email)

                    if senha == usuarios[indice + 1]:
                        st.session_state.dados_usuario = {
                            'email': usuarios[indice],
                            'senha': usuarios[indice + 1],
                            'nome': usuarios[indice + 2]
                        }
                        st.session_state.logado = True
                        st.rerun()
                    else:
                        st.error('Senha errada')

                else:
                    st.error('Usuário não cadastrado!')

else:
    aba_teste, aba_perfil = st.tabs(['Em breve','Perfil'])

    with aba_perfil:
        st.subheader('Perfil de Usuário')

        with st.container(border=True):
            st.write(f"Nome: {st.session_state.dados_usuario['nome']}")
            st.write(f"Email: {st.session_state.dados_usuario['email']}")
            st.write(f"Senha: {st.session_state.dados_usuario['senha']}")

            if st.button('Sair'):
                st.session_state.logado = False
                st.session_state.dados_usuario = {}
                st.rerun()

        st.subheader('Atualizar dados')

        with st.form('atualizar_dados'):
            nome = st.text_input('Novo nome', placeholder='Seu nome aqui', value=st.session_state.dados_usuario['nome'])
            email = st.text_input('Novo email', type='email', value=st.session_state.dados_usuario['email'])
            senha = st.text_input('Nova senha', type='password', value=st.session_state.dados_usuario['senha'])
            atualizar = st.form_submit_button('Atualizar', use_container_width=True)

        if atualizar:
            if not nome.split() or not email or not senha.split():
                st.error('Preencha todos os campos!')

            else:
                usuarios = ler_usuarios()
                if email in usuarios and email != st.session_state.dados_usuario['email']:
                    st.error('Email já cadastrado no sistema!')
                else:
                    indice = usuarios.index(st.session_state.dados_usuario['email'])        
                    usuarios[indice] = email
                    usuarios[indice + 1] = senha
                    usuarios[indice + 2] = nome
                    st.session_state.dados_usuario = {
                        'email': usuarios[indice],
                        'senha': usuarios[indice + 1],
                        'nome': usuarios[indice + 2]
                    }

                    with open('users.txt', 'w', encoding='utf-8') as arquivo:
                        arquivo.writelines([f'{linha}\n' for linha in usuarios])

                    st.success('Usuário atualizado com sucesso!')
                    st.rerun()

        if st.button('Excluir Conta', use_container_width=True, type='primary'):
            usuarios = ler_usuarios()
            indice = usuarios.index(st.session_state.dados_usuario['email'])
            del usuarios[indice:indice+3]

            with open('users.txt', 'w', encoding='utf-8') as arquivo:
                arquivo.writelines([f'{linha}\n' for linha in usuarios])

            st.session_state.logado = False
            st.session_state.dados_usuario = {}
            st.rerun()

    with aba_teste:
        st.subheader('Em breve')
        st.text('O conteúdo dessa aba ainda está sendo desenvolvido')
        st.button('Saiba mais')

