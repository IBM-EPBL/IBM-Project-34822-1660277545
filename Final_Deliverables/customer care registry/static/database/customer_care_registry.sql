-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 19, 2022 at 12:03 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `customer_care_registry`
--

-- --------------------------------------------------------

--
-- Table structure for table `cc_agent`
--

CREATE TABLE `cc_agent` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `problem_type` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `photo` varchar(100) NOT NULL,
  `create_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_agent`
--

INSERT INTO `cc_agent` (`id`, `name`, `address`, `mobile`, `email`, `problem_type`, `uname`, `pass`, `photo`, `create_date`) VALUES
(1, 'Suresh', '85, Chennai', 8863122491, 'suresh381@gmai.com', 'Inability to Access UI', 'AG1', '3507', '', '11-10-2022'),
(2, 'Ram', '33,Madurai', 7328946125, 'ram161@gmail.com', 'Data Storage Problem', 'AG2', '12345', 'A2testimonial-2.jpg', '11-10-2022'),
(3, 'Vinay', '456, Madurai', 8879644325, 'vinay254@gmail.com', 'Data Storage Problem', 'AG3', '8096', '', '12-10-2022'),
(4, 'Sherin', '51, Chennai', 7835846127, 'sherin1a@gmail.com', 'Security Problem', 'AG4', '1478', '', '12-10-2022'),
(5, 'Roshini', '34,Tanjore', 6396375219, 'roshini44@gmail.com', 'Time Limitations', 'AG5', '4913', '', '12-10-2022'),
(6, 'Arjun', '5/101,ST Colony, Chennai', 8974155267, 'arjun23@gmail.com', 'Security Problem', 'AG6', '8526', '', '12-10-2022'),
(7, 'Rajan', '45, GR Road, Trichy', 9856475124, 'raja32@gmail.com', 'Inability to Access UI', 'AG7', '1535', '', '12-10-2022'),
(8, 'Shalini', '56, Karur', 8856741245, 'shalini401@gmail.com', 'Time Limitations', 'AG8', '4709', '', '12-10-2022'),
(9, 'Rishi', '3/45, NSB Road, Trichy', 7856943255, 'rishi181@gmail.com', 'Design/Loading Problem', 'AG9', '1156', '', '12-10-2022'),
(10, 'Sundar', '7/68, Anna Nagar, Chennai', 8891233467, 'sundar110@gmail.com', 'Execution Speed', 'AG10', '5541', '', '12-10-2022'),
(11, 'Meena', '31, Erode', 7856941235, 'meena22@gmail.com', 'Features Required', 'AG11', '6566', '', '12-10-2022');

-- --------------------------------------------------------

--
-- Table structure for table `cc_customer`
--

CREATE TABLE `cc_customer` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `photo` varchar(100) NOT NULL,
  `create_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_customer`
--

INSERT INTO `cc_customer` (`id`, `name`, `address`, `mobile`, `email`, `uname`, `pass`, `photo`, `create_date`) VALUES
(1, 'Dharun', '38,Salem', 9637891594, 'dharun145@gmail.com', 'dharun', '12345', 'C1staff-4.jpg', '10-10-2022'),
(2, 'Vijay', '11, Covai', 8879611425, 'vijay312@gmail.com', 'vijay', '12345', '', '12-10-2022'),
(3, 'Aravindh', '41/3, Trichy', 8897432012, 'aravindh25@gmail.com', 'aravindh', '12345', '', '12-10-2022'),
(4, 'Maha', '33,Chennai', 9638527415, 'maha@gmail.com', 'maha', '12345', 'C4tm-1.jpg', '18-10-2022');

-- --------------------------------------------------------

--
-- Table structure for table `cc_feedback`
--

