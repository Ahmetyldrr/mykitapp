import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import glob
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
from concurrent import futures

today = dt.datetime.today().strftime('%d_%m_%Y_%H_%M_%S') 

def kitap1000(konu,page=10,bekle=1):
    

        url="https://akis.1000kitap.com/arama?q="+str(konu)+"&bolum=alintilar&sirala=yukselenler&sayfa="+str(page)+"&z=0&us=0&fr=1"
        options = Options()
        options.headless=True
        options.add_argument('user-agent=fake-useragent')
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(url)
        time.sleep(bekle)
        page = driver.page_source
        p = BeautifulSoup(page, 'html.parser')
        sonuc = p.find('html').text
        data=json.loads(sonuc)
        
   
        return data


def kitap1000Fast(konu,page):
    

        url="https://akis.1000kitap.com/arama?q="+str(konu)+"&bolum=alintilar&sirala=yukselenler&sayfa="+str(page)+"&z=0&us=0&fr=1"
        options = Options()
        options.headless=True
        options.add_argument('user-agent=fake-useragent')
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(url)
        time.sleep(bekle)
        page = driver.page_source
        p = BeautifulSoup(page, 'html.parser')
        sonuc = p.find('html').text
        data=json.loads(sonuc)
        
   
        return data

def veriaktarma(datalar,konu):  
      
    soz_list=[]
    sayfalar =  []
    soz_sıra = []
    for sayfa in range(0,len(datalar)):
        for soz in range(0,15):
            try:
                sozler = datalar[sayfa]['gonderiler'][soz]['alt']['sozler']['soz'].strip().replace("¶",'')
                soz_list.append(sozler)
                sayfalar.append(sayfa+1)
                soz_sıra.append(soz+1)
               
            except:
                pass
            
    df = pd.DataFrame(soz_list).reset_index()
    df.columns=['Sıra','Sozler']
    df['Sıra']=df['Sıra']+1
    df['Sayfa']=sayfalar
    df['Soz_Sıra']=soz_sıra

    adı=konu.replace(" ","_")

    #son_df=df.drop_duplicates(subset='Sozler', keep="last")
    # son_df=df[(~df.duplicated()) | (df['Sıra'].isnull())]
    # print("Toplam Benzer {} adet kayıt kaldırıldı".format(len(df)-len(son_df)))
    # print("Toplam {} adet soz excele atılacak".format(len(df)))

    # df_new = pd.DataFrame()
    # for i, row in son_df.iterrows():
    #     df_new = df_new.append(row)
    #     df_new = df_new.append(pd.Series(), ignore_index=True)
    today = dt.datetime.today().strftime('%d_%m_%Y_%H_%M_%S') 
    df.to_excel(adı+'_'+str(today)+'.xlsx',index=False)
    print("Verileriniz {} adında excel klasörüne atıldı".format(adı))
    time.sleep(3)

def birlestirme(konu):

        df_all = pd.DataFrame() 
        adı=konu.replace(" ","_")    
        for file_excel in glob.glob("*.xlsx"):
            df_file = pd.read_excel(file_excel)
            df_all = df_all.append(df_file, ignore_index=True)

        df_all.drop_duplicates(subset ="Sozler", inplace = True)

        df_new = pd.DataFrame()
        for i, row in df_all.iterrows():
            df_new = df_new.append(row)
            df_new = df_new.append(pd.Series(), ignore_index=True)
        df_new .to_excel('Full_Data_'+str(adı)+'.xlsx', index=False)   

if __name__ == "__main__":
    
    print("""1000 Kitap Veri Uygulama""")
    konu = input("Lütfen Bir konu Giriniz:  ")
    bekle = int(input("Veri çekimi bekleme süresi giriniz Örn:3  "))
    verim=kitap1000(konu,1,1) 
    sayfasayi = verim['toplamSayfa']
    iceriksayi=verim['toplamicerik']
    
    print("{} konusu için toplam {} sayfa ve {} içerik bulunmaktadır".format(konu,sayfasayi,iceriksayi))
    
    basla = int(input("Tarama Baslangic Sayfa no Giriniz:  "))
    bitis = int(input("Tarama Bitis Sayfa no Giriniz:  "))  
    print("Toplam Seçtiğiniz {} adet sayfa taranacaktır.".format(bitis-basla))
    flagno = input("Lütfen Flag değeri giriniz.")

    print("""

    "KİTAP APP İŞLEM MENUSU"

    1 - Normal Çekim İşlemi İçin 1 giriniz.
    2 - Hızlı Çekim İşlemi İçin 2 Giriniz.
    3 - İşlemi iptal için 3 Giriniz.


    
    """)


    ans = input("Lütfen Tercihinizi Yapınız.")
    

    if ans=='1':
        print("Toplam Taranacak Sayfa Sayısı {},Lütfen uygun bir sayfa sayısı giriniz.".format(sayfasayi))

        datalar=[]
        say=0
        flag=0

        for i in range(basla,bitis):
           
            say=say+1
            print("Taranacak Son Sayfa {} ,Taranan Sayfa {} ,Yuzde {}".format(bitis,i,round((say/(bitis-basla))*100,2)))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            
            verim=kitap1000(konu,i,bekle)
            datalar.append(verim)
           
            flag=flag+1

            print("Flag Değeri",flag)

            if flag==int(flagno):
                veriaktarma(datalar,konu)
                flag=0
                print("Flag Sıfırlandı",flag)
                datalar=[]

        veriaktarma(datalar,konu)
        print("Son Data Atıldı,Veri Çekim İşlemi Bitti")
        print("Tüm exceller birleştiriliyor")
        birlestirme(konu)
        print("Veriler Klasörde Birleştirildi.")
        print("Program 10 sn sonra kapanıyor.")
        time.sleep(10)
        exit() 

    if ans=='2':

    
        datalar=[]
        say=0
        flag=0
        number_task = input("Kaç paralel işlem çalışsın")
        executor = futures.ThreadPoolExecutor(max_workers=int(number_task))
        task=[]
        for i in range(basla,bitis):
           
            say=say+1

            print("Taranacak Son Sayfa {} ,Taranan Sayfa {} ,Yuzde {}".format(bitis,i,round((say/(bitis-basla))*100,2)))
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            

            d = executor.submit(kitap1000Fast,konu,i)
            task.append(d)

        for future in futures.as_completed(task):
              
                res = future.result()
                datalar.append(res)
            
                flag=flag+1

                print("Flag Değeri",flag)

                if flag==int(flagno):
                    
                    veriaktarma(datalar,konu)
                    flag=0
                    print("Flag Sıfırlandı",flag)
                    datalar=[]


        veriaktarma(datalar,konu)
        print("Son Data Atıldı,Veri Çekim İşlemi Bitti")
        print("Tüm exceller birleştiriliyor")
        birlestirme(konu)
        print("Veriler Klasörde Birleştirildi.")
        print("Program 10 sn sonra kapanıyor.")
        time.sleep(10)
        exit() 



    if ans=='3':
        print('İşlem İptal Edildi')
        time.sleep(3)
        print('Çıkış yapılıyor')
        exit()





