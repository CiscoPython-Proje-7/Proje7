# Lesson Time Tracker

## Lesson Time Tracker Analiz Raporu
### Kısa Özet
Özellikle pandemi sürecinde öğrenci dolaşımını azaltmak için farklı sınıf gruplarına farklı ders ve teneffüs zamanı uygulayabilmek gerekmektedir. Zaman bildirimi için kullanılan mevcut yöntem ders zili uygulamasıdır. Ancak bu yöntem farklı gruplara farklı zamanlarda bildirim vermeye uygun değildir. Bir grup öğrenci derse devam ederken diğer gruba zil ile bildirim göndermek karmaşaya ve ses kirliliğine neden olacaktır. Bu durum da bizi sınıflardaki öğrenciler ve öğretmenin akıllı tahtalarda ders akışını takip edebilecekleri bir araç geliştirme fikrine yönlendirmiştir. Projemizde; öğrencinin ders gördüğü ortamlardaki etkileşimli tahtaların alt kısmında, 50 piksel yüksekliğinde yarı şeffaf bir bar, zaman bildirimi için kullanılacaktır. Bu bar farklı zaman dilimi uygulaması kullanılmadığı durumlarda dahi zaman bildirimi için yeni bir alternatif oluşturacak ve okulda zil kullanımına olan gereksinimi tamamen ortadan kaldıracaktır. Uygulama seçilen sınıfa göre şu an hangi ders veya teneffüs zaman diliminde olduğumuzu, ders veya teneffüs bitimine ne kadar zaman kaldığını takip edebilmemizi sağlayacaktır. Yönetici ve öğretmenlerin okuldaki genel ders akışını izleyebilmeleri için de tüm sınıfların zaman çizelgelerini tek ekranda gösteren bir uygulama geliştirilmiştir. Proje aynı zamanda okul yöneticilerinin sınıf ders programlarını veritabanına kolay bir şekilde girebilmeleri için bir Django web uygulaması içermektedir.
### Problem Tanımı
Pandemi sürecinde öğrenci dolaşımını azaltmak için farklı sınıf gruplarına farklı ders ve teneffüs zamanı uygulayabilmek gerekmektedir. Zaman bildirimi için kullanılan mevcut yöntem ders zili uygulamasıdır. Ancak bu bildirim farklı gruplara farklı zamanlarda bildirim vermeye uygun değildir. Bir grup öğrenci derse devam ederken diğer gruba zil ile bildirim göndermek karmaşaya ve ses kirliliğine neden olacaktır. Bu durum da bizi; "Sınıflardaki öğrenciler ve öğretmenin akıllı tahtalarda ders akışını takip edebilecekleri bir araç geliştirilebilir mi?" sorusunu sormaya sebep olmuş ve bu sorun üzerinde problemin çözüm yolunun bulunması fikrini doğrmuştur.
### Analiz Süreci
Problemin çözümü için proje ekibimizle yaptığımız uzaktan toplantılarda problemin detaylı analizi gerçekleştirldi. Bu toplantılarda her sınıfa etkileşimli tahta bulunması, bu tahtaların genelde öğretmenler odalarında da bulunması, projenin kullanılabilir olduğu görüşünü destekledi. Bu analizler sonucunda, programlama dili olarak Python kullanılmasına, programın görsel tasarımında Python kurulumu ile birlikte geldiği için Tkinter modülünün kulllanılmasına, ses bildirimleri için pygame modülünün kullanılmasına ve günlük ders programının tutulması içinse JSON modülünün kullanılmasına kararına varıldı.
#### 1. İhtiyaç Analizi
Tüm dünyada olduğu gibi ülkemizde de pandemiden dolayı eğitime ara verildi. Bu süreçte eğitim EBA gibi online platformlar üzerinden gerçekleşti. Her ne kadar dünyadaki diğer ülkelerden uzaktan eğitime en hızlı adapte olmuş ülkeler arasında yer alsak da hiç bir eğitim yüz yüze eğitim kadar etkili olamamıştır. Yeni eğitim-öğretim yılında Milli Eğitim Bakanlığımızın birinci önceliği sağlıklı ortamlarda öğrencilerin eğitimine, okullarında ve sınıflarında devam edebilmeleridir. Ancak bu, beraberinde çok fazla riski de içermektedir. Aynı anda derse girmek, aynı anda teneffüs yapmak öğrencilerin birbirleriyle daha çok etkileşime girmeleri ve temas riskinin artması anlamına gelmektedir. Hem eğitimin okullarda yapılması hem de virüs bulaşını en aza indirebilmek için faklı zamanlarda teneffüs uygulamasının uygun olacağı değerlendirilmiş ve bunun için bir programa ihtiyaç duyulmuştur.

 
#### 2. İçerik Analizi 
 Bu proje kapsamında; Eğitim okulda yüz yüze yapılmalı, Öğrenciler derslere şube düzeyinde kademeli olarak  girmeli teneffüslere de kademeli olarak çıkmalı. öğrencilerin teneffüslerde minimum karşılaşmalı, derse giriş ve çıkışlarında karışıklığa sebebiyet vermemek için zil sistemi kullanılmamalı. Sistem Akıllı tahtaları kurulmalı ve ders , teneffüs süreleri akıllı tahtalar üzerinde takip edilmeli.