CREATE TABLE `cc_feedback` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `details` varchar(100) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_feedback`
--

INSERT INTO `cc_feedback` (`id`, `uname`, `details`, `rdate`) VALUES
(1, 'dharun', 'good service', '13-10-2022');

-- --------------------------------------------------------

--
-- Table structure for table `cc_login`
--

CREATE TABLE `cc_login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_login`
--

INSERT INTO `cc_login` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `cc_reply`
--

CREATE TABLE `cc_reply` (
  `id` int(11) NOT NULL,
  `agent` varchar(20) NOT NULL,
  `tid` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `reply` varchar(200) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_reply`
--

INSERT INTO `cc_reply` (`id`, `agent`, `tid`, `status`, `reply`, `date_time`) VALUES
(1, 'AG2', 1, 1, 'bug will be solved', '2022-10-13 16:23:24'),
(2, 'AG2', 1, 2, 'bug solved', '2022-10-13 16:53:29'),
(3, 'AG2', 1, 2, 'bug solved', '2022-10-13 16:58:45'),
(4, 'AG2', 1, 2, 'solved', '2022-10-13 17:07:38'),
(5, 'AG2', 1, 2, 'solved', '2022-10-13 17:15:07'),
(6, 'AG2', 1, 2, 'solved', '2022-10-13 17:33:48'),
(7, 'AG2', 1, 2, 'solved', '2022-10-13 17:35:10'),
(8, 'AG2', 1, 2, 'solved', '2022-10-13 17:36:08'),
(9, 'AG2', 1, 2, 'solved', '2022-10-13 17:37:28'),
(10, 'AG2', 1, 2, 'solved', '2022-10-13 17:38:51'),
(11, 'AG2', 1, 2, 'solved', '2022-10-13 17:58:04'),
(12, 'AG2', 1, 2, 'solved', '2022-10-13 17:59:17'),
(13, 'AG2', 1, 2, 'solved', '2022-10-13 18:10:16'),
(14, 'AG2', 1, 2, 'ss', '2022-10-13 18:14:20'),
(15, 'AG2', 4, 2, 'test', '2022-10-14 19:43:28'),
(16, 'AG2', 1, 2, 'test', '2022-10-14 19:43:57'),
(17, 'AG2', 1, 2, 'test', '2022-10-14 19:47:10'),
(18, 'AG2', 1, 2, 'solved', '2022-10-15 11:12:47'),
(19, 'AG9', 6, 1, 'checking', '2022-10-18 11:29:59');

-- --------------------------------------------------------

--
-- Table structure for table `cc_token`
--

CREATE TABLE `cc_token` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `sw_name` varchar(100) NOT NULL,
  `sw_link` varchar(100) NOT NULL,
  `problem_type` varchar(30) NOT NULL,
  `details` varchar(200) NOT NULL,
  `agent` varchar(20) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cc_token`
--

INSERT INTO `cc_token` (`id`, `uname`, `sw_name`, `sw_link`, `problem_type`, `details`, `agent`, `rdate`, `status`, `date_time`) VALUES
(1, 'dharun', 'Unable to pay for an app?', 'snapdeal.com', 'Data Storage Problem', 'Data has store or not, blank view', 'AG2', '12-10-2022', 2, '2022-10-13 16:53:29'),
(2, 'aravindh', 'Possible to connect external camera?', 'clipchamp.com', 'Features Required', 'Because i don''t have inbuild camera', 'AG11', '12-10-2022', 0, '2022-10-12 18:56:58'),
(3, 'aravindh', 'Latest update not completed', 'phonepe.com', 'Time Limitations', 'phonepe app not update', 'AG5', '12-10-2022', 0, '2022-10-12 18:58:57'),
(4, 'aravindh', 'Edited image has not stored', 'photopea.com', 'Data Storage Problem', 'Image editing in photopea', 'AG2', '12-10-2022', 2, '2022-10-14 19:43:28'),
(5, 'dharun', 'Latest update not completed', 'phonepe.com', 'Time Limitations', 'time expired without updating ', 'AG8', '17-10-2022', 0, '2022-10-17 17:09:28'),
(6, 'maha', 'Unable to pay for an app?', 'snapdeal.com', 'Design/Loading Problem', 'loading problem', 'AG9', '18-10-2022', 1, '2022-10-18 11:29:58');
