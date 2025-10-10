"""
Testes automatizados simples para a API Flask do agente.
Simula conversas de leads e valida as respostas retornadas.
"""

import requests

BASE_URL = "http://127.0.0.1:8000/query"


def send_message(number, question):
    """
    Envia uma mensagem simulada para o endpoint Flask.

    Args:
        number (str): Número do usuário (simulado).
        question (str): Texto enviado pelo usuário.

    Returns:
        dict: Resposta JSON da API.
    """
    print(f"\n Enviando pergunta: {question}")
    response = requests.post(BASE_URL, json={
        "question": question,
        "number": number
    })

    if response.status_code != 200:
        print(f" Erro HTTP: {response.status_code}")
        print("Resposta:", response.text)
        raise SystemExit(1)

    data = response.json()
    print(" Resposta:", data)
    return data


def test_full_lead_conversation():
    """
    Testa o fluxo completo de captação de lead:
    nome -> serviço -> horário -> telefone.
    """
    user_number = "5511999998888@c.us"

    # Dados dinâmicos do lead
    nome_cliente = "Gabriel"
    servico = "Criação de site"
    horario = "Amanhã às 14h"
    telefone = "(81) 99999-9999"

    try:
        # Envia nome
        response1 = send_message(user_number, nome_cliente)
        assert "serviço" in response1["message"].lower(), "Esperado pergunta sobre o serviço"

        # Envia serviço
        response2 = send_message(user_number, servico)
        assert "horário" in response2["message"].lower(), "Esperado pergunta sobre o horário"

        # Envia horário
        response3 = send_message(user_number, horario)
        assert "telefone" in response3["message"].lower(), "Esperado pergunta sobre o telefone"

        # Envia telefone
        response4 = send_message(user_number, telefone)
        assert "obrigado" in response4["message"].lower(), "Esperado mensagem de agradecimento"
        assert nome_cliente.lower() in response4["message"].lower(), "Esperado nome na resposta"

        # Testa mensagem após término
        response5 = send_message(user_number, "Quero outro serviço")
        assert ("agendamento" in response5["message"].lower() or
                "serviço" in response5["message"].lower()), "Esperado reinício de agendamento"

        print("\n [SUCESSO] Fluxo completo de lead testado com êxito!")

    except AssertionError as e:
        print(f"\n [FALHA] {e}")
        raise


def test_invalid_request():
    """
    Testa envio de requisição inválida (sem parâmetros obrigatórios).
    """
    print("\n Testando requisição inváclslida...")
    response = requests.post(BASE_URL, json={})
    if response.status_code == 400:
        print(" Retorno 400 recebido corretamente.")
    else:
        print(f" Código de status inesperado: {response.status_code}")

    data = response.json()
    assert "inválido" in data["message"].lower(), "Esperado mensagem de erro sobre requisição inválida"
    print(" Mensagem de erro validada com sucesso.")


if __name__ == "__main__":
    # Teste automatico
    # print(" Iniciando testes manuais da API...\n")
    # test_full_lead_conversation()
    # test_invalid_request()
    # print("\n Todos os testes finalizados.")

    # Teste manual (simula conversa)
    user_number = "5511999998800@c.us"
    # response1 = send_message(user_number, "Oi")
    # print(response1)
    # response2 = send_message(user_number, "Gabriel")
    # print(response2)
    # response3 = send_message(user_number, "Criação de site")
    # print(response3)
    response4 = send_message(user_number, "Amanhã às 14h")
    print(response4)
    response5 = send_message(user_number, "(81) 99999-9999")
    print(response5)
    response6 = send_message(user_number, "Quero outro serviço")
    print(response6)
