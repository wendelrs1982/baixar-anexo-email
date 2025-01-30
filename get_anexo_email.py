import imaplib
import email
import os
from datetime import datetime
import config

# Configurações de conexão com o servidor IMAP
imap_host = config.imap_host
imap_user = config.imap_user
imap_pass = config.imap_pass

# Cria a pasta onde será armazenado o anexo caso a pasta ainda não exista
DOWNLOAD_FOLDER = config.anexo
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Título do Email
remetente_email = config.remetente_email

# Data de início da busca
data_inicio = config.data_inicio

# Conexão com o servidor IMAP do Gmail
mail = imaplib.IMAP4_SSL(imap_host)
mail.login(imap_user, imap_pass)

# Selecionando a caixa de entrada
mail.select('inbox')

# Buscando os e-mails na caixa de entrada com um título específico e pela data mais recente
status, data = mail.search(None, f'(FROM "{remetente_email}" SINCE "{data_inicio}")')

# Verifica se a data não está vazio
if data and data[0]:
    # Pegando o ID do e-mail mais recente 
    latest_email_id = data[0].split()[-1]  
    print(f"Último e-mail encontrado: {latest_email_id}")
else:
    print("Nenhum e-mail encontrado.")
    latest_email_id = None

# Obtendo os dados do e-mail mais recente
status, data = mail.fetch(latest_email_id, '(RFC822)')
raw_email = data[0][1]
msg = email.message_from_bytes(raw_email)

# Verificando se o e-mail possui anexos
if msg.get_content_maintype() == 'multipart':
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        
        # Salvando o anexo em um arquivo local
        filename = part.get_filename()
        if filename:
            # Diretório onde os anexos serão salvos
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)  
            if not os.path.isfile(filepath):
                fp = open(filepath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                print(f'O anexo "{filename}" foi salvo com sucesso!')

# Fechando a conexão com o servidor IMAP
mail.close()
mail.logout()