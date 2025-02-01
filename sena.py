import pandas as pd
import random
from collections import Counter
import discord
import os

def carregar_jogos(arquivo):
    """Carrega os dados do arquivo .xlsx e retorna uma lista de tuplas com os jogos passados."""
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo {arquivo} não encontrado.")
    
    try:
        df = pd.read_excel(arquivo, skiprows=6, usecols="A:H")
        jogos_passados = [tuple(sorted(row[f'bola {i}'] for i in range(1, 7))) for _, row in df.iterrows()]
        return jogos_passados
    except Exception as e:
        raise ValueError(f"Erro ao carregar o arquivo: {e}")

def contar_frequencias(jogos_passados):
    """Conta a frequência dos números nos jogos passados e retorna os números mais frequentes."""
    todos_os_numeros = [numero for jogo in jogos_passados for numero in jogo]
    contagem = Counter(todos_os_numeros)
    numeros_frequentes = [numero for numero, _ in contagem.most_common()]
    return numeros_frequentes, contagem

def analisar_intervalos(jogos_passados):
    """Analisa os intervalos dos números nos jogos passados."""
    intervalos = {i: 0 for i in range(6)} 
    for jogo in jogos_passados:
        for numero in jogo:
            intervalo = (numero - 1) // 10
            if intervalo < 6:
                intervalos[intervalo] += 1
    return intervalos

def evitar_padroes(jogo):
    """Evita números sequenciais ou padrões comuns."""
    for i in range(len(jogo)-1):
        if jogo[i] + 1 == jogo[i+1]:
            return True
    return False

def calcular_pares_amigos(jogos_passados, numeros_quentes, numeros_frios):
    """Calcula pares de números amigos (quentes e frios que aparecem juntos)."""
    pares_amigos = Counter()
    for jogo in jogos_passados:
        quentes_no_jogo = [numero for numero in jogo if numero in numeros_quentes]
        frios_no_jogo = [numero for numero in jogo if numero in numeros_frios]
        for quente in quentes_no_jogo:
            for frio in frios_no_jogo:
                pares_amigos[(quente, frio)] += 1  
    return pares_amigos

def combinar_quentes_frios_com_amigos(numeros_quentes, numeros_frios, jogos_passados):
    """Combina números quentes e frios com base na frequência de coaparição."""
    pares_amigos = calcular_pares_amigos(jogos_passados, numeros_quentes, numeros_frios)
    quentes_e_frios = []
    num_quentes_selecionados = min(2, len(numeros_quentes))
    if not numeros_frios:
        numeros_frios = list(set(range(1, 61)) - set(numeros_quentes))
    quentes_selecionados = random.sample(numeros_quentes, num_quentes_selecionados)
    for quente in quentes_selecionados:
        amigos = [(frio, freq) for (q, frio), freq in pares_amigos.items() if q == quente]
        if amigos:
            frio = max(amigos, key=lambda x: x[1])[0]
        else:
            frio = random.choice(numeros_frios)
        quentes_e_frios.append(quente)
        quentes_e_frios.append(frio)
    return quentes_e_frios

def gerar_jogo_com_probabilidade(jogos_passados, jogos_passados_set, numeros_frequentes, intervalos, todos_os_numeros, contagem):
    """Gera um novo jogo com base em probabilidades e evita padrões comuns."""
    tentativas = 0
    max_tentativas = 10000
    while tentativas < max_tentativas:
        tentativas += 1
        
        numeros_quentes = [numero for numero, _ in contagem.most_common(20)]
        numeros_frios = [numero for numero, _ in contagem.most_common()[-20:]]

        numeros_quentes_3 = random.sample(numeros_quentes, min(3, len(numeros_quentes)))
        
        intervalos_selecionados = [i for i, count in intervalos.items() if count > 0]
        numeros_intervalos = []
        for intervalo in intervalos_selecionados:
            numeros_intervalos.extend(range(intervalo * 10 + 1, intervalo * 10 + 11))
        numeros_intervalos = list(set(numeros_intervalos) - set(numeros_quentes_3))
        numeros_aleatorios = random.sample(numeros_intervalos, min(3, len(numeros_intervalos)))
        
        quentes_e_frios = combinar_quentes_frios_com_amigos(numeros_quentes, numeros_frios, jogos_passados)
        
        todos_numeros = numeros_quentes_3 + numeros_aleatorios + quentes_e_frios
        todos_numeros_unicos = list(set(todos_numeros))
        
        if len(todos_numeros_unicos) < 6:
            numeros_restantes = list(set(range(1, 61)) - set(todos_numeros_unicos))
            todos_numeros_unicos.extend(random.sample(numeros_restantes, 6 - len(todos_numeros_unicos)))
        elif len(todos_numeros_unicos) > 6:
            todos_numeros_unicos = random.sample(todos_numeros_unicos, 6)
        
        novo_jogo = sorted(todos_numeros_unicos)
        
        if tuple(novo_jogo) not in jogos_passados_set:
            jogos_passados_set.add(tuple(novo_jogo))
            return tuple(novo_jogo)
    
    raise Exception(f"Não foi possível gerar um jogo único após {max_tentativas} tentativas.")

def gerar_jogos_unicos(arquivo, num_jogos):
    """Gera novos jogos únicos com base nos jogos passados."""
    jogos_passados = carregar_jogos(arquivo)
    jogos_passados_set = set(jogos_passados)
    numeros_frequentes, contagem = contar_frequencias(jogos_passados)
    intervalos = analisar_intervalos(jogos_passados)
    todos_os_numeros = [numero for jogo in jogos_passados for numero in jogo]
    novos_jogos = []
    
    for _ in range(num_jogos):
        novo_jogo = gerar_jogo_com_probabilidade(
            jogos_passados, jogos_passados_set, numeros_frequentes, intervalos, todos_os_numeros, contagem
        )
        novos_jogos.append(novo_jogo)
    
    return novos_jogos

async def sorte(ctx):
    """Gera novos jogos únicos para a Mega Sena e envia no Discord."""
    with open("carregando.gif", "rb") as gif_file:
        mensagem_processo = await ctx.send(
            content="⏳ O processo de geração dos jogos está em andamento e pode demorar um pouco...",
            file=discord.File(gif_file, filename="carregando.gif")
        )

    arquivo = "sorteio.xlsx"  
    num_jogos = 3
    try:
        jogos = gerar_jogos_unicos(arquivo, num_jogos)
    except Exception as e:
        await mensagem_processo.edit(content=f"Ocorreu um erro: {e}", attachments=[])
        return

    jogos_formatados = "\n".join(f" {', '.join(map(str, jogo))}" for jogo in jogos)

    mensagem = (
        "🎉 **Aqui estão seus jogos únicos da Mega Sena** 🎉\n\n"
        "Esses jogos nunca foram jogados entre 1996 e 2024. Boa sorte! 🍀\n\n"
        "**Jogos gerados**:\n"
        f"```diff\n{jogos_formatados}\n```"
        "\nBoa Sorte e que a sorte esteja ao seu lado! 🍀✨"
    )

    await mensagem_processo.edit(content=mensagem, attachments=[])