import unicodedata
import time
import requests as req

URL = "SUA URL"


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )
    return texto


def criar_conta(username, email, senha):
    usuario = {
        "username": normalizar(username),
        "email": normalizar(email),
        "senha": senha
    }

    response = req.post(f"{URL}/usuarios.json", json=usuario)

    if response.status_code != 200:
        return f"Erro ao criar conta: {response.text}"

    data = response.json()

    if "name" not in data:
        return f"Resposta inesperada do Firebase: {data}"

    user_id = data["name"]

    # adiciona o ID dentro do usuário
    req.patch(
        f"{URL}/usuarios/{user_id}.json",
        json={"id": user_id}
    )

    return f"Conta criada com sucesso! ID: {user_id}"


def login(email, senha):
    response = req.get(f"{URL}/usuarios.json")

    if response.status_code != 200:
        return f"Erro Firebase: {response.text}"

    usuarios = response.json()

    if not usuarios:
        return "Nenhum usuário cadastrado"

    email = normalizar(email)

    for user_id, dados in usuarios.items():
        if dados.get("email") == email and dados.get("senha") == senha:
            return f"Login realizado com sucesso! ID: {user_id}"

    return "Email ou senha incorretos."


def trocar_email(user_id, novo_email):
    response = req.get(f"{URL}/usuarios/{user_id}.json")

    if response.status_code != 200:
        return f"Erro Firebase: {response.text}"

    if response.json() is None:
        return "Usuário não encontrado."

    patch = req.patch(
        f"{URL}/usuarios/{user_id}.json",
        json={"email": normalizar(novo_email)}
    )

    if patch.status_code != 200:
        return f"Erro ao atualizar email: {patch.text}"

    return "Email atualizado com sucesso!"


def trocar_senha(email, nova_senha, senha_atual=None, user_id=None):
    response = req.get(f"{URL}/usuarios.json")

    if response.status_code != 200:
        return f"Erro Firebase: {response.text}"

    usuarios = response.json()

    if not usuarios:
        return "Nenhum usuário cadastrado."

    email = normalizar(email)

    for uid, dados in usuarios.items():
        if dados.get("email") == email:

            if senha_atual:
                if dados.get("senha") != senha_atual:
                    return "Senha atual incorreta."

            elif user_id:
                if dados.get("id") != user_id:
                    return "ID inválido."

            else:
                return "Informe a senha atual ou ID de usuário."

            patch = req.patch(
                f"{URL}/usuarios/{uid}.json",
                json={"senha": nova_senha}
            )

            if patch.status_code != 200:
                return f"Erro ao atualizar senha: {patch.text}"

            return "Senha alterada com sucesso."

    return "Usuário não encontrado."


def opcoes():
    print("\nBem-vindo ao sistema!")
    opcao = input(
        "1- Login\n"
        "2- Criar conta\n"
        "3- Trocar email\n"
        "4- Trocar senha\n"
        "Escolha: "
    )

    if opcao == "1":
        email = input("Email: ")
        senha = input("Senha: ")
        print(login(email, senha))

    elif opcao == "2":
        username = input("Username: ")
        email = input("Email: ")
        senha = input("Senha: ")
        print(criar_conta(username, email, senha))

    elif opcao == "3":
        user_id = input("ID do usuário: ")
        novo_email = input("Novo email: ")
        print(trocar_email(user_id, novo_email))

    elif opcao == "4":
        email = input("Email: ")
        nova_senha = input("Nova senha: ")

        escolha = input("1- Senha atual\n2- ID\nEscolha: ")

        if escolha == "1":
            senha_atual = input("Senha atual: ")
            print(trocar_senha(email, nova_senha, senha_atual=senha_atual))

        elif escolha == "2":
            user_id = input("ID: ")
            print(trocar_senha(email, nova_senha, user_id=user_id))

        else:
            print("Opção inválida")

    else:
        print("Opção não encontrada.")


while True:
    time.sleep(1)
    opcoes()
