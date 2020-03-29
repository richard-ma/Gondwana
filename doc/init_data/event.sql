-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: 2020-03-28 20:05:05
-- 服务器版本： 5.7.29-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Gondwana`
--

--
-- 转存表中的数据 `event`
--

INSERT INTO `event` (`id`, `name`) VALUES
(1, '缺货'),
(2, '重发'),
(3, '调货'),
(4, '换货'),
(5, '调货超时'),
(6, '等待客服处理'),
(7, '客服询问/答复'),
(8, '客服处理中'),
(9, '物流处理中'),
(10, '等待退款'),
(11, '派送问题件'),
(12, '已完结'),
(13, '未发货');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
