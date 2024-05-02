import imaplib
import email
import os
from datetime import datetime

# Configurações de conexão com o servidor IMAP
imap_host = 'imap.gmail.com'
imap_user = 'seu_email@gmail.com'
imap_pass = 'sua_senha'

# Conexão com o servidor IMAP do Gmail
mail = imaplib.IMAP4_SSL(imap_host)
mail.login(imap_user, imap_pass)

# Selecionando a caixa de entrada
mail.select('inbox')

# Buscando os e-mails na caixa de entrada com um título específico e pela data mais recente
status, data = mail.search(None, '(SUBJECT "TÍTULO_DO_EMAIL")', 'SINCE "01-May-2024"')

# Pegando o ID do e-mail mais recente
latest_email_id = data[0].split()[-1]

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
            filepath = os.path.join('downloads', filename)  # Diretório onde os anexos serão salvos
            if not os.path.isfile(filepath):
                fp = open(filepath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                print(f'Anexo "{filename}" salvo com sucesso!')

# Fechando a conexão com o servidor IMAP
mail.close()
mail.logout()