import os
import re
import asyncio
import tempfile
import zipfile
import discord
import pdfplumber
import wikipediaapi
from discord.ext import commands
from dotenv import load_dotenv
from langdetect import detect
import discord
import sena
from collections import deque
from huggingface_hub import InferenceClient
<<<<<<< Updated upstream
from docx import Document

# Carregar variáveis de ambiente
load_dotenv()
KEY_DISCORD = os.getenv('KEY_DISCORD')
KEY_LLAMA = os.getenv('KEY_LLAMA')
CANAL_ID = int(os.getenv('CANAL_ID'))

# Verificação de configuração essencial
if not KEY_DISCORD or not KEY_LLAMA or not CANAL_ID:
    raise ValueError("As chaves de ambiente 'KEY_DISCORD', 'KEY_LLAMA' e 'CANAL_ID' devem estar configuradas no arquivo .env.")

# Configuração do cliente LLaMA
llama_client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=KEY_LLAMA)

# Configurações globais
MAX_TOKENS = 800
MAX_HISTORY_LENGTH = 10
conversation_history = deque(maxlen=MAX_HISTORY_LENGTH)  # Histórico de mensagens com tamanho limitado

#### Funções Auxiliares ####
=======
import aiohttp
import os

# Configurações para o modelo LLaMA
llama_client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token=os.getenv("HUGGINGFACE_TOKEN")  
)
>>>>>>> Stashed changes

def resposta_voidzinho(prompt, linguagem="texto"):
    """Gera uma resposta usando o cliente LLaMA com histórico de conversa."""
    global conversation_history

    # Limitar histórico de mensagens para respeitar MAX_TOKENS
    history_text = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    prompt_formatado = f"{history_text}\nuser: Responda em Português (PT-BR) {linguagem}:\n\n{prompt}\nassistant:"

    try:
        response = llama_client.chat_completion(
            messages=[{"role": "user", "content": prompt_formatado}],
            max_tokens=MAX_TOKENS,
            stream=False
        )
        assistant_reply = response['choices'][0]['message']['content']

        # Atualizar histórico
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

def detectar_linguagem(texto):
    """Detecta o idioma de um texto."""
    try:
        linguagem = detect(texto)
        return "Português" if linguagem == 'pt' else "Inglês"
    except Exception as e:
        print(f"Erro ao detectar linguagem: {e}")
        return "texto"

def extrair_codigo_e_criar_arquivo(resposta):
    """Identifica código em respostas e salva em arquivos temporários."""
    arquivos = {
        "html": ("index.html", r"```html\n(.*?)```", "HTML"),
        "css": ("style.css", r"```css\n(.*?)```", "CSS"),
        "js": ("script.js", r"```(javascript|js)\n(.*?)```", "JavaScript"),
        "python": ("script.py", r"```(python|py)\n(.*?)```", "Python")
    }
    temp_paths = []

    for ext, (filename, pattern, lang) in arquivos.items():
        matches = re.findall(pattern, resposta, re.DOTALL)
        for match in matches:
            code = match[1] if isinstance(match, tuple) else match
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_file:
                temp_file.write(code.encode())
                temp_paths.append(temp_file.name)

    return temp_paths

async def enviar_mensagem_fragmentada(canal, conteudo):
    """Envia mensagens maiores que o limite em partes."""
    limite = 2000
    partes = [conteudo[i:i + limite] for i in range(0, len(conteudo), limite)]
    for parte in partes:
        await canal.send(parte)

#### Processamento de Anexos ####

