# Daily Activity Report — versão portátil para Windows

**Idioma:** **Português** · [Русский](README-RU.md) · [English](README-EN.md)

Uma aplicação autónoma para Windows 10/11 destinada ao registo diário do trabalho e à preparação de relatórios em português europeu. Basta descarregar um ficheiro executável, colocá-lo numa pasta com permissões de escrita e abri-lo. Não é necessário instalar Python, PostgreSQL ou qualquer instalador adicional.

## Descarregar

[Descarregar `DailyReport.exe`](https://github.com/sergeMMikh/daily_report_4_ua/raw/refs/heads/main-win/dist/DailyReport.exe)

O Windows SmartScreen poderá apresentar um aviso porque o executável não está assinado digitalmente. Consulte o código-fonte do repositório antes de o executar. Se confiar neste projeto, selecione **Executar mesmo assim** na janela do SmartScreen.

## Funcionalidades

- interface local em português, russo e inglês;
- português selecionado por predefinição;
- registo de relatórios com data e hora;
- ordenação cronológica dos relatórios guardados;
- exportação para Excel dos últimos sete dias, do mês atual ou de um ano selecionado;
- armazenamento local em ficheiros JSON UTF-8;
- sem base de dados externa e sem instalação do Python;
- acesso exclusivamente local em `http://127.0.0.1:8765`.

## Primeira utilização

1. Descarregue `DailyReport.exe`.
2. Coloque-o numa pasta com permissões de escrita, por exemplo `Documentos\DailyReport`.
3. Abra o executável.
4. A aplicação será aberta no navegador predefinido em `http://127.0.0.1:8765`.

A aplicação cria automaticamente dois ficheiros junto ao executável:

- `config.json` — definições da aplicação e idioma selecionado para a interface;
- `reports.json` — relatórios guardados.

Não coloque o executável em `Program Files`, pois a aplicação precisa de criar e atualizar estes ficheiros na mesma pasta.

## Dados e cópias de segurança

Todos os relatórios são guardados no ficheiro `reports.json`, junto ao executável. Para criar uma cópia de segurança ou transferir os dados, feche a aplicação e copie `reports.json` juntamente com o executável. O ficheiro utiliza JSON UTF-8 legível.

## Compilar a partir do código-fonte

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-build.txt
.\build.ps1
```

O executável será criado em `dist\DailyReport.exe`.

## Testes

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Para uma instalação partilhada num servidor, com armazenamento centralizado e administração, consulte a edição [`main-python`](https://github.com/sergeMMikh/daily_report_4_ua/tree/main-python).
