#!/usr/bin/env python
# coding: utf-8


import time, base64, hmac, hashlib, requests, json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# coin type and expected difference value to have alert

coin_list = (("XRP",0.00709219858156023),
("ETH",0.007407407407407408),
("FET",0.035587188612099675),
("ANKR",0.037267080745341574),
("DOGE",0.03703703703703707),
("XTZ",0.03192584963954691),
("ATOM",0.023885710591809713),
("BAT",0.02147426134632958),
("LRC",0.021303792074989274),
("XLM",0.020833333333333353),
("NEO",0.020618556701030976),
("UNI",0.02000000000000008),
("LINK",0.019564250778123512),
("STORJ",0.019364448857993894),
("EOS",0.01931649331352166),
("MKR",0.01838235294117647),
("FTM",0.01780151312861595),
("STX",0.017597888253409605),
("LTC",0.01728553137003834),
("SHIB",0.017038007863695998),
("FIL",0.016574585635359153),
("BTC",0.016295707472178067),
("ENJ",0.016207455429497513),
("GALA",0.014648437500000121),
("GRT",0.013513513513513526),
("DASH",0.0215),
("DOT",0.0215),
("COMP",0.0215),
("UMA",0.03),
("CHZ",0.0215),
("NU",0.0215),
("OMG",0.0215),
("MANA",0.010712372790573122),
("AAVE",0.01766241108881916),
("MATIC",0.009588068181818073),
("AXS",0.009380863039399626),
("ADA",0.008339124391938853),
("SAND",0.0074794315632011705),
("POLY",0.035380073800738013),
("TRX",0.0075),
("SNX",0.0215),
("SOL",0.0085),
("AVAX",0.0071))

#class to get data and calculate differences
class eco_finder:
    
    def __init__(self,firstc, secondc):
        self.firstc = firstc
        self.secondc = secondc
    
    def getting_data(self):
        base = "https://api.btcturk.com"
        method = "/api/v2/ticker?pairSymbol="+str(self.firstc)+"_"+str(self.secondc)
        uri = base+method
        result = requests.get(url=uri)
        result = result.json()
        self.value_ask = result['data'][0]['ask']
        self.value_last = result['data'][0]['bid']


    def calculator(self):
        diff_abs = self.value_ask-self.value_last
        diff_ratio = (self.value_ask-self.value_last)/self.value_ask
        return(round(diff_abs,3), diff_ratio)


#alert sender
def alert_sender(first_cur,second_cur,real_diff):
    mail = smtplib.SMTP("smtp.gmail.com",587)          
    mail.ehlo()
    mail.starttls()
    mail.login("burak.erdol34@gmail.com", "bur1990er")  
    mesaj = MIMEMultipart()

    mesaj["From"] = "burak.erdol34@gmail.com" 
    recipients = ["burakeralert@gmail.com","meltemerdol@gmail.com"]
    mesaj["To"] = ", ".join(recipients)
    
    mesaj["Subject"] = "ECO COIN ALERT ON -" + str(first_cur) + " - " + str(second_cur)

    body = """

        COIN ALERT for """ + str(real_diff) + """ $ 
    
    """

    body_text = MIMEText(body, "plain")  
    mesaj.attach(body_text)
    mail.sendmail(mesaj["From"], recipients, mesaj.as_string())
    print("Mail başarılı bir şekilde gönderildi.")
    mail.close()


eco = eco_finder(coin_list[0][0],'USDT')

def main(first_cur,second_cur,diff):
    eco = eco_finder(first_cur,second_cur)
    eco.getting_data()
    eco.calculator()
    if float(eco.calculator()[1]) > diff :
        alert_sender(first_cur,second_cur,eco.calculator()[0])
    else:
        pass

for x in range(len(coin_list)):
    main(coin_list[x][0],'USDT',coin_list[x][1])


