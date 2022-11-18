-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 18 Kas 2022, 11:59:10
-- Sunucu sürümü: 10.4.25-MariaDB
-- PHP Sürümü: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `blog`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `email` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `username` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `password` text COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `username`, `password`) VALUES
(1, 'Arzu Kardoğan', 'arzuelmas508@hotmail.com', 'arzum', '$5$rounds=535000$yjgP.gAVzmMa920M$LIrFutYA80Z0ypDjHRptEoyevnYKZQDwe39NXLMcfh2');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `yemekkategori`
--

CREATE TABLE `yemekkategori` (
  `id` int(11) NOT NULL,
  `kategori_adi` text COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `yemekkategori`
--

INSERT INTO `yemekkategori` (`id`, `kategori_adi`) VALUES
(1, 'Etli Yemekler'),
(2, 'Tavuklu Yemekler'),
(3, 'Kahvaltılık Tarifler'),
(4, 'Tatlılar ve Kekler'),
(5, 'Mezeler');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `yemektarifi`
--

CREATE TABLE `yemektarifi` (
  `id` int(11) NOT NULL,
  `yemek_adi` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `tarifi_yazan` text COLLATE utf8mb4_turkish_ci NOT NULL,
  `upload_time` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `kategori_id` int(11) DEFAULT NULL,
  `tarif` text COLLATE utf8mb4_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Tablo döküm verisi `yemektarifi`
--

INSERT INTO `yemektarifi` (`id`, `yemek_adi`, `tarifi_yazan`, `upload_time`, `kategori_id`, `tarif`) VALUES
(1, 'Omlet', 'arzum', '2022-11-18 10:52:09', 3, '<ul>\r\n	<li>4 adet yumurta</li>\r\n	<li>terayağı</li>\r\n	<li>tereyağını tavada kızdırdıktan sonra yumurtaları i&ccedil;erisine kırıyoruz</li>\r\n	<li>ve sıcak olarak servis ediyoruz</li>\r\n</ul>\r\n'),
(3, 'etli ekmek', 'arzum', '2022-11-18 10:52:09', 1, '<ul>\r\n	<li>un</li>\r\n	<li>tuz</li>\r\n	<li>su</li>\r\n	<li>maya</li>\r\n</ul>\r\n'),
(4, 'ekmek tatlısı', 'arzum', '2022-11-18 10:52:09', 4, '<p>ekmek</p>\r\n\r\n<p>şeker</p>\r\n'),
(5, 'börek', 'arzum', '2022-11-18 10:52:09', 3, '<p>yufka</p>\r\n'),
(6, 'humus', 'arzum', '2022-11-18 10:52:09', 5, '<ul>\r\n	<li>tahin</li>\r\n	<li>nohut</li>\r\n	<li>&nbsp;</li>\r\n</ul>\r\n');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `yemekkategori`
--
ALTER TABLE `yemekkategori`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `yemektarifi`
--
ALTER TABLE `yemektarifi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kategori_id` (`kategori_id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `yemekkategori`
--
ALTER TABLE `yemekkategori`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Tablo için AUTO_INCREMENT değeri `yemektarifi`
--
ALTER TABLE `yemektarifi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `yemektarifi`
--
ALTER TABLE `yemektarifi`
  ADD CONSTRAINT `yemektarifi_ibfk_1` FOREIGN KEY (`kategori_id`) REFERENCES `yemekkategori` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
