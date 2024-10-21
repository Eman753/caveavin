-- phpMyAdmin SQL Dump
-- version 5.2.1deb4
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : lun. 21 oct. 2024 à 20:14
-- Version du serveur : 11.4.3-MariaDB-1
-- Version de PHP : 8.2.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `caveavin`
--
CREATE DATABASE IF NOT EXISTS `caveavin` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci;
USE `caveavin`;

-- --------------------------------------------------------

--
-- Structure de la table `archives`
--

DROP TABLE IF EXISTS `archives`;
CREATE TABLE IF NOT EXISTS `archives` (
  `id` int(64) NOT NULL AUTO_INCREMENT COMMENT 'Identifiant unique de l''archive',
  `cave` int(64) NOT NULL COMMENT 'Cave associée à l''archive',
  `associate` int(64) NOT NULL COMMENT 'Utilisateur associé à l''archive',
  PRIMARY KEY (`id`),
  KEY `associate` (`associate`),
  KEY `cave_associe` (`cave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='Liste des archives associées aux utilisateurs';

-- --------------------------------------------------------

--
-- Structure de la table `bouteilles`
--

DROP TABLE IF EXISTS `bouteilles`;
CREATE TABLE IF NOT EXISTS `bouteilles` (
  `id` int(64) NOT NULL AUTO_INCREMENT COMMENT 'Identifiant unique de la bouteille',
  `cave` int(64) NOT NULL COMMENT 'Cave associée à la bouteille',
  `etagere` int(64) NOT NULL COMMENT 'ID de l''étagère associée',
  `proprietaire` int(64) NOT NULL COMMENT 'Identifiant de l''utilisateur associé à la bouteille',
  `archive` int(64) DEFAULT NULL COMMENT 'Archive associée à la bouteille',
  `nom` varchar(64) NOT NULL COMMENT 'Nom de la bouteille',
  `domaine` varchar(64) NOT NULL COMMENT 'Domaine associé à la bouteille',
  `type` enum('rouge','rosé','blanc','gris','pinot','pétillant') NOT NULL COMMENT 'Type de vin',
  `annee` int(64) NOT NULL COMMENT 'Millésime',
  `region` varchar(64) NOT NULL COMMENT 'Origine de la bouteille, ou appellation',
  `notePerso` enum('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20') DEFAULT NULL COMMENT 'Note personnelle appliquée à la bouteille sur 20',
  `noteCommu` enum('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20') DEFAULT NULL COMMENT 'Note communautaire appliquée à la bouteille sur 20',
  `photo` text DEFAULT NULL COMMENT 'Chemin amenant à la photo de la bouteille',
  `prix` varchar(64) DEFAULT NULL COMMENT 'Prix de la bouteille',
  `commentaires` text DEFAULT NULL COMMENT 'Commentaires liés à la bouteille',
  PRIMARY KEY (`id`),
  KEY `stockage` (`etagere`),
  KEY `personne` (`proprietaire`),
  KEY `historique` (`archive`),
  KEY `cave_associee` (`cave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='Liste des bouteilles de la cave';

-- --------------------------------------------------------

--
-- Structure de la table `caves`
--

DROP TABLE IF EXISTS `caves`;
CREATE TABLE IF NOT EXISTS `caves` (
  `id` int(64) NOT NULL AUTO_INCREMENT COMMENT 'Identifiant unique de la cave virtuelle',
  `nom` varchar(128) NOT NULL COMMENT 'Nom de la cave',
  `nombresBouteilles` int(64) DEFAULT NULL COMMENT 'Nombre de bouteilles',
  `owner` int(64) NOT NULL COMMENT 'Identifiant de l''utilisateur associé',
  PRIMARY KEY (`id`),
  KEY `nom` (`nom`),
  KEY `appartenance` (`owner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='Liste des caves virtuelles';

-- --------------------------------------------------------

--
-- Structure de la table `etageres`
--

DROP TABLE IF EXISTS `etageres`;
CREATE TABLE IF NOT EXISTS `etageres` (
  `id` int(64) NOT NULL AUTO_INCREMENT COMMENT 'Identifiant unique de l''étagère',
  `cave` int(64) NOT NULL COMMENT 'Cave associée à l''étagère',
  `numero` int(64) NOT NULL COMMENT 'Numéro unique de l''étagère',
  `emplacements` int(64) NOT NULL COMMENT 'Nombre d''emplacements disponibles',
  `nombreBouteilles` int(64) DEFAULT NULL COMMENT 'Nombre de bouteilles présentes dans l''étagère',
  PRIMARY KEY (`id`),
  KEY `numero` (`numero`),
  KEY `cave_linked` (`cave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='Etagères enregistrées dans le système';

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(64) NOT NULL AUTO_INCREMENT COMMENT 'Identifiant unique de l''utilisateur',
  `login` varchar(64) NOT NULL COMMENT 'Login unique de l''utilisateur',
  `nom` varchar(64) NOT NULL COMMENT 'Nom de famille de l''utilisateur',
  `prenom` varchar(64) NOT NULL COMMENT 'Prénom de l''utilisateur',
  `passwd` text DEFAULT NULL COMMENT 'Hash du mot de passe de l''utilisateur',
  `inscription` date DEFAULT current_timestamp() COMMENT 'Date d''inscription de l''utilisateur',
  PRIMARY KEY (`id`),
  KEY `login` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='Liste des utilisateurs du système';

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `archives`
--
ALTER TABLE `archives`
  ADD CONSTRAINT `cave_associe` FOREIGN KEY (`cave`) REFERENCES `caves` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `proprietaire` FOREIGN KEY (`associate`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `bouteilles`
--
ALTER TABLE `bouteilles`
  ADD CONSTRAINT `cave_associee` FOREIGN KEY (`cave`) REFERENCES `caves` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `historique` FOREIGN KEY (`archive`) REFERENCES `archives` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `personne` FOREIGN KEY (`proprietaire`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `stockage` FOREIGN KEY (`etagere`) REFERENCES `etageres` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `caves`
--
ALTER TABLE `caves`
  ADD CONSTRAINT `appartenance` FOREIGN KEY (`owner`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `etageres`
--
ALTER TABLE `etageres`
  ADD CONSTRAINT `cave_linked` FOREIGN KEY (`cave`) REFERENCES `caves` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
