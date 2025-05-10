from tkinter import *
from tkinter import messagebox
import pyodbc

try:
    baglanti = pyodbc.connect('*************************************************')
    baglanti.autocommit = True

except pyodbc.Error as ex:
    print('Bağlantı başarısız.', ex)
root = Tk()
root.title("Giriş Yap")
root.resizable(False, False)
root.geometry("400x400+750+300")


def girisYap():
    kulAdi = str(kulAdiEntry.get())
    sifre = str(sifreEntry.get())


    if baglanti: #eğer başarılı bağlantı oluşursa
        cursor = baglanti.cursor() #sorgularımızı çlaıştıracak olan imlecimizi oluşturuyoruz
        try:
            ogrencisorgu = "select Ogrenci_Adi from Ogrenciler where Ogrenci_Adi = ? and Ogrenci_sifre = ?" # burada parametreli veri girmek için ? işareti kullandık verileri execute sorgusu ile ekleyeceğiz
            cursor.execute(ogrencisorgu, (kulAdi, sifre))
            ogrenciler = cursor.fetchone() #sorguda çıkan ilk sonucu alır

            if ogrenciler:
                root.withdraw()
                komut = "select Ogrenci_ID from Ogrenciler where Ogrenci_Adi = ? and Ogrenci_sifre = ?"
                cursor.execute(komut, (kulAdi, sifre))
                ogrenci = cursor.fetchone()

                if ogrenci:
                    ogrenci_id = ogrenci[0]
                    matsorgu2 = "select Matematik from OgrDevamsizlik where Ogrenci_ID = ?"
                    cursor.execute(matsorgu2, (ogrenci_id))
                    matematik_devamsizlik = cursor.fetchone()
                    matdvm = matematik_devamsizlik[0] if matematik_devamsizlik else "---"  # ternary operator syntaxi: 'True döndürecek değer' if 'durum' else 'False değer'

                    tursorgu2 = "select Turkce from OgrDevamsizlik where Ogrenci_ID = ?"
                    cursor.execute(tursorgu2, (ogrenci_id))
                    turkce_devamsizlik = cursor.fetchone()
                    trdvm = turkce_devamsizlik[0] if turkce_devamsizlik else "---"

                    ingsorgu2 = "select Ingilizce from OgrDevamsizlik where Ogrenci_ID = ?"
                    cursor.execute(ingsorgu2, (ogrenci_id))
                    ingilizce_devamsizlik = cursor.fetchone()
                    ingdvm = ingilizce_devamsizlik[0] if ingilizce_devamsizlik else "---"

                    matsorgu = "select Matematik from OgrNotlar where Ogrenci_ID = ?"
                    cursor.execute(matsorgu, (ogrenci_id))
                    matematik_notu = cursor.fetchone()
                    matnotu = matematik_notu[0] if matematik_notu else "---"

                    tursorgu = "select Turkce from OgrNotlar where Ogrenci_ID = ?"
                    cursor.execute(tursorgu, (ogrenci_id))
                    turkce_notu = cursor.fetchone()
                    trnotu = turkce_notu[0] if turkce_notu else "---"

                    ingsorgu = "select Ingilizce from OgrNotlar where Ogrenci_ID = ?"
                    cursor.execute(ingsorgu, (ogrenci_id))
                    ingilizce_notu = cursor.fetchone()
                    ingnotu = ingilizce_notu[0] if ingilizce_notu else "---"

                    ogrenciPanel = Toplevel(root)
                    ogrenciPanel.title("Öğrenci Bilgileri")
                    ogrenciPanel.geometry("400x400+750+300")
                    ogrenciPanel.resizable(False, False)

                    def geriDonGiris():
                        ogrenciPanel.destroy()
                        root.deiconify()

                    baslikLabel1 = Label(ogrenciPanel, text="Öğrenci Bilgileri", font=("Arial", 24))
                    dersLabel = Label(ogrenciPanel, text="Dersler", font=("Arial", 15))
                    notLabel = Label(ogrenciPanel, text="Notlar", font=("Arial", 15))
                    devamsizlikLabel = Label(ogrenciPanel, text="Devamsızlıklar", font=("Arial", 15))
                    matLabel = Label(ogrenciPanel, text="Matematik", font=("Arial", 10))
                    trLabel = Label(ogrenciPanel, text="Türkçe", font=("Arial", 10))
                    ingLabel = Label(ogrenciPanel, text="İngilizce", font=("Arial", 10))
                    matNot = Label(ogrenciPanel, text=matnotu, font=("Arial", 10))
                    trNot = Label(ogrenciPanel, text=trnotu, font=("Arial", 10))
                    ingNot = Label(ogrenciPanel, text=ingnotu, font=("Arial", 10))
                    matdvms = Label(ogrenciPanel, text=matdvm, font=("Arial", 10))
                    trdvms = Label(ogrenciPanel, text=trdvm, font=("Arial", 10))
                    ingdvms = Label(ogrenciPanel, text=ingdvm, font=("Arial", 10))
                    buttonGeriDon = Button(ogrenciPanel, text="Geri Dön", command=geriDonGiris)

                    matLabel.place(x=45, y=180)
                    trLabel.place(x=45, y=230)
                    ingLabel.place(x=45, y=280)
                    matNot.place(x=200, y=180)
                    trNot.place(x=200, y=230)
                    ingNot.place(x=200, y=280)
                    matdvms.place(x=300, y=180)
                    trdvms.place(x=300, y=230)
                    ingdvms.place(x=300, y=280)

                    buttonGeriDon.place(x=175, y=300)
                    baslikLabel1.place(x=90, y=50)
                    dersLabel.place(x=40, y=120)
                    notLabel.place(x=180, y=120)
                    devamsizlikLabel.place(x=250, y=120)
                    ogrenciPanel.mainloop()
                    return
            ogretmensorgu = "select Ogretmen_Adi from Ogretmenler where Ogretmen_Adi = ? and Ogretmen_sifre = ?"
            cursor.execute(ogretmensorgu, kulAdi, sifre)
            ogretmen = cursor.fetchone()
            if ogretmen:
                root.withdraw()
                def notEkle():
                    guncelsnv = str(sinavGuncelle.get())
                    ogrencinumara = str(ogrNo.get())
                    ders = str(dersEntry.get())

                    # burada not girdiğin zaman tabloda bulunuyosa o tablodaki null değer yerine girmesi için yazdım
                    if guncelsnv == "" or ders == "" or ogrencinumara == "":
                        messagebox.showerror("Hata", "Boş değer giremezsiniz!!")
                    else:
                        try:
                            dersler =["Matematik", "Turkce", "Ingilizce"]
                            if ders not in dersler:
                                messagebox.showerror("Hata", "Geçersiz ders seçimi!")
                                return
                            sorgu = f"""
                            if exists (select 1 from OgrNotlar where Ogrenci_ID = ?)
                                update OgrNotlar
                                set {ders} = ?
                                where Ogrenci_ID = ?
                            else
                                insert into OgrNotlar (Ogrenci_ID, {ders})
                                values (?, ?);
                            """

                            cursor.execute(sorgu, (ogrencinumara, guncelsnv, ogrencinumara, ogrencinumara, guncelsnv))
                            baglanti.commit() #eğer var olan bir öğrenciye farklı değer girerken farklı veri açıp girdiğimiz değeri girmek yerine verisi varsa o
                                              # tabloyu güncelleyecek komutu yaptık ve commit ile yaptığımız değişiklikleri kalıcı halde veritabanında depoladık.

                            messagebox.showinfo("Başarılı", "Not başarıyla eklendi!")
                        except Exception as hata:
                            messagebox.showerror("Hata", f"Bir hata oluştu: {hata}")

                def notGuncelle():
                    guncelsnv = str(sinavGuncelle.get())
                    ogrencinumara = int(ogrNo.get())
                    ders = str(dersEntry.get())
                    baglanti.execute(f"update OgrNotlar set {ders}='{guncelsnv}' where Ogrenci_ID ='{ogrencinumara}'")
                    messagebox.showinfo("Eklendi", "Öğrencinin notu başarıyla güncellendi")

                def devamsizlikYonetme():
                    def dvmEkle():
                        guncelsnv = str(dvmsGuncelle.get())
                        ogrencinumara = str(ogrNo.get())
                        ders = str(derSec.get())
                        if guncelsnv == "" or ogrencinumara == "" or ders == "":
                            messagebox.showerror("Hata", "Boş değer giremezsiniz!!")
                        else:
                            try:
                                dersler2 = ["Matematik", "Turkce", "Ingilizce"]
                                if ders not in dersler2:
                                    messagebox.showerror("Hata", "Geçersiz ders seçimi!")
                                    return
                                sorgu = f"""
                                if exists (select 1 from OgrDevamsizlik where Ogrenci_ID = ?)
                                    update OgrDevamsizlik
                                    set {ders} = ?
                                    where Ogrenci_ID = ?
                                else
                                    insert into OgrDevamsizlik (Ogrenci_ID, {ders})
                                    values (?, ?);
                                """

                                cursor.execute(sorgu,
                                               (ogrencinumara, guncelsnv, ogrencinumara, ogrencinumara, guncelsnv))
                                baglanti.commit()

                                messagebox.showinfo("Devamsızlık", "Devamsızlık başarıyla eklendi!")
                            except Exception as hata:
                                messagebox.showerror("Hata", f"Bir hata oluştu: {hata}")

                    def dvmGuncelle():
                        gunceldvm = str(dvmsGuncelle.get())
                        ogrencinumara = int(ogrNo.get())
                        ders = str(derSec.get())
                        baglanti.execute(
                            f"update OgrDevamsizlik set {ders}='{gunceldvm}' where Ogrenci_ID ='{ogrencinumara}'")
                        messagebox.showinfo("Devamsızlık", "Öğrencinin devamsızlığı başarıyla güncellendi")

                    dvmhoca = Toplevel(root)
                    dvmhoca.title("Öğretmen Paneli")
                    dvmhoca.geometry("400x400+750+300")
                    baslikLabel1 = Label(dvmhoca, text="Öğretmen Paneli", font=("Arial", 24))
                    ogrNo = Entry(dvmhoca, width=20, bg="white", fg="black")
                    dvmsGuncelle = Entry(dvmhoca, width=20, bg="white", fg="black")
                    noGirLabel = Label(dvmhoca, text="Öğrenci No")
                    dmvsLabel = Label(dvmhoca, text="Devamsızlık")
                    dersSecLabel = Label(dvmhoca, text="Ders Seçiniz")
                    buttonEkle = Button(dvmhoca, text="Devamsızlık Ekle", command=dvmEkle)
                    buttonGuncelle = Button(dvmhoca, text="Devamsızlık Güncelle", command=dvmGuncelle)

                    derSec = Entry(dvmhoca, width=20, bg="white", fg="black")

                    noGirLabel.place(x=90, y=150)
                    dmvsLabel.place(x=90, y=190)
                    dersSecLabel.place(x=90, y=230)
                    ogrNo.place(x=170, y=150)
                    dvmsGuncelle.place(x=170, y=190)
                    baslikLabel1.place(x=80, y=50)
                    derSec.place(x=170, y=230)
                    buttonEkle.place(x=270, y=300)
                    buttonGuncelle.place(x=40, y=300)
                    dvmhoca.mainloop()

                hocaPanel = Toplevel(root)
                hocaPanel.title("Öğretmen Paneli")
                hocaPanel.geometry("400x400+750+300")
                hocaPanel.resizable(False, False)

                def geriDonGiris():
                    hocaPanel.destroy()
                    root.deiconify()

                baslikLabel1 = Label(hocaPanel, text="Öğretmen Paneli", font=("Arial", 24))

                ogrNo = Entry(hocaPanel, width=20, bg="white", fg="black")
                sinavGuncelle = Entry(hocaPanel, width=20, bg="white", fg="black")
                noGirLabel = Label(hocaPanel, text="Öğrenci No")
                notGirLabel = Label(hocaPanel, text="Not")
                dersSecLabel = Label(hocaPanel, text="Ders Seçiniz")
                buttonEkle = Button(hocaPanel, text="Not Ekle", command=notEkle)
                buttonGuncelle = Button(hocaPanel, text="Not Güncelle", command=notGuncelle)
                devamsizlikEkle = Button(hocaPanel, text="Devamsızlık Yönet", command=devamsizlikYonetme)
                buttonGeriDon = Button(hocaPanel, text="Geri Dön", command=geriDonGiris)
                dersEntry = Entry(hocaPanel, width=20, bg="white", fg="black")

                noGirLabel.place(x=90, y=150)
                notGirLabel.place(x=90, y=190)
                dersSecLabel.place(x=90, y=230)
                ogrNo.place(x=170, y=150)
                sinavGuncelle.place(x=170, y=190)
                baslikLabel1.place(x=80, y=50)
                dersEntry.place(x=170, y=230)
                buttonEkle.place(x=270, y=300)
                buttonGuncelle.place(x=40, y=300)
                devamsizlikEkle.place(x=145, y=300)
                buttonGeriDon.place(x=175, y=350)
                hocaPanel.mainloop()
                return

            if kulAdi.lower() == "admin" and sifre == "123":
                root.withdraw()

                def hocaEkle():
                    isim = str(kulAdiKayitOgr.get())
                    no = str(ogrNoKayit.get())
                    sifre = str(sifreKayitOgr.get())
                    if isim == "" or no == 0 or sifre == "":
                        messagebox.showerror("Hata", "Boş değer giremezsiniz!!")
                    else:
                        baglanti.autocommit = True
                        baglanti.execute(f"insert into Ogretmenler values({no},'{isim}','{sifre}')")
                        messagebox.showinfo("Eklendi", "Öğretmen Eklendi.")

                def ogrenciEkle():
                    isim = str(kulAdiKayitOgr.get())
                    no = str(ogrNoKayit.get())
                    sifre = str(sifreKayitOgr.get())
                    if isim == "" or no == "" or sifre == "":
                        messagebox.showerror("Hata", "Boş değer giremezsiniz!!")
                    else:
                        baglanti.autocommit = True
                        baglanti.execute(
                            f"insert into Ogrenciler(Ogrenci_ID,Ogrenci_Adi,Ogrenci_sifre) values({no},'{isim}','{sifre}')")
                        messagebox.showinfo("Eklendi", "Öğrenci Eklendi.")

                def ogrenciSil():
                    cevap = messagebox.askquestion("Dikkat!",
                                                   "Silme işlemi yapmak üzeresiniz. Bu işlem geri çevirilemez. Onaylıyormusunuz?")
                    if cevap == "yes":
                        isim = str(kulAdiKayitOgr.get())
                        no = int(ogrNoKayit.get())
                        sifre = str(sifreKayitOgr.get())
                        baglanti.autocommit = True
                        baglanti.execute(f"delete from Ogrenciler where Ogrenci_ID={no}")
                        messagebox.showinfo("Başarılı", "Öğrenci silindi.")
                    elif cevap == "no":
                        messagebox.showinfo("Iptal", "Silme işlemi iptal edildi.")

                def hocaSil():
                    cevap = messagebox.askquestion("Dikkat!",
                                                   "Silme işlemi yapmak üzeresiniz. Bu işlem geri çevirilemez. Onaylıyormusunuz?")
                    if cevap == "yes":

                        no = int(ogrNoKayit.get())

                        baglanti.autocommit = True
                        baglanti.execute(f"delete from Ogretmenler where Ogretmen_ID={no}")
                        messagebox.showinfo("Başarılı", "Öğretmen silindi.")
                    elif cevap == "no":
                        messagebox.showinfo("Iptal", "Silme işlemi iptal edildi.")

                def geriDonGiris():
                    adminPanel.destroy()
                    root.deiconify()

                adminPanel = Toplevel(root)
                adminPanel.title("Admin Paneli")
                adminPanel.geometry("400x400+750+300")
                adminPanel.resizable(False, False)
                baslik1Label = Label(adminPanel, text="Admin Paneli", font=("Arial", 24))
                isimLabel = Label(adminPanel, text="İsim")
                numaraLabel = Label(adminPanel, text="Numara")
                sifreLabel1 = Label(adminPanel, text="Sifre")
                buttonHoca = Button(adminPanel, text="Öğretmen Ekleyin", command=hocaEkle)
                buttonOgrenci = Button(adminPanel, text="Öğenci Ekleyin", command=ogrenciEkle)
                buttonOgrSilme = Button(adminPanel, text="Öğenci Silin", command=ogrenciSil)
                buttonHocaSilme = Button(adminPanel, text="Öğretmen Silin", command=hocaSil)

                buttonGeriDon = Button(adminPanel, text="Geri Dön", command=geriDonGiris)

                kulAdiKayitOgr = Entry(adminPanel, width=20, bg="white", fg="black")
                ogrNoKayit = Entry(adminPanel, width=20, bg="white", fg="black")
                sifreKayitOgr = Entry(adminPanel, width=20, bg="white", fg="black")

                isimLabel.place(x=90, y=150)
                numaraLabel.place(x=90, y=250)
                sifreLabel1.place(x=90, y=200)
                kulAdiKayitOgr.place(x=140, y=150)
                sifreKayitOgr.place(x=140, y=200)
                ogrNoKayit.place(x=140, y=250)
                buttonOgrenci.place(x=270, y=300)
                buttonHoca.place(x=40, y=300)
                buttonHoca.place(x=40, y=300)
                baslik1Label.place(x=100, y=50)
                buttonHocaSilme.place(x=50, y=340)
                buttonOgrSilme.place(x=280, y=340)
                buttonGeriDon.place(x=175, y=300)

                adminPanel.mainloop()
                return

            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")
        except Exception as exp:
            messagebox.showerror("Hata", f"Bilinmeyen bir hata oluştu hata: {exp}")


baslikLabel = Label(text="LilBoard Giriş", font=("Arial", 24))
kulAdiLabel = Label(text="Kullanıcı Adı", font=("Arial", 10))
sifreLabel = Label(text="Şifre", font=("Arial", 10))
kulAdiEntry = Entry(root, width=20, bg="white", fg="black")
sifreEntry = Entry(root, width=20, bg="white", fg="black", show="*")
buttonGiris = Button(root, text="Giriş Yap", command=girisYap)

# -----------------------------------------------------------------------------------------------------------------

baslikLabel.place(x=110, y=50)
kulAdiLabel.place(x=60, y=130)
sifreLabel.place(x=90, y=190)
kulAdiEntry.place(x=140, y=130)
sifreEntry.place(x=140, y=190)
buttonGiris.place(x=170, y=270)

root.mainloop()


