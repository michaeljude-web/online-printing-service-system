-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 29, 2025 at 05:28 AM
-- Server version: 10.1.28-MariaDB
-- PHP Version: 5.6.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hera_printing`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'admin@gmail.com', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customer_id`, `full_name`, `email`, `password`, `date_created`, `status`) VALUES
(1, 'Myke Tyson', 'mike@gmail.com', 'mike', '2025-05-15 17:12:15', 'Approved'),
(2, 'Juan Delacruz', 'juan@gmail.com', 'juan', '2025-05-26 20:10:11', 'Approved'),
(3, 'Joana Mae', 'joana@gmail.com', 'joana', '2025-05-27 14:08:58', 'Pending'),
(4, 'Ella Cruz', 'ella@gmail.com', 'ella', '2025-05-28 07:33:06', 'Pending');

-- --------------------------------------------------------

--
-- Table structure for table `customer_transaction`
--

CREATE TABLE `customer_transaction` (
  `transaction_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `size` varchar(20) NOT NULL,
  `copies` int(11) NOT NULL,
  `print_type` varchar(20) NOT NULL,
  `transaction_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT 'pending',
  `total` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer_transaction`
--

INSERT INTO `customer_transaction` (`transaction_id`, `customer_id`, `file_path`, `size`, `copies`, `print_type`, `transaction_date`, `status`, `total`) VALUES
(1, 1, 'C:/Users/agard/Downloads/alog12.docx', 'Short', 2, 'colored', '2025-05-27 07:02:15', 'completed', 200),
(3, 1, 'C:/Users/agard/Downloads/GardeMichaelJude-17724-BSIT2-BLK1.pdf', 'Short', 5, 'colored', '2025-05-27 09:36:02', 'completed', 15),
(4, 1, 'C:/Users/agard/Downloads/appdev.pdf', 'Short', 22, 'colored', '2025-05-27 09:37:04', 'completed', 66),
(22, 1, 'C:/Users/agard/Downloads/users - Copy.sql', 'LONG BOND PAPER', 7, 'colored', '2025-05-27 23:38:35', 'completed', 35),
(25, 1, 'C:/Users/agard/Downloads/appdev.pdf', 'LONG BOND PAPER', 6, 'colored', '2025-05-28 02:19:47', 'pending', 30),
(26, 2, 'C:/Users/agard/Downloads/windows-7-official-3840x2160-13944.jpg', 'SHORT BOND PAPER', 9, 'colored', '2025-05-28 06:55:05', 'pending', 27);

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `quantity` decimal(10,2) DEFAULT NULL,
  `unit` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`inventory_id`, `item_name`, `quantity`, `unit`) VALUES
(1, 'Ink', '101.00', 'stock'),
(2, 'A4 Bond Paper', '499.00', 'sheets'),
(4, 'Long Bond Paper', '400.00', 'sheets'),
(5, 'Short Bond Paper', '300.00', 'sheets');

-- --------------------------------------------------------

--
-- Table structure for table `transaction_usage`
--

CREATE TABLE `transaction_usage` (
  `usage_id` int(11) NOT NULL,
  `transaction_id` int(11) NOT NULL,
  `inventory_id` int(11) NOT NULL,
  `used_quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `customer_transaction`
--
ALTER TABLE `customer_transaction`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`inventory_id`);

--
-- Indexes for table `transaction_usage`
--
ALTER TABLE `transaction_usage`
  ADD PRIMARY KEY (`usage_id`),
  ADD KEY `transaction_id` (`transaction_id`),
  ADD KEY `inventory_id` (`inventory_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `customer_transaction`
--
ALTER TABLE `customer_transaction`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `transaction_usage`
--
ALTER TABLE `transaction_usage`
  MODIFY `usage_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customer_transaction`
--
ALTER TABLE `customer_transaction`
  ADD CONSTRAINT `customer_transaction_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`);

--
-- Constraints for table `transaction_usage`
--
ALTER TABLE `transaction_usage`
  ADD CONSTRAINT `transaction_usage_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `customer_transaction` (`transaction_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transaction_usage_ibfk_2` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