async def processar_anexo_pdf(message, attachment):
    """Extrai e processa texto de arquivos PDF."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await attachment.read())
            temp_file.seek(0)
            with pdfplumber.open(temp_file.name) as pdf:
                texto_paginas = [page.extract_text() for page in pdf.pages if page.extract_text()]
                texto = '\n'.join(texto_paginas)

                # Gerar interpretação do texto extraído
                resposta = resposta_voidzinho(texto, detectar_linguagem(texto))
                await enviar_mensagem_fragmentada(message.channel, resposta)
    except Exception as e:
        await message.channel.send(f"Erro ao processar PDF: {e}")

async def processar_anexo_docx(message, attachment):
    """Extrai e processa texto de arquivos DOCX."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            temp_file.write(await attachment.read())
            temp_file.seek(0)
            doc = Document(temp_file.name)
            texto_paragrafos = [para.text for para in doc.paragraphs if para.text]
            texto = '\n'.join(texto_paragrafos)

            # Gerar interpretação do texto extraído
            resposta = resposta_voidzinho(texto, detectar_linguagem(texto))
            await enviar_mensagem_fragmentada(message.channel, resposta)
    except Exception as e:
        await message.channel.send(f"Erro ao processar DOCX: {e}")

async def processar_anexo_codigo(message, attachment):
    """Processa arquivos de código (js, py, c, cpp, etc.) e explica o conteúdo."""
    try:
        extensao = attachment.filename.split('.')[-1].lower()
        linguagens_suportadas = {
            'js': 'JavaScript',
            'py': 'Python',
            'c': 'C',
            'cpp': 'C++',
            'java': 'Java',
            'html': 'HTML',
            'css': 'CSS',
        }

        if extensao not in linguagens_suportadas:
            await message.channel.send(f"❌ Formato de arquivo não suportado: {extensao}.")
            return

        conteudo = await attachment.read()
        conteudo_texto = conteudo.decode('utf-8')

        prompt = f"Explique o seguinte código {linguagens_suportadas[extensao]}:\n\n{conteudo_texto}"
        explicacao = resposta_voidzinho(prompt, linguagem="texto")

        await enviar_mensagem_fragmentada(message.channel, f"📝 **Explicação do código ({linguagens_suportadas[extensao]}):**\n\n{explicacao}")

    except Exception as e:
        await message.channel.send(f"❌ Erro ao processar arquivo de código: {e}")

#### Configuração do Bot ####

intents = discord.Intents.default()
intents.message_content = True
<<<<<<< Updated upstream
bot = commands.Bot(command_prefix="-", intents=intents)
=======
bot = commands.Bot(command_prefix="!", intents=intents)

# Armazena o conteúdo dos arquivos carregados
projetos = {}

# Função para detectar a linguagem de programação
def detectar_linguagem(input_usuario):
    input_usuario = input_usuario.lower()
    if "python" in input_usuario:
        return "Python"
    elif "html" in input_usuario:
        return "HTML"
    elif "css" in input_usuario:
        return "CSS"
    elif "javascript" in input_usuario or "js" in input_usuario:
        return "JavaScript"
    return "texto"

# Função para formatar respostas com código
def formatar_resposta_com_codigo(resposta, linguagem="texto"):
    if linguagem.lower() in ["python", "html", "css", "javascript"]:
        return f"```{linguagem.lower()}\n{resposta}\n```"
    return resposta

# Função para enviar mensagens longas em partes
async def enviar_mensagem_em_partes(canal, mensagem):
    for i in range(0, len(mensagem), 2000):
        await canal.send(mensagem[i:i + 2000])
