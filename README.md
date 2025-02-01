# **Voidzinho Discord Bot**

O **Voidzinho** é um bot para Discord que utiliza inteligência artificial para gerar respostas, processar anexos (PDF, DOCX, código) e criar arquivos de código com base em descrições. Ele é ideal para desenvolvedores, estudantes e entusiastas de tecnologia que desejam automatizar tarefas no Discord.

---

## **Funcionalidades**

- ✨ **Geração de Respostas**: Utiliza modelos de linguagem para responder perguntas e gerar conteúdo.
- 📄 **Processamento de Anexos**:
  - Extrai texto de arquivos **PDF** e **DOCX**.
  - Explica o conteúdo de arquivos de código (**JavaScript, Python, HTML, CSS, etc.**).
- 📝 **Criação de Arquivos de Código**: Gera arquivos de código (**HTML, CSS, JS, Python**) com base em descrições.
- 🛠️ **Comandos Úteis**:
  - `-ajuda` — Mostra todos os comandos disponíveis.
  - `-limpar` — Apaga mensagens do canal.
  - `-sorte` — Gera 3 jogos únicos da Mega Sena.
  - `-wiki` — Busca informações na Wikipedia.
  - `-dev` — Cria arquivos de código com base em uma descrição.

---

## **Instalação**

### **Requisitos**

- **Python 3.8 ou superior**
- Conta no [Hugging Face](https://huggingface.co/) para obter uma chave de API.
- Conta no [Discord Developer Portal](https://discord.com/developers/applications) para criar um bot.

### **Passo a Passo**

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/voidzinhodiscord.git
   cd voidzinhodiscord
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado)**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # No Windows
   source venv/bin/activate  # No macOS/Linux
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   - Crie um arquivo `.env` na raiz do projeto e adicione:
     ```env
     KEY_DISCORD=sua_chave_discord_aqui
     KEY_LLAMA=sua_chave_huggingface_aqui
     CANAL_ID=id_do_canal_discord_aqui
     ```

5. **Inicie o bot**:
   ```bash
   python voidzinho.py
   ```

---

## **Comandos Disponíveis**

| Comando   | Descrição |
|-----------|------------|
| `-ajuda`  | Mostra todos os comandos disponíveis. |
| `-limpar` | Apaga mensagens do canal. Use `-limpar all` para apagar todas as mensagens. |
| `-sorte`  | Gera 3 jogos únicos da Mega Sena. |
| `-dm`     | Inicia uma conversa privada com o bot no Direct Message (DM). |
| `-wiki`   | Busca informações na Wikipedia. |
| `-dev`    | Cria arquivos de código com base em uma descrição. |

---

## **Exemplos de Uso**

**🏠 Criar um site simples:**
```bash
-dev "Crie um site simples com um título, uma lista de produtos e um estilo CSS básico."
```

**📝 Buscar informações na Wikipedia:**
```bash
-wiki "Inteligência Artificial"
```

**📄 Processar um arquivo PDF:**
- Anexe um arquivo **PDF** no chat e o bot extrairá o texto e gerará uma interpretação.

**👨‍💻 Explicar um arquivo de código:**
- Anexe um arquivo de código (**JavaScript, Python, etc.**) e o bot explicará o conteúdo.

---

## **📚 Licença**

Este projeto está licenciado sob a [MIT License](LICENSE).

## **🌟 Contribuição**

Sinta-se à vontade para abrir **issues** e enviar **pull requests**!

### **Desenvolvedor Principal**
- **Haygo Nunes** 🌟

---

Feito com ❤️ por Haygo Nunes e a comunidade! 🚀

