# Realizar Download de Anexo

A função desse código é realizar o download do anexo contido em um email que foi enviado por um remetente específico.

## Requisitos

- imaplib
- email
- os
- datetime

## Instalação

1. Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

2. Execute o comando abaixo para criar o arquivo de configuração:
```bash
cp config-example.py config.py
```

3. Acesse o arquivo `config.py` e informe os parâmetros necessários.

## Uso

1. Execute o script `get_anexo_email.py`:
```bash
python get_anexo_email.py
```