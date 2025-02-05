```markdown
# Voidzinho Discord Bot

Voidzinho é um bot para Discord que utiliza inteligência artificial para gerar respostas, processar anexos (PDF, DOCX, código) e criar arquivos de código a partir de descrições. Destinado a desenvolvedores, estudantes e entusiastas, o bot simplifica tarefas e enriquece a interação nos servidores.

---

## Funcionalidades

- **Geração de Respostas:** Produz conteúdos e responde a perguntas utilizando modelos de linguagem avançados.
- **Processamento de Anexos:**  
  - Extrai texto de arquivos PDF e DOCX.  
  - Explica o conteúdo de arquivos de código (JavaScript, Python, HTML, CSS, etc.).
- **Criação de Arquivos de Código:** Gera arquivos (HTML, CSS, JS, Python) com base em descrições fornecidas.
- **Comandos Essenciais:**
  - `-ajuda` – Exibe a lista de todos os comandos.
  - `-limpar` – Remove mensagens do canal (use `-limpar all` para apagar todas as mensagens).
  - `-sorte` – Gera três jogos únicos da Mega Sena.
  - `-wiki` – Pesquisa informações na Wikipedia.
  - `-dev` – Cria arquivos de código a partir de uma descrição.
  - `-dm` – Inicia uma conversa privada com o bot.

---

## Instalação

### Requisitos

- **Python 3.8+**
- Conta no [Hugging Face](https://huggingface.co/) (necessária para a chave de API)
- Conta no [Discord Developer Portal](https://discord.com/developers/applications) (para criação do bot)

### Passo a Passo

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/HaygoNunes/Discord-Bot-Voidzinho
   cd Discord-Bot-Voidzinho
   ```

2. **Crie um ambiente virtual (recomendado):**

   ```bash
   python -m venv venv
   ```

   - **Windows:**  
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**  
     ```bash
     source venv/bin/activate
     ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes linhas:

   ```env
   KEY_DISCORD=sua_chave_discord_aqui
   KEY_LLAMA=sua_chave_huggingface_aqui
   CANAL_ID=id_do_canal_discord_aqui
   ```

5. **Inicie o bot:**

   ```bash
   python voidzinho.py
   ```

---

## Comandos

| Comando   | Descrição                                                      |
|-----------|----------------------------------------------------------------|
| `-ajuda`  | Lista todos os comandos disponíveis.                           |
| `-limpar` | Apaga mensagens do canal. Use `-limpar all` para apagar todas.   |
| `-sorte`  | Gera três jogos únicos da Mega Sena.                             |
| `-dm`     | Inicia uma conversa privada com o bot.                          |
| `-wiki`   | Pesquisa informações na Wikipedia.                              |
| `-dev`    | Cria arquivos de código a partir de uma descrição.              |

---

## Exemplos de Uso

- **Criar um site simples:**

  ```bash
  -dev "Crie um site simples com um título, uma lista de produtos e um estilo CSS básico."
  ```

- **Buscar informações na Wikipedia:**

  ```bash
  -wiki "Inteligência Artificial"
  ```

- **Processar um arquivo PDF:**  
  Anexe um PDF no chat e o bot extrairá o texto para análise.

- **Explicar um arquivo de código:**  
  Anexe um arquivo de código (JavaScript, Python, etc.) e o bot fornecerá uma explicação detalhada.

---

## Licença

Distribuído sob a [MIT License](LICENSE).

---

## Contribuição

Contribuições são bem-vindas! Caso identifique melhorias ou deseje adicionar novas funcionalidades, sinta-se à vontade para abrir issues e enviar pull requests.

---

Desenvolvido por **Haygo Nunes**.
```
