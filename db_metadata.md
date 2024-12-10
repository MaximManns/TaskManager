## Create Table SQL Statements:

```sql
CREATE TABLE `User` (
    `id` int NOT NULL AUTO_INCREMENT,
    `email` varchar(30) DEFAULT NOT NULL,
    `password` varchar(30) DEFAULT NOT NULL,
    `name` varchar(30) DEFAULT NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`),
    KEY `password` (`password`),
    UNIQUE KEY `name` (`name`),
    KEY `ix_User_id` (`id`)
)

CREATE TABLE `Task` (
    `id` int NOT NULL AUTO_INCREMENT,
    `title` varchar(30) DEFAULT NOT NULL,
    `description` varchar(100) DEFAULT NULL,
    `owner_id` int DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `owner_id` (`owner_id`),
    KEY `ix_Task_title` (`title`),
    KEY `ix_Task_description` (`description`),
    KEY `ix_Task_id` (`id`),
    CONSTRAINT `task_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `User` (`id`)
)
