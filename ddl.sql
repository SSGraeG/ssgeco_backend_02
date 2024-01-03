
CREATE SCHEMA IF NOT EXISTS `eco` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `eco` ;

-- -----------------------------------------------------
-- Table `eco`.`mileage_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eco`.`mileage_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `usepoint` INT NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `eco`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eco`.`user` (
  `email` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NULL DEFAULT NULL,
  `address` VARCHAR(50) NULL DEFAULT NULL,
  `mileage` INT NULL DEFAULT '0',
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`email`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `eco`.`milege_tracking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eco`.`milege_tracking` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `use_date` DATETIME NULL DEFAULT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `mileage_category_id` INT NOT NULL,
  `before_mileage` INT NULL DEFAULT NULL,
  `after_mileage` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tracking_user_idx` (`user_email` ASC) VISIBLE,
  INDEX `fk_milege_tracking_mileage_category1_idx` (`mileage_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_milege_tracking_mileage_category1`
    FOREIGN KEY (`mileage_category_id`)
    REFERENCES `eco`.`mileage_category` (`id`),
  CONSTRAINT `fk_tracking_user`
    FOREIGN KEY (`user_email`)
    REFERENCES `eco`.`user` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `eco`.`coupon_list`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eco`.`coupon_list` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `expired_date` DATETIME NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `mileage_category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_coupon_list_user1_idx` (`user_email` ASC) VISIBLE,
  INDEX `fk_coupon_list_mileage_category1_idx` (`mileage_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_coupon_list_user1`
    FOREIGN KEY (`user_email`)
    REFERENCES `eco`.`user` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_coupon_list_mileage_category1`
    FOREIGN KEY (`mileage_category_id`)
    REFERENCES `eco`.`mileage_category` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

use eco;
INSERT INTO `mileage_category` (`name`, `usepoint`, `category`) VALUES
('1000원 쿠폰', 1000, 'coupon'),
('2000원 쿠폰', 2000, 'coupon'),
('연탄 봉사', 1000, 'donation');

-- user 테이블에 더미 데이터 삽입
INSERT INTO `user` (`email`, `name`, `phone`, `address`, `mileage`, `password`) VALUES
('test@test.com', 'User One', '123-456-7890', 'Address 1', 200, 'testtest'),
('user2@example.com', 'User Two', '987-654-3210', 'Address 2', 150, 'password2'),
('user3@example.com', 'User Three', '111-222-3333', 'Address 3', 300, 'password3');

-- milege_tracking 테이블에 더미 데이터 삽입
INSERT INTO `milege_tracking` (`use_date`, `user_email`, `mileage_category_id`, `before_mileage`, `after_mileage`) VALUES
('2023-12-01 10:00:00', 'test@test.com', 4, 200, 150),
('2023-12-02 11:30:00', 'test@test.com', 5, 150, 75),
('2023-12-03 09:45:00', 'user3@example.com', 6, 300, 200);

-- coupon_list 테이블에 더미 데이터 삽입
INSERT INTO `coupon_list` (`expired_date`, `user_email`, `mileage_category_id`) VALUES
('2024-01-01 00:00:00', 'test@test.com', 4),
('2024-01-15 00:00:00', 'user2@example.com', 5),
('2024-01-31 00:00:00', 'test@test.com', 6);