import logging
import logging.handlers
from datetime import datetime

if __name__ == "__main__":
    print(f"Running script at {datetime.now()}")

    notiFromaddr = "letter.wettbewerbsanalyseWS21@gmx.de"
    notiToaddr = ["Fabian.Wallisch@Student.Reutlingen-University.de", 
                    "Lasse.Bieber@Student.Reutlingen-University.de",
                    "Daniel.Kipp@Student.Reutlingen-University.de",
                    "Jonas.Wagenknecht@Student.Reutlingen-University.de",
                    "Max.Gress@Student.Reutlingen-University.de"]
    notiSubj = "Management Cockpit Scraper error!"
    notiCredentials = ("letter.wettbewerbsanalyseWS21@gmx.de", "An@lyseWS21")

    smtp_handler = logging.handlers.SMTPHandler(mailhost=("mail.gmx.net", 587),
                                            fromaddr=notiFromaddr, 
                                            toaddrs=notiToaddr,
                                            subject=notiSubj,
                                            credentials=notiCredentials,
                                            secure=())

    logger = logging.getLogger()
    logger.addHandler(smtp_handler)

    try:
        raise Exception('Test exception. No action required.')
    except Exception as e:
        logger.exception('Unhandled Exception')