>>>>>>> Stashed changes

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

    # Busca o canal pelo ID
    canal = bot.get_channel(CANAL_ID)

    if canal:
        await canal.send("🎉 **Voidzinho está online!** 🎉\n\nDigite `-ajuda` para ver todos os comandos disponíveis.")
    else:
        print(f"Canal com ID {CANAL_ID} não encontrado.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Processar anexos
    if message.attachments:
        for attachment in message.attachments:
            filename = attachment.filename
            if filename.endswith('.pdf'):
                await processar_anexo_pdf(message, attachment)
            elif filename.endswith('.docx'):
                await processar_anexo_docx(message, attachment)
            elif filename.split('.')[-1].lower() in ['js', 'py', 'c', 'cpp', 'java', 'html', 'css']:
                await processar_anexo_codigo(message, attachment)
        return

    # Processar mensagens de texto
    if not message.content.startswith("-"):
        linguagem = detectar_linguagem(message.content)
        resposta = resposta_voidzinho(message.content, linguagem)
        await enviar_mensagem_fragmentada(message.channel, resposta)

    await bot.process_commands(message)

@bot.command(name="limpar", help="Apaga mensagens do canal.")
@commands.has_permissions(manage_messages=True)
async def limpar(ctx, tipo=None):
    if tipo == "all":
        await ctx.channel.purge()
        confirmacao = await ctx.send("Todas as mensagens foram apagadas.")
        await confirmacao.delete(delay=5)
        aviso = await ctx.send("Use o comando `-ajuda` para ver todos os comandos.")
    else:
        await ctx.send("Especifique o tipo de limpeza. Ex: `-limpar all`", delete_after=5)

@bot.command(name="sorte", help="Gera 3 jogos únicos da Mega Sena.")
async def sorte(ctx):
    await sena.sorte(ctx)

@bot.command(name="dm", help="Inicia uma conversa privada com o bot.")
async def dm(ctx):
    """Inicia uma conversa privada com o usuário no direct message (DM)."""
    try:
        # Envia uma mensagem privada para o usuário
        await ctx.author.send("Olá! Vamos conversar em privado. O que você gostaria de discutir?")
        
        # Confirma no canal público que a DM foi enviada
        await ctx.send(f"{ctx.author.mention}, eu te enviei uma mensagem privada! Verifique sua DM.")
    except discord.Forbidden:
        # Caso o usuário tenha as DMs desativadas ou o bot não possa enviar mensagens
        await ctx.send(f"{ctx.author.mention}, não consigo te enviar uma mensagem privada. Verifique se suas DMs estão abertas para este servidor.")

@bot.command(name="wiki", help="Busca informações na Wikipedia.")
async def wiki(ctx, *, termo: str):
    # Configura o idioma para português e define um user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='pt',
        user_agent='VoidzinhoBot/1.0 (https://github.com/seu-usuario/seu-repositorio)'  # Substitua pelo seu user agent
    )

    try:
        # Busca a página na Wikipedia
        pagina = wiki_wiki.page(termo)
        if pagina.exists():
            # Retorna um resumo da página
            resumo = pagina.summary[:1000]  # Limita o resumo a 1000 caracteres
            mensagem = (
                f"📚 **Wikipedia: {termo.capitalize()}** 📚\n\n"
                f"{resumo}\n\n"
                f"Leia mais em: {pagina.fullurl}"
            )
            await ctx.send(mensagem)
        else:
            await ctx.send(f"Não foi possível encontrar informações sobre {termo} na Wikipedia.")
    except Exception as e:
        await ctx.send(f"Erro ao buscar na Wikipedia: {e}")

<<<<<<< Updated upstream

