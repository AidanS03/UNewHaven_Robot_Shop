-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: robotStore
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,3,1,9999.00,9999.00),(2,2,6,3,59.95,179.85),(3,2,17,1,600.00,600.00),(5,3,7,5,14999.00,74995.00),(6,4,16,2,12000.00,24000.00),(7,4,6,3,59.95,179.85);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
  `total` decimal(12,2) NOT NULL DEFAULT '0.00',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,2,'pending',10633.94,'2025-12-11 14:17:41','2025-12-11 14:37:46'),(2,2,'pending',13591.37,'2025-12-11 14:24:52','2025-12-11 14:37:46'),(3,4,'complete',79757.18,'2025-12-11 14:33:04','2025-12-11 15:05:17'),(4,4,'pending',25715.27,'2025-12-11 15:08:09','2025-12-11 15:08:09');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `unit_price` decimal(10,2) NOT NULL,
  `stock` int NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (3,'Tenacity','This competition‑proven Mars rover is our best design yet, earning 13th place at the 2025 University Rover Challenge. Built on a compact tracked chassis for maximum traction on loose regolith and steep slopes, the platform is engineered around its standout feature: a highly capable robotic arm designed for precision manipulation in the field.\r\n\r\nKey features:\r\n\r\n- 6‑DOF robotic arm with long reach and finely tuned joints for operating tools, flipping switches, grasping rocks, and performing delicate science and equipment‑servicing tasks\r\n- End‑effector and sensor mounting that support sample collection, inspection, and interaction with URC task boards\r\n- Tracked drive base for confident climbing and traversing rough, Mars‑analog terrain\r\n- Integrated cameras and communications mast for situational awareness and teleoperation over long distances\r\n- Competition‑tested mechanical, electrical, and software architecture, refined through multiple rover generations\r\n- This rover is an excellent showcase of advanced student engineering, with the arm doing most of the heavy lifting—literally and figuratively—during challenge tasks.',9999.00,0,'2025-11-30 17:21:16','2025-12-11 14:17:41',1),(4,'Nussy Jr','This student‑built Mars rover prototype is a six‑wheel exploration platform modeled after planetary rovers, featuring a highly flexible rocker–bogie suspension for traversing uneven terrain. While very much a work in progress—with “characterful” code and plenty of zip‑ties—it’s an ideal testbed for learning real‑world robotics, from mechanical design and wiring to field testing and debugging autonomous behaviors.\r\n\r\nKey features:\r\n\r\n- Six‑wheel rocker–bogie suspension that passively flexes to keep wheels on the ground over bumps and slopes\r\n- Lightweight tubular frame with ample space for sensors, cameras, and computing hardware\r\n- Designed for experimentation with teleoperation, autonomous driving, and navigation algorithms\r\n- Perfect teaching platform for understanding why robust code, wiring, and mechanical design all matter in outdoor robotics',499.00,1,'2025-12-01 12:38:00','2025-12-02 21:23:52',1),(5,'BART','The Bad A$$ Rover Tank is our first full competition Mars rover, a rugged tracked platform that earned 24th place at the University Rover Challenge. Built around a stiff, lightweight aluminum chassis and aggressive tank treads, B.A.R.T. is designed to muscle through loose regolith, rocks, and steep inclines while carrying a capable science and manipulation payload.\r\n\r\nKey features:\r\n\r\nTracked “rover tank” drivetrain for excellent traction and stability on Mars‑analog terrain\r\nLightweight CNC‑style aluminum frame with generous cutouts for strength, serviceability, and mounting electronics\r\nArticulated arm and mast system for sample interaction, tool deployment, and camera positioning\r\nCompetition‑proven platform that laid the groundwork for later, higher‑ranking rover designs',5499.00,1,'2025-12-01 12:42:05','2025-12-02 21:34:46',1),(6,'Arduino Robot','Arduino Smart Rover Kit\r\n\r\nBuild and program your own rover with this Arduino‑based robot car kit. Featuring a sturdy 4‑wheel‑drive chassis with high‑traction rubber tires, this platform is perfect for learning electronics, coding, and robotics.\r\n\r\nThe robot includes:\r\n\r\n- Arduino‑compatible control board pre‑wired to motor drivers and sensor ports\r\n- 4 geared DC motors for precise, independent wheel control\r\n- Swivel‑mounted sensor bracket for adding ultrasonic or other sensors\r\n- Onboard battery pack for fully mobile operation\r\n\r\nIdeal for students, hobbyists, and makers, this kit is great for projects in obstacle avoidance, autonomous navigation, line following, and remote‑controlled driving. Assemble, program, and customize to create your own smart robot vehicle.',59.95,4,'2025-12-02 20:34:24','2025-12-11 15:08:09',1),(7,'Quanser Car','Quanser Self‑Driving Car Platform\r\n\r\nThe Quanser self‑driving car is a high‑performance, 1/10‑scale autonomous vehicle designed for research and education in robotics, controls, and artificial intelligence. Built on a robust RC chassis, it integrates an embedded compute platform, LiDAR sensor, onboard cameras, and high‑precision motor control for realistic autonomous‑driving experiments.\r\n\r\nThe platform supports:\r\n\r\n- Real‑time implementation of perception, planning, and control algorithms\r\n- Line‑following, lane‑keeping, and obstacle‑avoidance demonstrations\r\n- Integration with MATLAB/Simulink, ROS, and common AI/ML frameworks\r\n- Expandable I/O and sensor ports for custom research projects\r\n- Ideal for university labs and advanced training centers, this system provides a complete testbed for modern autonomous vehicle development.',14999.00,0,'2025-12-02 20:51:32','2025-12-11 14:33:04',1),(8,'Zumo Tank','Pololu Zumo Robot Tank\r\n\r\nThe Pololu Zumo is a compact tracked robot platform designed for education, hobby projects, and robotics competitions. Built on a low‑profile tank chassis with rubber tracks, it offers excellent traction and maneuverability on a variety of surfaces. The integrated control board (Zumo shield or Zumo 32U4, depending on model) provides motor drivers, power management, and headers for sensors and add‑on electronics.\r\n\r\nTypical features include:\r\n\r\n- Compact tracked chassis with high‑grip rubber treads\r\n- Integrated dual motor drivers for differential steering\r\n- Onboard microcontroller or Arduino‑compatible shield\r\n- Mounting points for sensors (IR, reflectance array, IMU, etc.)\r\n- Designed for maze solving, line following, mini‑sumo, and autonomous navigation',54.95,8,'2025-12-02 20:56:05','2025-12-02 21:01:06',1),(9,'Turtlebot 3','TurtleBot3 Mobile Robot Platform\r\n\r\nTurtleBot3 is a compact, ROS‑compatible mobile robot designed for learning, research, and rapid prototyping in robotics and AI. Built on a modular chassis with differential drive, it includes a 3D LiDAR or depth camera (model‑dependent), onboard SBC (e.g., Raspberry Pi or similar), and an OpenCR control board for real‑time motor and sensor interfacing.\r\n\r\nKey features:\r\n\r\n- Fully supported by ROS/ROS 2 with extensive tutorials and sample packages\r\n- Modular design for easy customization and sensor/actuator expansion\r\n- Open‑source hardware and software for education and research\r\n- Ideal for SLAM, navigation, multi‑robot systems, and human‑robot interaction projects',649.00,2,'2025-12-02 21:00:54','2025-12-02 21:00:54',1),(10,'Flipper Tank','This custom‑built robot tank is constructed from recycled VEX components and designed specifically for tackling rough terrain and climbing obstacles. Dual rubber tracks provide strong traction, while front and rear articulating flippers pivot to lift the chassis, helping the robot climb over steps, debris, and uneven surfaces that would stop a standard wheeled robot.\r\n\r\nKey features:\r\n\r\n- Tracked tank drive using VEX motors and gearboxes for powerful, precise movement\r\n- Articulating flippers that rotate to boost obstacle‑climbing and self‑recovery\r\n- Modular VEX structure, allowing easy reconfiguration, strengthening, or expansion\r\n- Compatible with VEX microcontrollers, radios, and sensors for autonomous or remote‑controlled operation\r\n- Ideal as a teaching and demo platform for robotics, mechanical design, and control systems, showcasing how repurposed parts can create a capable all‑terrain robot',179.95,4,'2025-12-02 21:08:19','2025-12-02 21:08:31',1),(11,'Turtlebot 2i','The TurtleBot 2i is a versatile ROS‑ready mobile robot built on the proven Kobuki base and a multi‑tier payload tower. Designed for research and education, it provides a stable platform for mobile manipulation, navigation, and human–robot interaction experiments. The open frame makes it easy to mount sensors, cameras, manipulators, and computing hardware such as laptops or mini‑PCs.\r\n\r\nKey features:\r\n\r\n- Kobuki differential‑drive base with wheel encoders, bumper sensors, cliff sensors, and rechargeable battery\r\n- Stackable platform shelves for neatly organizing controllers, power supplies, and experimental payloads\r\n- Full ROS/ROS 2 integration with mapping, localization, and navigation packages\r\n- Ideal for projects in service robotics, indoor navigation, and mobile manipulation in labs and classrooms',2200.00,2,'2025-12-02 21:10:44','2025-12-02 21:10:59',1),(12,'Roomba','This Roomba‑style mobile robot is a modified robotic vacuum platform adapted for research and education. Built on a compact, low‑profile circular base with differential drive, it adds a forward‑mounted depth or vision sensor and additional electronics to support indoor navigation, mapping, and human–robot interaction experiments.\r\n\r\nKey features:\r\n\r\n- Robotic vacuum chassis with integrated bump sensors and rechargeable battery\r\n- Front‑mounted depth/vision sensor for obstacle detection and environment perception\r\n- Ideal for SLAM, autonomous indoor navigation, and service‑robot prototypes\r\n- Low profile allows it to move easily under tables and around furniture in realistic environments',720.00,2,'2025-12-02 21:13:07','2025-12-02 21:13:07',1),(13,'Scooter Bot','This rideable robot platform is built from the rugged base of a mobility scooter and converted into a differential‑drive research vehicle. It retains the original high‑torque drive motors, suspension, and large pneumatic tires, providing a stable, human‑scale platform for experimenting with autonomous navigation, assistive robotics, and human–robot interaction.\r\n\r\nKey features:\r\n\r\n- Differential‑drive mobility scooter base with powerful DC motors and integrated braking\r\n- Ride-on seat and footrest, allowing a human operator to sit or be transported during tests\r\n- Outdoor‑capable chassis with large wheels and suspension for ramps, thresholds, and uneven flooring\r\n- Ample mounting space for controllers, batteries, sensors, and safety hardware (e‑stop, joysticks, etc.) \r\n- Ideal for assistive robotics, telepresence, shared‑control, and full‑scale autonomy experiments',1400.00,1,'2025-12-02 21:15:04','2025-12-02 21:15:04',1),(14,'Research Bot','This legacy research robot is a custom‑built differential‑drive rover originally designed for advanced indoor navigation and perception experiments. The platform combines a rugged wheeled chassis with a powerful onboard computer and a 2D laser scanner mounted on top, making it a capable testbed for early SLAM, mapping, and autonomous navigation research.\r\n\r\nKey features:\r\n\r\n- Rugged, mid‑size wheeled base with large rubber tires for smooth motion on lab floors and uneven surfaces\r\n- Top‑mounted 2D LiDAR sensor for precise range measurements and environment mapping\r\n- Integrated embedded PC and interface boards for real‑time control and data logging\r\n- Multiple front‑facing sensors and status indicators, ideal for experimental perception setups\r\n- Ample interior volume and exterior mounting space for additional sensors, radios, and custom electronics\r\n\r\nWARNING: Item may arrive in conditions ranging from semi-functional to completely broken',3000.00,1,'2025-12-02 21:17:41','2025-12-02 21:17:41',1),(15,'Turtlebot 4','The TurtleBot 4 Lite is a compact, ROS 2–ready mobile robot built on an iRobot® Create® 3 base with an integrated depth camera and 2D LiDAR. Designed for education and research, it offers a powerful yet approachable platform for learning autonomous navigation, mapping, and multi‑robot systems in realistic indoor environments.\r\n\r\nKey features:\r\n\r\n- Create 3 mobile base with bump, cliff, and wheel sensors plus onboard odometry\r\n- Integrated 2D LiDAR and depth camera for SLAM, obstacle avoidance, and perception\r\n- Fully supported by ROS 2 with example packages, demos, and extensive documentation\r\n- Onboard SBC (Raspberry Pi–class) for running navigation, vision, and AI stacks\r\n- Compact footprint ideal for labs, classrooms, and apartment‑scale environments',999.00,3,'2025-12-02 21:19:09','2025-12-02 21:19:09',1),(16,'Fabio','“Fabio” is our NAO humanoid robot, a fully programmable, 58‑cm‑tall platform designed for human–robot interaction, education, and research. With 25 degrees of freedom, integrated cameras, microphones, speakers, and a rich sensor suite, NAO can walk, gesture, recognize faces and objects, and hold natural, speech‑based interactions.\r\n\r\nKey features:\r\n\r\n- Humanoid form factor with articulated arms, legs, and head for expressive motion\r\n- Vision and audio sensors for face detection, object recognition, and speech interaction\r\n- Programmable in Python, C++, and visual tools via the NAOqi framework\r\n- Widely used for HRI, social robotics, classroom teaching, and outreach demos',12000.00,3,'2025-12-02 21:20:23','2025-12-11 15:08:09',1),(17,'Battle Bot','This custom battle bot is a high‑agility combat robot built on a perforated metal chassis with omni wheels and a large spinning disc weapon. Designed for competition and demonstration, it combines rapid maneuverability with a powerful front‑mounted saw blade to deliver dramatic offensive capability in the arena.\r\n\r\nKey features:\r\n\r\n- Omni‑wheel drivetrain for quick strafing, pivoting, and precise positioning\r\n- Large spinning disc/saw blade weapon for high‑impact strikes on opposing robots\r\n- Onboard electronics and microcontroller for motor control, weapon actuation, and radio interface\r\n- Heavy‑duty battery system sized for short, high‑current combat matches\r\n- Open frame for easy modification, repair, and upgrading between bouts',600.00,0,'2025-12-02 21:21:34','2025-12-11 14:24:52',1);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'test','test@test.com','123456789','2025-11-30 17:21:16','2025-11-30 17:21:16',1),(2,'Aidan Stoner','aston2@unh.newhaven.edu','scrypt:32768:8:1$00kOUujafq9t9xSY$e337ca57cf576233c807a740b760867f3f5e7adbeafcd876815f854008369790af01f66437d76e4f9636491ce3c342ca2222f8d7b2a1b55bc8afe59df9bd12a8','2025-11-30 17:21:16','2025-11-30 17:21:16',1),(3,'admin','admin@admin.op','scrypt:32768:8:1$sfAv57luYIZ9cciL$a4d91ad05c1f5989f00bf5dcfd66db38f6069be779fc49e66f7001125b7d8dbfb63a213e9a0e0ab9977268b784f8085b19c8476a6ae837e4c3615bebdbb11703','2025-11-30 18:10:31','2025-11-30 18:10:31',1),(4,'Aidan Stoner','aidanstoner1@gmail.com','scrypt:32768:8:1$P0oKgPXBVnmYBoaz$f2a5fcb148d2a13b7584638510cc81dd9265c0a46a5a3c6f607e5d8554a4ac9d6849ef62260d86bd5e8f05de5eda8cdb495f65adae02529add80f37ccdc5a3e4','2025-12-11 14:26:17','2025-12-11 14:26:17',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-11 15:12:25
