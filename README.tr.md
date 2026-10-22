# DeleteMe

[English](README.md) | **Türkçe**

DeleteMe, yumruğunu sıktığında seni kameradaki görüntüden silen küçük bir OpenCV tabanlı webcam uygulamasıdır.

> Bu proje, Tzur Soffer'ın [TzurSoffer/deleteMe](https://github.com/TzurSoffer/deleteMe) projesinden geliştirilmiştir.
> Bu sürümde eklenenler: sanal kamera çıkışı (Zoom, Meet, Teams, Discord'da kullanılabilir), kamera seçimi, Türkçe/İngilizce arayüz ve çeşitli hata düzeltmeleri.

## Gereksinimler

- Python 3.10+ önerilir
- Webcam
- Kamera erişimi olan Windows, macOS veya Linux

Python paketleri [requirements.txt](requirements.txt) dosyasında listelenmiştir.

## Kurulum

Bir sanal ortam oluşturup etkinleştir, ardından bağımlılıkları kur:

```bash
pip install -r requirements.txt
```

Elle kurmak istersen, proje şu paketlere bağımlıdır:

- opencv-python
- mediapipe
- pyvirtualcam
- pillow
- pygrabber (yalnızca Windows'ta, kameraları adlarıyla listelemek için)

## Çalıştırma

Arayüzü proje klasöründen başlat:

```bash
python main.py
```

Arayüzün sağ üstündeki **Dil / Language** menüsünden Türkçe ve İngilizce arasında geçiş yapabilirsin.

## Kullanım

1. Uygulamayı başlat.
2. "Kamera" listesinden kameranı seç. Uygulamayı açtıktan sonra kamera taktıysan "Yenile" düğmesine tıkla.
3. Kameranın boş bir arka plan gösterdiğinden emin ol.
4. "Arka Planı Yakala" düğmesine tıkla.
5. Canlı önizleme penceresini izle ve geri sayım bitmeden kadrajdan çık.
6. Efekti başlatmak için "Uygulamayı Başlat" düğmesine tıkla.

### Sanal kamera

"Görüntüyü sanal kameraya gönder" seçiliyken, işlenmiş görüntü
[pyvirtualcam](https://github.com/letmaik/pyvirtualcam) aracılığıyla **OBS Virtual Camera**'ya da gönderilir.
Zoom, Google Meet, Teams, Discord vb. uygulamalarda kamera olarak OBS Virtual Camera'yı seç.

- OBS Studio (28+) kurulu olmalıdır; OBS'nin kendi sanal kamerası aynı anda açık olmamalıdır.
- "Kamera" listesi bilgisayarındaki kameraları adlarıyla gösterir. Uygulama görüntüyü OBS Virtual Camera'ya gönderdiği için bu kamera listede yer almaz.

### Kontroller

- Arka plan önizleme penceresinde yakalamayı iptal etmek için `q` veya `Esc` tuşuna bas.
- Ana OpenCV penceresinde döngüden çıkmak için `q` tuşuna bas.

## Dosyalar

- [main.py](main.py) Tkinter arayüzünü, kamera akışını ve Türkçe/İngilizce metinleri içerir.
- [deleteMe.py](deleteMe.py) ana efekt mantığını içerir.
- [utils.py](utils.py) kişi ve el algılama yardımcılarını içerir.
- `bg.jpg`, uygulamanın çalışırken oluşturduğu arka plan görüntüsüdür.

## Notlar

- Uygulama yakalanan arka planı `bg.jpg` dosyasına kaydeder.
- Kamera açılmazsa başka bir uygulamanın kamerayı kullanmadığından emin ol.
- Arka plan yakalaması yanlış görünüyorsa sahneyi tekrar boşaltıp yeniden yakala.

## Lisans

Bu proje MIT lisansı altındadır, ayrıntılar için [LICENSE](LICENSE) dosyasına bak. Resmî olmayan Türkçe çevirisi [LICENSE.tr](LICENSE.tr) dosyasındadır.