#### 3. Durum Ortam Analizi
Yazılımı gerçekleştirirken;
 Settings,
 requests,
 json,
 pygame,
 tkinter,
 win32api,
 datetime isimli python kütüphanelerinden faydalanılmıştır.
Yazılımın gerçekleştirilmesi sürecinde kullanılan veriler ve kütüphaneler vb. bilgiler yer almaktadır. 
#### 4. Kullanıcı Analizi 
Bu yazılım Ülkemizde ve tüm dünyadaki resmi ya da özel okullarda görev yapan idarecilerin rahatlıkla kullanabilmeleri için yazılmıştır.

Yazılımı kullanacak olan ya da bu yazılımın paylaşılması durumunda kaynak kod üzerinden faydalanmak isteyecek kullanıcının profiline yönelik bilgiler yer almaktadır.

## Lesson Time Tracker Tasarım Raporu
### Kısa Özet
Projenin Tasarım sürecinde uygulanan süreç adımlarının ifade edildiği bölümdür. 
### Veri Tasarımı
Projede veritabanı kullanıldığı durumda veritabanı diyagramı bu bölüm içerisinde yer almaktadır. 
### Ara yüz Tasarımı
Kullanıcı ara yüzüne ait tasarımların (Mock Up) yer aldığı bölümdür. 
### Kod Tasarımı
Yazılım geliştirme süreci sırasında Nesne Yönelimli Programlama dikkate alınarak (Class Diagram) tasarımlar bu alanda yer almaktadır. 
### Zaman Çizelgesi
Projenin rapor yazım süreçleri de dahil edilerek gerektiğinde iç içe geçmiş süreçlerinde ifade edilebileceği bölümdür. (Gannt Chart)
 
## Lesson Time Tracker Gerçekleştirme Raporu
### Karşılaşılan Sorunlar ve Uygulanan Çözümler
Projenin gerçekleştirme sürecine karşılaşılan sorunlar ve gidermek için uygulanan çözümlerin ifade edildiği bölümler. 
### Proje Bileşenleri ve Görevleri
Programa ait dökümantasyonun taslak halininde ortaya çıktığı bölümdür. 
### Github Yükleme Süreci
Yazılım kaynak kodunun github profilinde paylaşılması farklı bir kullanıcı tarafından başka bir platforma yüklenmesi sürecinde yapılması gerekenlerin yer aldığı bölümdür. 

## Lesson Time Tracker Test Raporu
### Karşılaşılan Sorunlar ve Uygulanan Çözümler
Yazılım projesinin çalıştırılması ve test edilmesi süresince karşılaşılan sorunlar ve uygulanan çözümler yer almaktadır. 
### Test Sürecinde Kullanılan Modüller (Varsa) 
Proje test sürecinde gerektiğinde farklı modüller kullanılarak test çalışması gerçekleştirilmektedir. Proje sürecinde eğer bu modüllerden herhangi birini kullandıysanız. Modülü kullanırken yaptığınız kodlama bu bölümde yer almaktadır. 
 
### Görev dağılımı
#### 1.	Analiz Raporunun Tamamlanması
Yusuf Önder Akyol, Serkan Güner				
#### 2.	Tasarım Raporunun Tamamlanması
Yusuf Önder Akyol, Serkan Güner				
#### 3.	Gerçekleştirim Raporunun Tamamlanması
Yusuf Önder Akyol, Serkan Güner				
#### 4.	Gantt Diagramı
Serdar Asarkaya				
#### 5.	Arayüz tasarımı
Kemal Özlü, Mahmut Atik, Serdar Asarkaya				
#### 6.	Veri Tasarımı-Sınıf Tasarımı
Kemal Özlü, Mahmut Atik, Serdar Asarkaya				
#### 7.	Kullanıcı Yardım Dökümanı
Gökhan Dağlı				
#### 8. Programın Çalıştırılması
Kemal Özlü, Mahmut Atik, Serdar Asarkaya, Serkan Güner, Yusuf Önder Akyol				
#### 9. Yazılım Test Çalışması
Olgun Uğurlu				