@bot.command(name="dev", help="Cria arquivos de código com base em uma descrição. Use: -dev [descrição]")
async def dev(ctx, *, descricao: str):
    """Cria arquivos de código com base em uma descrição, gerando múltiplos arquivos se necessário."""
    try:
        # Verifica se a descrição foi fornecida
        if not descricao:
            await ctx.send("❌ Por favor, forneça uma descrição do código que deseja criar.")
            return

        # Lista de arquivos a serem gerados
        arquivos_necessarios = [
            "index.html",  # Exemplo de arquivos para um projeto web
            "style.css",
            "script.js",
            # Adicione mais arquivos conforme necessário
        ]

        # Gera cada arquivo separadamente
        temp_files = []
        for nome_arquivo in arquivos_necessarios:
            # Gera o conteúdo do arquivo usando a IA
            prompt_geracao_codigo = (
                f"Crie o arquivo {nome_arquivo} com base na seguinte descrição:\n\n"
                f"Descrição: {descricao}\n\n"
                f"Retorne **apenas o código**, sem comentários, explicações ou textos adicionais. "
                f"Certifique-se de que o código seja 100% funcional e completo. "
                f"Formate o código em blocos marcados com ```."
            )
            resposta_ia = resposta_voidzinho(prompt_geracao_codigo, linguagem="texto")

            # Extrai o código dos blocos marcados com ```
            padrao_codigo = r"```(?:[a-zA-Z]*\n)?(.*?)```"
            matches = re.findall(padrao_codigo, resposta_ia, re.DOTALL)

            if not matches:
                await ctx.send(f"❌ Não foi possível extrair código para o arquivo {nome_arquivo}.")
                continue

            # Pega o primeiro bloco de código encontrado
            codigo = matches[0].strip()

            # Remove caracteres inválidos do nome do arquivo
            nome_arquivo = re.sub(r'[<>:"/\\|?*]', '_', nome_arquivo)

            # Salva o arquivo temporariamente no modo binário
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{nome_arquivo}", mode='wb') as temp_file:
                temp_file.write(codigo.encode('utf-8'))
                temp_files.append((nome_arquivo, temp_file.name))

        # Se houver apenas um arquivo, envia diretamente
        if len(temp_files) == 1:
            nome_arquivo, caminho_arquivo = temp_files[0]
            await ctx.send(f"✅ **Arquivo gerado:** `{nome_arquivo}`", file=discord.File(caminho_arquivo, filename=nome_arquivo))
        else:
            # Se houver múltiplos arquivos, compacta em um ZIP
            zip_filename = "projeto_gerado.zip"
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for nome_arquivo, caminho_arquivo in temp_files:
                    zipf.write(caminho_arquivo, arcname=nome_arquivo)

            # Envia o arquivo ZIP
            await ctx.send(f"✅ **Arquivos gerados ({len(temp_files)} arquivos):**", file=discord.File(zip_filename))

        # Limpa os arquivos temporários
        for _, caminho_arquivo in temp_files:
            os.remove(caminho_arquivo)
        if len(temp_files) > 1:
            os.remove(zip_filename)

    except Exception as e:
        await ctx.send(f"❌ Erro ao gerar código: {e}")
      

@bot.command(name="ajuda", help="Mostra todos os comandos disponíveis do bot e como usá-los.")
async def ajuda(ctx):
    """Exibe uma lista de todos os comandos disponíveis e suas descrições."""
    mensagem_ajuda = (
        "🎉 **Comandos disponíveis do Voidzinho** 🎉\n\n"
        "Aqui estão todos os comandos que você pode usar:\n\n"
        "**1. `-ajuda`**\n"
        "   - Mostra esta mensagem de ajuda com todos os comandos disponíveis.\n\n"
        "**2. `-dm`**\n"
        "   - Inicia uma conversa privada com o bot no direct message (DM).\n"
        "   - Exemplo: `-dm`\n\n"
        "**3. `-sorte`**\n"
        "   - Gera 3 jogos únicos da Mega Sena.\n"
        "   - Exemplo: `-sorte`\n\n"
        "**4. `-limpar [all]`**\n"
        "   - Apaga mensagens do canal. Use `-limpar all` para apagar todas as mensagens.\n"
        "**5. `-wiki [termo]`**\n"
        "   - Busca informações na Wikipedia.\n"
        "**6. `-dev [linguagem] [descrição]`**\n"
        "   - Cria um arquivo de código com base em uma descrição.\n"
        "   - Exemplo: `-dev Python \"Crie uma função que calcule a média de uma lista de números.\"`\n\n"
        "✨ **Como usar** ✨\n"
        "Para usar qualquer comando, digite `-` seguido do nome do comando. Exemplo: `-sorte`.\n\n"
        "Se precisar de mais ajuda, é só chamar! 😊"
    )

    await ctx.send(mensagem_ajuda)                    

bot.run(KEY_DISCORD)
=======
# Conecte o bot ao servidor do Discord usando o token do bot
bot.run(os.getenv("DISCORD_TOKEN"))
>>>>>>> Stashed changes
