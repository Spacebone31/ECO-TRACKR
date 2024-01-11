-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 11, 2024 at 09:15 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pollution`
--

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `event_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `severityLevel` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `source_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`event_id`, `date`, `severityLevel`, `description`, `source_id`) VALUES
(15, '2023-01-01', 'High', 'Industrial activity', 16),
(18, '2023-02-15', 'Moderate', 'Chemical spill', 17),
(19, '2023-03-10', 'Low', 'City Traffic', 18),
(20, '2023-04-20', 'High', 'Factory emissions', 19),
(21, '2023-05-05', 'Severe', 'Oil tanker accident', 20);

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `location_id` int(11) NOT NULL,
  `country` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `source_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`location_id`, `country`, `city`, `source_id`) VALUES
(17, 'USA', 'New York', 16),
(20, 'Canada', 'Toronto', 17),
(21, 'UK', 'London', 18),
(22, 'Germany', 'Berlin', 19),
(23, 'Australia', 'Sydney', 20);

-- --------------------------------------------------------

--
-- Table structure for table `mitigationstrategy`
--

CREATE TABLE `mitigationstrategy` (
  `strategy_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `effectiveness` varchar(255) NOT NULL,
  `event_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mitigationstrategy`
--

INSERT INTO `mitigationstrategy` (`strategy_id`, `name`, `description`, `effectiveness`, `event_id`) VALUES
(16, 'Air Purification', 'Improved air quality', 'Medium', 15),
(19, 'Water Filtration', 'Reduced water contamination', 'High', 18),
(20, 'Noise Barriers', 'Reduced noise levels', 'Low', 19),
(21, 'Greenery Planting', 'Improved air quality', 'Medium', 20),
(22, 'Containment Booms', 'Minimized environmental impact', 'High', 21);

-- --------------------------------------------------------

--
-- Table structure for table `source`
--

CREATE TABLE `source` (
  `source_id` int(11) NOT NULL,
  `pollutionType` varchar(255) NOT NULL,
  `pollutantName` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `source`
--

INSERT INTO `source` (`source_id`, `pollutionType`, `pollutantName`, `description`, `user_id`) VALUES
(16, 'Air Pollution', 'CO2', 'High levels of carbon dioxide emissions', 2),
(17, 'Water Pollution', 'Mercury', 'Contaminated water sources', 3),
(18, 'Noise Pollution', 'Traffic noise', 'Excessive traffic noise', 4),
(19, 'Air Pollution', 'Sulfur Dioxide', 'Industrial emissions', 4),
(20, 'Water Pollution', 'Oil Spill', 'Marine oil spill', 2);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fullName` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `fullName`, `email`) VALUES
(1, 'test', 'test', 'test', 'test@mail.co.id'),
(2, 'john', '123', 'john doe', 'johndoe@gmail.com'),
(3, 'Jane', '123', 'Jane Smith', 'janeS@mail.com'),
(4, 'Space', '123', 'Spacebone', 'space_bone@yahoo.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`event_id`),
  ADD KEY `source_id` (`source_id`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`location_id`),
  ADD KEY `source_id` (`source_id`);

--
-- Indexes for table `mitigationstrategy`
--
ALTER TABLE `mitigationstrategy`
  ADD PRIMARY KEY (`strategy_id`),
  ADD KEY `event_id` (`event_id`);

--
-- Indexes for table `source`
--
ALTER TABLE `source`
  ADD PRIMARY KEY (`source_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `mitigationstrategy`
--
ALTER TABLE `mitigationstrategy`
  MODIFY `strategy_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `source`
--
ALTER TABLE `source`
  MODIFY `source_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_1` FOREIGN KEY (`source_id`) REFERENCES `source` (`source_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `location`
--
ALTER TABLE `location`
  ADD CONSTRAINT `location_ibfk_1` FOREIGN KEY (`source_id`) REFERENCES `source` (`source_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `mitigationstrategy`
--
ALTER TABLE `mitigationstrategy`
  ADD CONSTRAINT `mitigationstrategy_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `source`
--
ALTER TABLE `source`
  ADD CONSTRAINT `source_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
